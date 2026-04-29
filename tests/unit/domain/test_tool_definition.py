# tests/unit/domain/test_tool_definition.py
from src.domain.entities.tool_definition import ToolDefinition, ToolParameter


def test_to_openai_schema():
    tool = ToolDefinition(
        name="get_weather",
        description="Get current weather",
        parameters=[
            ToolParameter(name="location", type="string", description="City name", required=True),
        ],
    )
    schema = tool.to_openai_schema()
    assert schema["type"] == "function"
    assert schema["function"]["name"] == "get_weather"
    assert "location" in schema["function"]["parameters"]["properties"]
    assert "location" in schema["function"]["parameters"]["required"]
