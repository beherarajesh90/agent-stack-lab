# Model Context Protocol (MCP)
# MCP is an open standard for exposing tools to LLMs. An adapter connects to any MCP server and turns its tools into ordinary LangChain tools your agent can call.

# Concept
# MCPAdapter connects to one or many servers and infers the transport — a local script (stdio) or a URL (streamable HTTP).
# await adapter.list_tools() returns tools that drop straight into create_agent.


import asyncio
from pydantic import SecretStr
import os

from langchain.agents import create_agent
from langchain.mcp import MCPAdapter
from langchain.chat_models import init_chat_model
from langchain.agents.middleware import dynamic_prompt, ModelRequest

model = init_chat_model(
    model=os.environ["FLEXAI_MODEL"],
    base_url=os.environ["FLEXAI_URL"],
    api_key=SecretStr(os.environ["FLEXAI_API_KEY"])
)

async def main():
    config = {
        "mcpServers":{
            "weather":{"command": "python", "args": ["weather_server.py"]},  # stdio
             "docs": {"url": "https://example.com/mcp"},                     # http
        }
    }

    async with MCPAdapter(config) as mcpAdapter:
        tools = await mcpAdapter.list_tools()
        agent = create_agent(model=model, tools=tools)
        result = await agent.ainvoke({
            "messages": [{"role": "user", "content": "What's the forecast for Oslo?"}]
        })
        print(result["messages"][-1].content)

asyncio.run(main())

# MCP tools are async, so drive the agent with ainvoke. Mix them freely with your own @tool functions in the same list.


# A single stdio server
# Point the adapter at a local script path — the transport is inferred as stdio.