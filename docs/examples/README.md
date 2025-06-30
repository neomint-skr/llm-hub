# LLM Hub API Examples

This directory contains code examples for interacting with LLM Hub APIs in various programming languages.

## Available Examples

### Python (`python/`)
- **`basic_usage.py`** - Complete Python client with async support
- Features: Health checks, tool listing, text generation, batch processing
- Requirements: `httpx`, `asyncio`

### JavaScript (`javascript/`)
- **`basic_usage.js`** - Browser and Node.js compatible client
- Features: Modern async/await, fetch API, error handling
- Works in: Browser, Node.js, React, Vue, etc.

### cURL (`curl/`)
- **`basic_usage.sh`** - Shell script with comprehensive API examples
- Features: All endpoints, error handling, performance testing
- Requirements: `curl`, optional `jq` for JSON formatting

## Quick Start

### Prerequisites

1. **Start LLM Hub services**
   ```bash
   cd ops/compose
   docker-compose up -d
   ```

2. **Verify services are running**
   ```bash
   curl http://localhost:8080/health
   curl http://localhost:3000/health
   ```

### Python Example

```bash
cd docs/examples/python
pip install httpx
python basic_usage.py
```

### JavaScript Example

**Node.js:**
```bash
cd docs/examples/javascript
node basic_usage.js
```

**Browser:**
```html
<script src="basic_usage.js"></script>
<script>
    const client = new LLMHubClient();
    client.checkHealth().then(console.log);
</script>
```

### cURL Example

```bash
cd docs/examples/curl
chmod +x basic_usage.sh
./basic_usage.sh
```

## Configuration

All examples use these default settings:

| Setting | Default Value | Environment Variable |
|---------|---------------|---------------------|
| Gateway URL | `http://localhost:8080` | `GATEWAY_URL` |
| API Key | `changeme` | `API_KEY` |

### Customizing Configuration

**Python:**
```python
client = LLMHubClient(
    gateway_url="http://your-gateway:8080",
    api_key="your-api-key"
)
```

**JavaScript:**
```javascript
const client = new LLMHubClient(
    'http://your-gateway:8080',
    'your-api-key'
);
```

**cURL:**
```bash
export GATEWAY_URL="http://your-gateway:8080"
export API_KEY="your-api-key"
./basic_usage.sh
```

## Common Use Cases

### 1. Health Monitoring

Check if services are running and healthy:

```python
# Python
health = await client.check_health()
print(f"Status: {health['status']}")
```

```bash
# cURL
curl http://localhost:8080/health
```

### 2. List Available Models

Get all models available for text generation:

```python
# Python
models = await client.list_models()
for model in models:
    print(f"- {model['id']}: {model['name']}")
```

```bash
# cURL
curl -H "Authorization: Bearer changeme" \
     -H "Content-Type: application/json" \
     -d '{"parameters":{}}' \
     http://localhost:8080/tools/list_models
```

### 3. Generate Text

Generate text using a specific model:

```python
# Python
result = await client.generate_text(
    prompt="Write a haiku about coding",
    model="llama-2-7b-chat",
    temperature=0.8,
    max_tokens=100
)
print(result)
```

```bash
# cURL
curl -X POST \
     -H "Authorization: Bearer changeme" \
     -H "Content-Type: application/json" \
     -d '{
       "parameters": {
         "prompt": "Write a haiku about coding",
         "model": "llama-2-7b-chat",
         "temperature": 0.8,
         "max_tokens": 100
       }
     }' \
     http://localhost:8080/tools/inference
```

### 4. Batch Processing

Process multiple prompts efficiently:

```python
# Python
prompts = ["Hello", "How are you?", "Goodbye"]
tasks = [
    client.generate_text(prompt, model_id)
    for prompt in prompts
]
results = await asyncio.gather(*tasks)
```

```javascript
// JavaScript
const prompts = ["Hello", "How are you?", "Goodbye"];
const promises = prompts.map(prompt =>
    client.generateText(prompt, modelId)
);
const results = await Promise.all(promises);
```

## Error Handling

### Common HTTP Status Codes

| Code | Meaning | Common Causes |
|------|---------|---------------|
| 200 | Success | Request completed successfully |
| 400 | Bad Request | Invalid JSON or missing parameters |
| 401 | Unauthorized | Missing or invalid API key |
| 404 | Not Found | Invalid endpoint or tool name |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Service error or LM Studio unavailable |

### Error Handling Examples

**Python:**
```python
try:
    result = await client.generate_text(prompt, model)
except httpx.HTTPStatusError as e:
    if e.response.status_code == 401:
        print("Invalid API key")
    elif e.response.status_code == 429:
        print("Rate limit exceeded")
    else:
        print(f"HTTP error: {e.response.status_code}")
except httpx.RequestError as e:
    print(f"Connection error: {e}")
```

**JavaScript:**
```javascript
try {
    const result = await client.generateText(prompt, model);
} catch (error) {
    if (error.message.includes('401')) {
        console.log('Invalid API key');
    } else if (error.message.includes('429')) {
        console.log('Rate limit exceeded');
    } else {
        console.log(`Error: ${error.message}`);
    }
}
```

## Performance Tips

### 1. Connection Reuse

**Python:**
```python
# Reuse client instance
client = LLMHubClient()
# Make multiple requests with same client
```

**JavaScript:**
```javascript
// Reuse client instance
const client = new LLMHubClient();
// Make multiple requests with same client
```

### 2. Concurrent Requests

**Python:**
```python
# Process multiple requests concurrently
tasks = [client.generate_text(prompt, model) for prompt in prompts]
results = await asyncio.gather(*tasks)
```

**JavaScript:**
```javascript
// Process multiple requests concurrently
const promises = prompts.map(prompt => client.generateText(prompt, model));
const results = await Promise.all(promises);
```

### 3. Timeout Configuration

**Python:**
```python
async with httpx.AsyncClient(timeout=60.0) as client:
    # Longer timeout for text generation
```

**JavaScript:**
```javascript
// Use AbortController for timeout
const controller = new AbortController();
setTimeout(() => controller.abort(), 60000);
fetch(url, { signal: controller.signal });
```

## Troubleshooting

### Services Not Responding

1. **Check if services are running:**
   ```bash
   docker-compose ps
   ```

2. **Check service logs:**
   ```bash
   docker-compose logs unified-gateway
   docker-compose logs lm-studio-bridge
   ```

3. **Verify LM Studio is running:**
   ```bash
   curl http://localhost:1234/v1/models
   ```

### Authentication Issues

1. **Check API key in environment:**
   ```bash
   echo $API_KEY
   ```

2. **Verify API key in service configuration:**
   ```bash
   grep API_KEY ops/compose/.env
   ```

3. **Test without authentication (development only):**
   ```bash
   # Set AUTH_ENABLED=false in .env file
   ```

### Network Issues

1. **Check port availability:**
   ```bash
   netstat -an | grep 8080
   netstat -an | grep 3000
   ```

2. **Test direct connectivity:**
   ```bash
   telnet localhost 8080
   telnet localhost 3000
   ```

3. **Check firewall settings:**
   ```bash
   # Windows
   netsh advfirewall show allprofiles
   
   # Linux
   sudo ufw status
   ```

## Contributing

To add examples for additional languages:

1. Create a new directory: `docs/examples/your-language/`
2. Add a basic usage example following the same pattern
3. Update this README with the new language
4. Test the example with a running LLM Hub instance
5. Submit a pull request

### Example Structure

Each language example should include:
- Health check functionality
- Tool listing
- Model listing  
- Text generation
- Error handling
- Clear documentation and comments
