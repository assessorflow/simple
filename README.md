# Greeting Agent

A simple greeting agent powered by OpenAI Response API with A2A protocol compatibility.

## Features

- **OpenAI Response API** - Uses the OpenAI Responses API for generating greetings
- **Configurable** - Environment-based configuration for API key, base URL, and model
- **Pydantic schemas** - Type-safe input/output with Pydantic validation
- **A2A compatible** - Implements the Agent-to-Agent protocol for multi-agent systems

## Installation

```bash
uv venv && source .venv/bin/activate && uv pip install -e .
```

## Configuration

Copy `.env.example` to `.env` and configure:

```bash
OPENAI_API_KEY=your-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

## Usage

```bash
uvicorn src.main:app --reload
```

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health info and available endpoints |
| GET | `/health` | Health check |
| POST | `/greet` | Generate a greeting |
| POST | `/chat` | Chat with the agent |
| GET | `/a2a` | Get agent card (A2A discovery) |
| POST | `/a2a` | Send A2A message |
| GET | `/a2a/schema` | Get supported A2A message types |

### Examples

**Greet endpoint:**
```bash
curl -X POST http://localhost:8000/greet \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "style": "friendly"}'
```

**Chat endpoint:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?"}'
```

**A2A greeting:**
```bash
curl -X POST http://localhost:8000/a2a \
  -H "Content-Type: application/json" \
  -d '{"type": "greeting", "content": {"name": "Bob", "style": "formal"}}'
```

### Greeting Styles

- `formal` - Professional, formal greeting
- `casual` - Relaxed, informal greeting
- `friendly` (default) - Warm, friendly greeting
