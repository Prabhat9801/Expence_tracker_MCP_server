import random
import json
from fastmcp import FastMCP

# Create FastMCP server instance
mcp = FastMCP(name="Simple Calculator Server")

# -----------------------
# TOOLS
# -----------------------

@mcp.tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together

    Args:
        a: First number
        b: Second number
    Returns:
        The sum of a and b
    """
    return a + b


@mcp.tool
def random_number(min_val: int = 1, max_val: int = 100) -> int:
    """Generate a random integer within a range
    
    Args:
        min_val: Minimum value (default: 1)
        max_val: Maximum value (default: 100)
        
    Returns:
        A random integer between min_val and max_val
    """
    return random.randint(min_val, max_val)

# -----------------------
# RESOURCE
# -----------------------

@mcp.resource("info://server")
def server_info() -> str:
    """Get information about this server"""
    info = {
        "name": "Simple Calculator Server",
        "version": "1.0.0",
        "description": "A basic MCP server with math tools",
        "tools": ["add_numbers", "random_number"],
        "author": "Your Name"
    }
    return json.dumps(info, indent=2)

# -----------------------
# RUN SERVER
# -----------------------

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
