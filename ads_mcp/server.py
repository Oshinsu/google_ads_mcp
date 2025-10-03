import os
import asyncio
from ads_mcp.coordinator import mcp_server
from ads_mcp.scripts.generate_views import update_views_yaml
from ads_mcp.tools import api, docs
import dotenv
dotenv.load_dotenv()

tools = [api, docs]

def _ensure_google_ads_yaml_from_env():
    yaml_inline = os.getenv("GOOGLE_ADS_YAML")
    path_env = os.getenv("GOOGLE_ADS_CREDENTIALS")
    if yaml_inline and not path_env:
        path = "/tmp/google-ads.yaml"
        with open(path, "w") as f:
            f.write(yaml_inline)
        os.environ["GOOGLE_ADS_CREDENTIALS"] = path

def main():
    _ensure_google_ads_yaml_from_env()
    asyncio.run(update_views_yaml())
    api.get_ads_client()

    transport = os.getenv("MCP_TRANSPORT", "stdio")
    if os.getenv("PORT") and transport == "stdio":
        transport = "sse"

    print(f"mcp server starting... transport={transport}")

    if transport == "sse":
        port = int(os.getenv("PORT", "8000"))
        host = os.getenv("HOST", "0.0.0.0")
        mcp_server.run(transport="sse", host=host, port=port)
    else:
        mcp_server.run(transport="stdio")

if __name__ == "__main__":
    main()
