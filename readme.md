# Simple OpenAI Proxy

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

This project is a simple proxy server for the OpenAI API. It allows you to use the OpenAI API with different providers, such as OpenAI, Azure, or a custom endpoint.

## Features

*   Supports multiple API providers (OpenAI, Groq, OpenRouter, custom)
*   Can be configured via command-line arguments or environment variables
*   Provides a simple and easy-to-use interface
*   Supports streaming responses
*   Can be deployed using Docker

## Getting Started

### Prerequisites

*   Python 3.9+
*   pip

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/cingork/simple-openai-proxy
    ```
2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

The proxy server can be configured using command-line arguments or environment variables.

**Command-line arguments:**

*   `--provider`: The API provider to use (e.g., `openai`, `groq`, `openrouter`, `custom`).
*   `--api_key`: The API key for the selected provider.
*   `--base_url`: The custom API endpoint URL for the `custom` provider.

**Environment variables:**

*   `PROVIDER`: The API provider to use.
*   `OPENAI_API_KEY`: The API key for the OpenAI provider.
*   `CUSTOM_API_BASE_URL`: The custom API endpoint URL for the `custom` provider. **Required if using the `custom` provider.**
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

To use a custom provider, you must specify the custom API endpoint URL using the `--base_url` argument:

```bash
python main.py --provider custom --api_key <your_custom_api_key> --base_url <your_custom_api_base_url>
```

**Alternatively**, you can run the script without any arguments and it will prompt you to manually enter the API provider and API key:

```bash
python main.py
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
  "model": "gpt-5-mini",
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
    docker-compose build
    ```
2.  Run the Docker container:
    ```bash
    docker-compose up
    ```

For example, to run the container with the OpenAI provider, create a `.env` file with the following content:
```
PROVIDER=openai
OPENAI_API_KEY=<your_openai_api_key>
```

To use a custom provider, your `.env` file should include both the provider and the custom API base URL:
```
PROVIDER=custom
CUSTOM_API_KEY=<your_custom_api_key>
CUSTOM_API_BASE_URL=<your_custom_api_base_url>
PORT=8192
```
And then run `docker-compose up`.
