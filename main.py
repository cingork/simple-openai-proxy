import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
import argparse
from dotenv import load_dotenv
from openai import AsyncOpenAI
import logging
from openai import APIError

from client import get_client, PROVIDERS

app = FastAPI()
client: AsyncOpenAI = None

@app.get("/v1/models")
async def models():
    model_list = await client.models.list()
    return model_list.model_dump()


def error_response(e: Exception) -> JSONResponse:
    if isinstance(e, APIError) and hasattr(e, 'body') and e.body:
        return JSONResponse({"error": e.body}, status_code=e.status_code, media_type="application/json; charset=utf-8")
    return JSONResponse({"error": {"message": str(e)}}, status_code=getattr(e, 'status_code', 500), media_type="application/json; charset=utf-8")

@app.post("/v1/chat/completions")
async def chat(request: Request):
    try:
        data = await request.json()

        if data.get("stream"):
            try:
                response_stream = await client.chat.completions.create(**data)
                
                async def stream():
                    async for chunk in response_stream:
                        yield f"data: {chunk.model_dump_json()}\n\n"

                return StreamingResponse(stream(), media_type="text/event-stream")
            except Exception as e:
                logging.error(f"Streaming error: {e}")
                return error_response(e)
        else:
            completion = await client.chat.completions.create(**data)
            return completion.model_dump()
    except Exception as e:
        logging.error(f"Chat error: {e}")
        return error_response(e)


def running_in_docker() -> bool:
    """Return True if the process is executing inside a Docker container."""
    try:
        if os.path.exists("/.dockerenv"):
            return True
        with open("/proc/1/cgroup", "rt") as f:
            return any(keyword in f.read() for keyword in ("docker", "containerd", "kubepods"))
    except Exception:
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple OpenAI Proxy")
    parser.add_argument("--provider", type=str, choices=list(PROVIDERS.keys()), help="API provider to use.")
    parser.add_argument("--api_key", type=str, help="API key for the selected provider.")
    parser.add_argument("--base_url", type=str, help="Custom API endpoint URL for the 'custom' provider.")
    args = parser.parse_args()

    load_dotenv()

    provider = args.provider or os.getenv("PROVIDER")
    if not provider:
        provider_keys = '/'.join(PROVIDERS.keys())
        provider = input(f"Select API provider ({provider_keys}): ")
        while provider not in PROVIDERS:
            print("Invalid provider.")
            provider = input(f"Select API provider ({provider_keys}): ")

    base_url = args.base_url
    if provider == "custom":
        if not base_url:
            base_url = os.getenv("CUSTOM_API_BASE_URL")
        if not base_url:
            base_url = input("Enter custom API endpoint URL: ")
    else:
        base_url = PROVIDERS[provider]

    # Always use OPENAI_API_KEY for all providers
    API_KEY = args.api_key or os.getenv("OPENAI_API_KEY")
    if not API_KEY:
        API_KEY = input("Enter API key: ")

    client = get_client(api_key=API_KEY, base_url=base_url)


    host = "0.0.0.0" if running_in_docker() else "127.0.0.1"
    uvicorn.run(app, host=host, port=int(os.getenv("PORT", "8192")))