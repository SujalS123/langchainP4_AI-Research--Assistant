# Quick Setup Guide - AI Research Assistant

This guide will help you set up and run the simplified AI Research Assistant backend.

## Step 1: Get Google API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your API key

## Step 2: Backend Setup

### Windows

```powershell
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
@"
GOOGLE_API_KEY=your_api_key_here
DEFAULT_MODEL=gemini-pro
DEFAULT_TEMPERATURE=0.7
DEBUG=True
"@ | Out-File -FilePath .env -Encoding UTF8

# Edit the .env file and replace 'your_api_key_here' with your actual API key
notepad .env
```

### Linux/Mac

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
GOOGLE_API_KEY=your_api_key_here
DEFAULT_MODEL=gemini-pro
DEFAULT_TEMPERATURE=0.7
DEBUG=True
EOF

# Edit the .env file and replace 'your_api_key_here' with your actual API key
nano .env
```

## Step 3: Run the Server

```bash
# Make sure you're in the backend directory with virtual environment activated
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see output like:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Step 4: Test the API

### Option 1: Using curl (Terminal)

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"What is 2 + 2?\"}"
```

### Option 2: Using Python

Create a file `test_api.py`:

```python
import requests
import json

# Test simple math
response = requests.post(
    "http://localhost:8000/api/query",
    json={"query": "What is 25 multiplied by 4?"}
)
print("Math Test:")
print(json.dumps(response.json(), indent=2))
print("\n" + "="*50 + "\n")

# Test search
response = requests.post(
    "http://localhost:8000/api/query",
    json={"query": "What is the capital of France?"}
)
print("Search Test:")
print(json.dumps(response.json(), indent=2))
```

Run it:
```bash
python test_api.py
```

### Option 3: Using Postman or Insomnia

1. Create a new POST request
2. URL: `http://localhost:8000/api/query`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
```json
{
  "query": "What is the population of Tokyo?"
}
```

## Step 5: View API Documentation

Open your browser and go to:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Common Issues

### Issue: "No module named 'app'"

**Solution**: Make sure you're in the `backend` directory and your virtual environment is activated.

### Issue: "GOOGLE_API_KEY must be set"

**Solution**: 
1. Check if `.env` file exists in the `backend` directory
2. Verify the API key is correctly set in `.env`
3. Make sure there are no extra spaces or quotes around the key

### Issue: "Address already in use"

**Solution**: Another process is using port 8000. Either:
- Stop the other process
- Use a different port: `uvicorn app.main:app --reload --port 8001`

### Issue: DuckDuckGo search fails

**Solution**: DuckDuckGo may have rate limits. Wait a few minutes and try again.

## What's Simplified?

Compared to the original complex structure, this simplified version:

✅ **Single Service File**: All agent logic in `langchain_service.py`
- No separate files for agent, chains, llm_config
- No tools subdirectory with stub files

✅ **Minimal Dependencies**: Only what's needed
- Removed unused packages
- Added proper version numbers

✅ **Clear Structure**: Easy to understand and extend
- Each file has a clear purpose
- No circular imports
- Well-documented code

✅ **Production-Ready Patterns**: But kept simple
- Proper configuration management
- Error handling
- Type hints with Pydantic

## Next Steps

1. ✅ Backend is running
2. ⏳ Build the frontend
3. ⏳ Test the complete flow
4. ⏳ Deploy (optional)

## Understanding the Code

### Flow of a Query

1. **Request arrives** at `app/main.py` (FastAPI app)
2. **Routed** to `app/routes/query_router.py`
3. **Processed** by `app/services/langchain_service.py`:
   - Creates LLM (Gemini)
   - Creates tools (Search, Calculator)
   - Initializes agent
   - Runs agent with query
4. **Response** sent back to client

### Key Files

- `app/main.py`: FastAPI app setup, CORS, routes
- `app/config.py`: Configuration and environment variables
- `app/routes/query_router.py`: API endpoint definition
- `app/services/langchain_service.py`: Core AI logic
- `app/models/request_models.py`: Request/response schemas

## Tips for Development

1. **Keep the terminal open** to see agent reasoning (verbose=True)
2. **Test incrementally** - try simple queries first
3. **Check logs** - the agent shows its decision-making process
4. **Use the docs** - FastAPI auto-generates API documentation

Happy coding! 🚀
