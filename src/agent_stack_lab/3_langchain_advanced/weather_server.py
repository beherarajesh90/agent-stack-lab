from mcp.server.mcpserver import MCPServer
mcp = MCPServer("Weather Server")

@mcp.tool()
def get_weather(location: str) -> str:
    """Get the current weather forecast for a given location."""
    # Mock weather logic for demonstration purposes
    
    return f"The weather in {location} is 20°C, partly cloudy."

if __name__ == "__main__":
    # Run the server using stdio transport
    mcp.run(transport="stdio")