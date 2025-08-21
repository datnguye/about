"""
Example 5: MCP (Model Context Protocol) with MCP Python SDK
Demonstrates proper MCP client usage with the official Python SDK
"""

import asyncio
import json
from typing import Any, Dict, List
from litellm import completion
from dotenv import load_dotenv
from os import getenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()


async def create_mcp_session(server_command: List[str]):
    """Create MCP session using stdio_client directly"""
    print(f"🚀 Starting MCP server: {' '.join(server_command)}")

    # Create server parameters
    if len(server_command) > 1:
        server_params = StdioServerParameters(
            command=server_command[0], args=server_command[1:]
        )
    else:
        server_params = StdioServerParameters(command=server_command[0], args=[])

    try:
        # Create stdio connection and session using context manager
        stdio_ctx = stdio_client(server_params)
        read_stream, write_stream = await stdio_ctx.__aenter__()

        session_ctx = ClientSession(read_stream, write_stream)
        session = await session_ctx.__aenter__()

        await session.initialize()
        print("✅ MCP server started and initialized successfully")

        return session, session_ctx, stdio_ctx

    except Exception as e:
        print(f"❌ Failed to start MCP server: {e}")
        print("📝 Note: Install with: uvx --help (ensure uvx is available)")
        print("   Or: uv add mcp-server-time")
        raise


async def close_mcp_session(session_ctx, stdio_ctx):
    """Close MCP session and cleanup contexts"""
    try:
        if session_ctx:
            await session_ctx.__aexit__(None, None, None)
        if stdio_ctx:
            await stdio_ctx.__aexit__(None, None, None)
        print("🔌 MCP connection closed")
    except Exception as e:
        print(f"⚠️ Error during cleanup: {e}")


async def list_mcp_tools(session: ClientSession) -> List[Dict]:
    """List available tools from the MCP session"""
    try:
        tools_response = await session.list_tools()
        tools = []

        for tool in tools_response.tools:
            tools.append(
                {
                    "name": tool.name,
                    "description": tool.description,
                    "inputSchema": tool.inputSchema,
                }
            )

        return tools

    except Exception as e:
        print(f"❌ Failed to list tools: {e}")
        return []


async def call_mcp_tool(
    session: ClientSession, tool_name: str, arguments: Dict[str, Any] = None
) -> Dict:
    """Call a tool on the MCP session"""
    try:
        result = await session.call_tool(tool_name, arguments or {})

        # Convert MCP result to our expected format
        content = []
        for item in result.content:
            if hasattr(item, "text"):
                content.append({"type": "text", "text": item.text})
            else:
                content.append({"type": "unknown", "text": str(item)})

        return {"content": content}

    except Exception as e:
        print(f"❌ Tool call failed: {e}")
        return {"content": [{"type": "text", "text": f"Error: {e}"}]}


