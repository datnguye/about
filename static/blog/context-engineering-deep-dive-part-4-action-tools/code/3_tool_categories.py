"""
Example 3: Tool Categories and Risk Assessment
Demonstrates the hierarchy of tool danger and appropriate safeguards
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional


class RiskLevel(Enum):
    """Risk levels for tools"""

    SAFE = "🟢 Safe"
    MODERATE = "🟡 Moderate"
    HIGH = "🔴 High"
    CRITICAL = "⛔ Critical"


@dataclass
class ToolDefinition:
    """Tool definition with risk assessment"""

    name: str
    description: str
    risk_level: RiskLevel
    safeguards: List[str]
    requires_approval: bool = False
    rate_limit: Optional[int] = None
    audit_required: bool = False


class ToolRegistry:
    """Registry of available tools with risk categorization"""

    def __init__(self):
        self.tools: Dict[str, ToolDefinition] = {}
        self._register_tools()

    def _register_tools(self):
        """Register all available tools with their risk profiles"""

        # Safe tools - start here
        safe_tools = [
            ToolDefinition(
                name="search_documentation",
                description="Search and read API documentation",
                risk_level=RiskLevel.SAFE,
                safeguards=["Read-only access"],
                rate_limit=100,
            ),
            ToolDefinition(
                name="query_analytics",
                description="Read-only database queries on analytics DB",
                risk_level=RiskLevel.SAFE,
                safeguards=[
                    "Read-only credentials",
                    "Automatic LIMIT clause",
                    "Query timeout 30s",
                ],
                rate_limit=50,
                audit_required=True,
            ),
            ToolDefinition(
                name="fetch_metrics",
                description="Get performance metrics from monitoring",
                risk_level=RiskLevel.SAFE,
                safeguards=["Cached responses", "Rate limiting"],
                rate_limit=60,
            ),
            ToolDefinition(
                name="list_files",
                description="List directory contents",
                risk_level=RiskLevel.SAFE,
                safeguards=["Restricted to project directories", "No system paths"],
                rate_limit=100,
            ),
        ]

        # Moderate risk tools - add safeguards
        moderate_tools = [
            ToolDefinition(
                name="send_slack_message",
                description="Send messages to Slack channels",
                risk_level=RiskLevel.MODERATE,
                safeguards=[
                    "Rate limited to 10/minute",
                    "Restricted to specific channels",
                    "Message length limit",
                ],
                rate_limit=10,
                audit_required=True,
            ),
            ToolDefinition(
                name="create_jira_ticket",
                description="Create tickets in Jira",
                risk_level=RiskLevel.MODERATE,
                safeguards=[
                    "Template-based creation only",
                    "No custom field modifications",
                    "Rate limited",
                ],
                rate_limit=5,
                audit_required=True,
            ),
            ToolDefinition(
                name="generate_report",
                description="Generate PDF/CSV reports",
                risk_level=RiskLevel.MODERATE,
                safeguards=[
                    "Resource limits (CPU/Memory)",
                    "Sandboxed execution",
                    "Output size limits",
                ],
                rate_limit=10,
                audit_required=True,
            ),
            ToolDefinition(
                name="cache_invalidation",
                description="Invalidate specific cache keys",
                risk_level=RiskLevel.MODERATE,
                safeguards=[
                    "Whitelist of allowed cache keys",
                    "Rate limiting",
                    "Rollback capability",
                ],
                rate_limit=5,
                audit_required=True,
            ),
        ]

        # High risk tools - require human approval
        high_risk_tools = [
            ToolDefinition(
                name="execute_code",
                description="Execute arbitrary code in sandbox",
                risk_level=RiskLevel.HIGH,
                safeguards=[
                    "Sandboxed environment",
                    "Resource limits",
                    "Timeout enforcement",
                    "No network access",
                ],
                requires_approval=True,
                rate_limit=1,
                audit_required=True,
            ),
            ToolDefinition(
                name="database_write",
                description="Modify database records",
                risk_level=RiskLevel.HIGH,
                safeguards=[
                    "Transaction rollback capability",
                    "Backup before modification",
                    "Human approval required",
                ],
                requires_approval=True,
                rate_limit=1,
                audit_required=True,
            ),
            ToolDefinition(
                name="send_email",
                description="Send emails to external recipients",
                risk_level=RiskLevel.HIGH,
                safeguards=[
                    "Template-based only",
                    "Recipient whitelist",
                    "Human approval for new recipients",
                ],
                requires_approval=True,
                rate_limit=5,
                audit_required=True,
            ),
        ]

        # Critical tools - never fully automate
        critical_tools = [
            ToolDefinition(
                name="deploy_code",
                description="Deploy code to production",
                risk_level=RiskLevel.CRITICAL,
                safeguards=[
                    "Multi-stage approval",
                    "Automated testing required",
                    "Rollback plan mandatory",
                    "Change window enforcement",
                ],
                requires_approval=True,
                rate_limit=1,
                audit_required=True,
            ),
            ToolDefinition(
                name="modify_infrastructure",
                description="Change infrastructure configuration",
                risk_level=RiskLevel.CRITICAL,
                safeguards=[
                    "Terraform plan review",
                    "Cost estimation",
                    "Multi-person approval",
                    "Backup state required",
                ],
                requires_approval=True,
                rate_limit=1,
                audit_required=True,
            ),
        ]

        # Register all tools
        for tool in safe_tools + moderate_tools + high_risk_tools + critical_tools:
            self.tools[tool.name] = tool

    def get_tool(self, name: str) -> Optional[ToolDefinition]:
        """Get tool by name"""
        return self.tools.get(name)

    def get_tools_by_risk(self, risk_level: RiskLevel) -> List[ToolDefinition]:
        """Get all tools of a specific risk level"""
        return [tool for tool in self.tools.values() if tool.risk_level == risk_level]

    def can_execute_automatically(self, tool_name: str) -> bool:
        """Check if tool can be executed without human approval"""
        tool = self.get_tool(tool_name)
        return tool and not tool.requires_approval


def demonstrate_tool_categories():
    """Show tool categorization and risk assessment"""
    print("=== Tool Risk Categories ===\n")

    registry = ToolRegistry()

    # Display tools by risk level
    for risk_level in RiskLevel:
        tools = registry.get_tools_by_risk(risk_level)
        if tools:
            print(f"\n{risk_level.value} - {len(tools)} tools:")
            print("-" * 40)

            for tool in tools:
                print(f"\n  📦 {tool.name}")
                print(f"     {tool.description}")
                print("     Safeguards:")
                for safeguard in tool.safeguards[:3]:  # Show first 3
                    print(f"       • {safeguard}")
                if tool.requires_approval:
                    print("       ⚠️  Requires human approval")
                if tool.rate_limit:
                    print(f"       ⏱️  Rate limit: {tool.rate_limit}/min")


def demonstrate_execution_decision():
    """Show execution decision logic"""
    print("\n\n=== Execution Decision Logic ===\n")

    registry = ToolRegistry()

    test_tools = [
        "search_documentation",
        "send_slack_message",
        "database_write",
        "deploy_code",
    ]

    for tool_name in test_tools:
        tool = registry.get_tool(tool_name)
        if tool:
            print(f"\nTool: {tool.name}")
            print(f"Risk: {tool.risk_level.value}")

            if registry.can_execute_automatically(tool_name):
                print("✅ Can execute automatically")
                print(f"   Rate limit: {tool.rate_limit}/min")
            else:
                print("🛑 Requires human approval")
                print("   Safeguards:", ", ".join(tool.safeguards[:2]))


if __name__ == "__main__":
    print("Tool Categories and Risk Assessment\n")
    print("=" * 50)

    demonstrate_tool_categories()
    demonstrate_execution_decision()