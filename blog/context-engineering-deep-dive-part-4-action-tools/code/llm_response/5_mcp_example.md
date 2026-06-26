🚀 MCP (Model Context Protocol) with Python SDK Demo

============================================================

=== LLM Agent with MCP (Configuration-based) ===


=== MCP Configuration (like Claude Desktop) ===

📋 MCP Server Configuration:
  time: uvx mcp-server-time
🔧 Discovering tools from configured MCP servers...
🚀 Starting MCP server: uvx mcp-server-time
✅ MCP server started and initialized successfully
   ✅ time: 2 tools available
🔌 MCP connection closed

📦 Total tools available: 2

👤 User: What time is it in UTC?
----------------------------------------
  🔧 Calling MCP tool: get_current_time
     Arguments: {'timezone': 'UTC'}
🚀 Starting MCP server: uvx mcp-server-time
✅ MCP server started and initialized successfully
     ✅ Result: {
  "timezone": "UTC",
  "datetime": "2025-08-21T04:52:31+00:00",
  "is_dst": false
}
🔌 MCP connection closed
🤖 Agent: Based on the tools:

📅 {
  "timezone": "UTC",
  "datetime": "2025-08-21T04:52:31+00:00",
  "is_dst": false
}
============================================================

👤 User: What time is it in Paris?
----------------------------------------
  🔧 Calling MCP tool: get_current_time
     Arguments: {'timezone': 'Europe/Paris'}
🚀 Starting MCP server: uvx mcp-server-time
✅ MCP server started and initialized successfully
     ✅ Result: {
  "timezone": "Europe/Paris",
  "datetime": "2025-08-21T06:52:33+02:00",
  "is_dst": true
}
🔌 MCP connection closed
🤖 Agent: Based on the tools:

📅 {
  "timezone": "Europe/Paris",
  "datetime": "2025-08-21T06:52:33+02:00",
  "is_dst": true
}
============================================================

👤 User: Convert 3pm in New York to London time
----------------------------------------
  🔧 Calling MCP tool: convert_time
     Arguments: {'source_timezone': 'America/New_York', 'time': '15:00', 'target_timezone': 'Europe/London'}
🚀 Starting MCP server: uvx mcp-server-time
✅ MCP server started and initialized successfully
     ✅ Result: {
  "source": {
    "timezone": "America/New_York",
    "datetime": "2025-08-21T15:00:00-04:00",
    "is_dst": true
  },
  "target": {
    "timezone": "Europe/London",
    "datetime": "2025-08-21T20:00:00+01:00",
    "is_dst": true
  },
  "time_difference": "+5.0h"
}
🔌 MCP connection closed
🤖 Agent: Based on the tools:

📅 {
  "source": {
    "timezone": "America/New_York",
    "datetime": "2025-08-21T15:00:00-04:00",
    "is_dst": true
  },
  "target": {
    "timezone": "Europe/London",
    "datetime": "2025-08-21T20:00:00+01:00",
    "is_dst": true
  },
  "time_difference": "+5.0h"
}
============================================================

👤 User: What time is it in Tokyo?
----------------------------------------
  🔧 Calling MCP tool: get_current_time
     Arguments: {'timezone': 'Asia/Tokyo'}
🚀 Starting MCP server: uvx mcp-server-time
✅ MCP server started and initialized successfully
     ✅ Result: {
  "timezone": "Asia/Tokyo",
  "datetime": "2025-08-21T13:52:36+09:00",
  "is_dst": false
}
🔌 MCP connection closed
🤖 Agent: Based on the tools:

📅 {
  "timezone": "Asia/Tokyo",
  "datetime": "2025-08-21T13:52:36+09:00",
  "is_dst": false
}
============================================================
✅ Agent cleanup complete - using direct connections