class MCPAgent:
    """LLM Agent with MCP server configuration (like Claude Desktop/VS Code)"""

    def __init__(self, mcp_servers_config: Dict):
        """Initialize with MCP server configuration

        Args:
            mcp_servers_config: Dict with server configurations like:
            {
                "time": {
                    "command": "uvx",
                    "args": ["mcp-server-time"]
                }
            }
        """
        self.servers_config = mcp_servers_config
        self.available_tools = []
        self.conversation_history = []
        self.tool_to_server_map = {}  # Maps tool names to server names

    async def setup(self):
        """Discover tools from all configured MCP servers"""
        print("🔧 Discovering tools from configured MCP servers...")

        for server_name, config in self.servers_config.items():
            session_ctx = None
            stdio_ctx = None
            try:
                command = [config["command"]] + config["args"]

                # Create session and get tools
                session, session_ctx, stdio_ctx = await create_mcp_session(command)
                tools = await list_mcp_tools(session)

                # Map each tool to this server
                for tool in tools:
                    self.tool_to_server_map[tool["name"]] = {
                        "server_name": server_name,
                        "command": command,
                    }

                self.available_tools.extend(tools)
                print(f"   ✅ {server_name}: {len(tools)} tools available")

            except Exception as e:
                print(f"   ❌ {server_name}: Failed to connect - {e}")
                print(
                    "      Make sure the MCP server is properly installed and available"
                )
            finally:
                if session_ctx or stdio_ctx:
                    try:
                        await close_mcp_session(session_ctx, stdio_ctx)
                    except Exception:
                        pass

        print(f"\n📦 Total tools available: {len(self.available_tools)}")
        return len(self.available_tools) > 0

    def _convert_to_openai_tools(self) -> List[Dict]:
        """Convert MCP tools to OpenAI function calling format"""
        openai_tools = []
        for tool in self.available_tools:
            openai_tool = {
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool.get("description", ""),
                    "parameters": tool.get(
                        "inputSchema", {"type": "object", "properties": {}}
                    ),
                },
            }
            openai_tools.append(openai_tool)
        return openai_tools

    async def chat(self, user_message: str) -> str:
        """Process user message with MCP tool access"""

        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": user_message})

        # System prompt with available tools
        tools_info = "\n".join(
            [
                f"- {tool['name']}: {tool.get('description', 'No description')}"
                for tool in self.available_tools
            ]
        )

        system_prompt = f"""You are a helpful assistant with access to tools via MCP.
Available tools:
{tools_info}

Use these tools when appropriate to answer user questions."""

        # Prepare messages
        messages = [
            {"role": "system", "content": system_prompt},
            *self.conversation_history,
        ]

        # Get OpenAI-formatted tools
        tools = self._convert_to_openai_tools()

        try:
            # Call LLM with tools
            response = completion(
                model="openrouter/openai/gpt-4o-mini",
                api_key=getenv("OPENROUTER_API_KEY"),
                messages=messages,
                tools=tools if tools else None,
                tool_choice="auto" if tools else None,
                temperature=0.3,
            )

            message = response.choices[0].message

            # Handle tool calls
            if hasattr(message, "tool_calls") and message.tool_calls:
                tool_results = []

                for tool_call in message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = (
                        json.loads(tool_call.function.arguments)
                        if tool_call.function.arguments
                        else {}
                    )

                    print(f"  🔧 Calling MCP tool: {tool_name}")
                    if tool_args:
                        print(f"     Arguments: {tool_args}")

                    # Get server info for this tool
                    server_info = self.tool_to_server_map.get(tool_name)
                    if server_info:
                        session_ctx = None
                        stdio_ctx = None
                        try:
                            # Create session and call tool
                            session, session_ctx, stdio_ctx = await create_mcp_session(
                                server_info["command"]
                            )
                            mcp_result = await call_mcp_tool(
                                session, tool_name, tool_args
                            )

                            if mcp_result.get("content"):
                                content = mcp_result["content"][0].get(
                                    "text", "No result"
                                )
                                tool_results.append(f"📅 {content}")
                                print(f"     ✅ Result: {content}")

                        except Exception as e:
                            print(f"     ❌ Tool call error: {e}")
                        finally:
                            if session_ctx or stdio_ctx:
                                try:
                                    await close_mcp_session(session_ctx, stdio_ctx)
                                except Exception:
                                    pass
                    else:
                        print(f"     ❌ No server found for tool: {tool_name}")

                # Format response
                response_text = message.content or "Based on the tools:"
                if tool_results:
                    response_text += "\n\n" + "\n".join(tool_results)

            else:
                response_text = message.content

            # Add to history
            self.conversation_history.append(
                {"role": "assistant", "content": response_text}
            )

            return response_text

        except Exception as e:
            return f"Error: {str(e)}"

    async def cleanup(self):
        """No persistent connections to clean up"""
        print("✅ Agent cleanup complete - using direct connections")


def get_mcp_config():
    """Show MCP configuration like Claude Desktop/VS Code"""
    print("\n=== MCP Configuration (like Claude Desktop) ===\n")

    mcp_config = {
        "time": {"command": "uvx", "args": ["mcp-server-time"]}
        # In real usage, you might have multiple servers:
        # "filesystem": {
        #     "command": "uvx",
        #     "args": ["mcp-server-filesystem", "--allowed-dirs", "/safe/path"]
        # },
        # "sqlite": {
        #     "command": "uvx",
        #     "args": ["mcp-server-sqlite", "--db", "data.db"]
        # }
    }

    print("📋 MCP Server Configuration:")
    for name, config in mcp_config.items():
        print(f"  {name}: {config['command']} {' '.join(config['args'])}")

    return mcp_config


async def demonstrate_agent_integration():
    """Demonstrate LLM agent with MCP configuration"""
    print("\n=== LLM Agent with MCP (Configuration-based) ===\n")

    # Get MCP configuration
    mcp_config = get_mcp_config()

    # Initialize agent with configuration
    agent = MCPAgent(mcp_config)

    try:
        if await agent.setup():
            # Test queries
            queries = [
                "What time is it in UTC?",
                "What time is it in Paris?",
                "Convert 3pm in New York to London time",
                "What time is it in Tokyo?",
            ]

            for query in queries:
                print(f"\n👤 User: {query}")
                print("-" * 40)
                response = await agent.chat(query)
                print(f"🤖 Agent: {response}")
                print("=" * 60)
        else:
            print("❌ No MCP tools available - server connection failed")

    except Exception as e:
        print(f"❌ Agent demo failed: {e}")

    finally:
        await agent.cleanup()


async def main():
    """Main async function to run all demos"""
    print("🚀 MCP (Model Context Protocol) with Python SDK Demo\n")
    print("=" * 60)

    try:
        # Show agent integration with configuration
        await demonstrate_agent_integration()

    except Exception as e:
        print(f"\n❌ MCP demo failed: {e}")
        print("   Please ensure MCP servers are properly installed and available")


if __name__ == "__main__":
    asyncio.run(main())
