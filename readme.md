# Simple OpenAI Proxy

This project is a simple proxy server for the OpenAI API. It allows you to use the OpenAI API with different providers, such as OpenAI, Azure, or a custom endpoint.

## Features

*   Supports multiple API providers (OpenAI, Azure, custom)
*   Can be configured via command-line arguments or environment variables
*   Provides a simple and easy-to-use interface
*   Supports streaming responses
*   Can be deployed using Docker

## Getting Started

### Prerequisites

*   Python 3.7+
*   pip

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/simple-openai-proxy.git
    ```
2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

The proxy server can be configured using command-line arguments or environment variables.

**Command-line arguments:**

*   `--provider`: The API provider to use (e.g., `openai`, `azure`, `custom`).
*   `--api_key`: The API key for the selected provider.
*   `--base_url`: The custom API endpoint URL for the `custom` provider.

**Environment variables:**

*   `PROVIDER`: The API provider to use.
*   `OPENAI_API_KEY`: The API key for the OpenAI provider.
*   `AZURE_API_KEY`: The API key for the Azure provider.
*   `CUSTOM_API_KEY`: The API key for the custom provider.
*   `CUSTOM_API_BASE_URL`: The custom API endpoint URL for the `custom` provider.
*   `PORT`: The port to run the proxy server on.

### Running the server

To run the proxy server, use the following command:

```bash
python main.py --provider <provider> --api_key <api_key>
```

For example, to run the server with the OpenAI provider, use the following command:

```bash
python main.py --provider openai --api_key <your_openai_api_key>
```

## Usage

The proxy server provides the following endpoints:

*   `/v1/models`: Returns a list of available models.
*   `/v1/chat/completions`: Creates a chat completion.

### Example

To get a list of available models, you can use the following `curl` command:

```bash
curl http://localhost:8192/v1/models
```

To create a chat completion, you can use the following `curl` command:

```bash
curl http://localhost:8192/v1/chat/completions -H "Content-Type: application/json" -d '{
  "model": "gpt-3.5-turbo",
  "messages": [
    {
      "role": "user",
      "content": "Hello!"
    }
  ]
}'
```

## Docker

To build and run the project using Docker, use the following commands:

1.  Build the Docker image:
    ```bash
    docker build -t simple-openai-proxy .
    ```
2.  Run the Docker container:
    ```bash
    docker run -p 8192:8192 -e PROVIDER=<provider> -e <PROVIDER>_API_KEY=<api_key> simple-openai-proxy
    ```

For example, to run the container with the OpenAI provider, use the following command:

```bash
docker run -p 8192:8192 -e PROVIDER=openai -e OPENAI_API_KEY=<your_openai_api_key> simple-openai-proxy
```
