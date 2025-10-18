# AI Research Assistant

A sophisticated AI Research Assistant powered by LangChain chains, Google Gemini AI, FastAPI backend, and React frontend with beautiful pastel aesthetics. This assistant demonstrates modern AI application development with intelligent query routing, multi-tool processing, and chain-based reasoning.

## 🎯 Project Overview

This project showcases a complete AI research assistant with production-ready architecture:

- **🤖 Google Gemini 2.0 Flash Experimental** (via LangChain)
- **🔍 DuckDuckGo Search Integration** (for web searches)
- **🔗 Advanced LangChain Chains** (intelligent processing & routing)
- **⚡ FastAPI Backend** (async API with proper error handling)
- **🎨 React Frontend** (beautiful pastel design with smooth animations)
- **🐳 Docker Support** (complete containerized deployment)
- **🗄️ PostgreSQL & Redis** (database and caching infrastructure)

## 🚀 Key Features Implemented

### AI Capabilities
- ✅ **Intelligent Query Routing** - Automatically detects query type and selects appropriate processing chains
- ✅ **Multi-Chain Processing** - Q&A, Research, Math, Reasoning, and Summary chains
- ✅ **Tool Integration** - Web search, calculator, and reasoning tools
- ✅ **Parallel Chain Execution** - Runs multiple chains simultaneously for comprehensive analysis
- ✅ **Context-Aware Responses** - Uses search results for up-to-date information

### Backend Features
- ✅ **LangChain LCEL Implementation** - Modern LangChain Expression Language patterns
- ✅ **Async FastAPI** - High-performance async API endpoints
- ✅ **Structured Error Handling** - Graceful fallbacks and error recovery
- ✅ **Configuration Management** - Environment-based configuration
- ✅ **API Documentation** - Auto-generated Swagger/ReDoc docs

### Frontend Features
- ✅ **Beautiful Pastel UI** - Modern design with glass morphism effects
- ✅ **Responsive Layout** - Works perfectly on all devices
- ✅ **Smooth Animations** - Micro-interactions and transitions
- ✅ **Tool Visualization** - See which AI tools were used
- ✅ **Copy & Print** - Easy sharing of research results

### DevOps Features
- ✅ **Docker Compose Setup** - Complete containerized deployment
- ✅ **Database Integration** - PostgreSQL with Redis caching
- ✅ **Production Configuration** - Environment-based settings
- ✅ **Comprehensive Testing** - Test suites for all components

## 📁 Enhanced Project Structure

```
AI Research Assistant/
│
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── main.py                   # FastAPI app entry point
│   │   ├── config.py                 # Configuration & settings
│   │   ├── routes/
│   │   │   ├── query_router.py       # Main API endpoint: POST /api/query
│   │   │   └── admin_router.py       # Admin endpoints
│   │   ├── services/
│   │   │   ├── langchain_service.py  # Main LangChain service with chains
│   │   │   ├── chains.py             # LangChain chains definitions
│   │   │   ├── llm_config.py         # LLM configuration
│   │   │   └── enhanced_search_service.py # Enhanced search capabilities
│   │   ├── models/
│   │   │   └── request_models.py     # Pydantic request/response models
│   │   └── .env.example              # Environment template
│   ├── requirements.txt              # Python dependencies with versions
│   ├── test_langchain.py             # Comprehensive test suite
│   ├── Dockerfile                    # Docker configuration
│   └── .env                          # Environment variables (API keys)
│
├── frontend/                         # React Frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── QueryInput.jsx        # Beautiful query input component
│   │   │   └── AgentTimeline.jsx     # Results display with pastel design
│   │   ├── utils/
│   │   │   ├── api.js                # API communication utilities
│   │   │   └── textFormatter.js      # Text formatting utilities
│   │   ├── App.jsx                   # Main app with gradient background
│   │   └── index.jsx                 # React entry point
│   ├── tailwind.config.js            # Custom pastel color palette
│   ├── package.json                  # Dependencies and scripts
│   └── Dockerfile                    # Frontend Docker configuration
│                  
│
├── docker-compose.yml                # Complete multi-service deployment
├── LANGCHAIN_IMPLEMENTATION_SUMMARY.md # Detailed LangChain documentation
├── SETUP_GUIDE.md                    # Step-by-step setup instructions
├── SIMPLIFICATION_SUMMARY.md         # Architecture decisions
└── README.md                         # This file
```

## 🧠 LangChain Implementation Details

### Architecture Overview

This project uses LangChain's modern LCEL (LangChain Expression Language) approach with intelligent chain selection and parallel processing capabilities.

### 1. Core Components

#### LLM Configuration (`backend/app/services/llm_config.py`)
```python
# Google Gemini 2.0 Flash Experimental model
gemini_flash = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    temperature=0.2,
    max_tokens=1000
)
```

#### Advanced Chain Types (`backend/app/services/chains.py`)

**Q&A Chain** - Simple question-answering
```python
qa_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI research assistant. Provide accurate, concise answers."),
    ("human", "{question}")
])
qa_chain = qa_template | llm | StrOutputParser()
```

**Research Chain** - Context-aware research with search integration
```python
research_template = ChatPromptTemplate.from_messages([
    ("system", "Using the provided search results, provide comprehensive, up-to-date answers."),
    ("human", "Search Results: {search_context}\nQuestion: {question}")
])
research_chain = research_template | pro_llm | StrOutputParser()
```

**Math Chain** - Mathematical problem solving with step-by-step explanations
```python
math_template = ChatPromptTemplate.from_messages([
    ("system", "You are a mathematical assistant. Solve problems step-by-step, showing your work."),
    ("human", "Solve: {math_expression}")
])
math_chain = math_template | llm | StrOutputParser()
```

**Reasoning Chain** - Multi-step analytical reasoning
```python
reasoning_template = ChatPromptTemplate.from_messages([
    ("system", "Break down complex questions into logical steps and provide detailed analysis."),
    ("human", "Question: {question}\nAnalyze step by step...")
])
reasoning_chain = reasoning_template | pro_llm | StrOutputParser()
```

**Summary Chain** - Content summarization and key point extraction
```python
summary_template = ChatPromptTemplate.from_messages([
    ("system", "Summarize the following content, extracting the most important information."),
    ("human", "Content to summarize: {content}")
])
summary_chain = summary_template | llm | StrOutputParser()
```

### 2. Intelligent Query Processing (`backend/app/services/langchain_service.py`)

#### Query Analysis & Routing
```python
def analyze_query_type(self, query: str) -> dict:
    """Intelligently analyze query and determine processing needs"""
    query_lower = query.lower()
    
    return {
        'needs_search': any(keyword in query_lower for keyword in [
            'search', 'find', 'latest', 'current', 'news', 'what is', 
            'who is', 'when was', 'recent', 'today', 'update'
        ]),
        'needs_math': any(char in query for char in ['+', '-', '*', '/', '=', 'calculate']),
        'needs_reasoning': any(keyword in query_lower for keyword in [
            'analyze', 'compare', 'explain', 'why', 'how', 'step by step'
        ])
    }
```

#### Tool Execution Pipeline
```python
async def execute_tools(self, query: str, analysis: dict) -> tuple:
    """Execute required tools and gather context"""
    context = ""
    tools_used = []
    
    if analysis['needs_search']:
        search_result = await self.perform_web_search(query)
        context += f"Search Results:\n{search_result}\n\n"
        tools_used.append("Search")
    
    if analysis['needs_math']:
        math_result = await self.calculate_math(query)
        context += f"Math Calculation:\n{math_result}\n\n"
        tools_used.append("Calculator")
    
    return context, tools_used
```

#### Intelligent Chain Selection
```python
async def select_and_execute_chain(self, query: str, context: str, analysis: dict):
    """Select appropriate chain based on query analysis"""
    
    if context and analysis['needs_search']:
        # Use research chain with search context
        chain = self.research_chains.get_research_chain()
        response = await chain.ainvoke({
            "search_context": context.strip(),
            "question": query
        })
    elif analysis['needs_reasoning']:
        # Use reasoning chain for complex analysis
        chain = self.research_chains.get_reasoning_chain()
        response = await chain.ainvoke({"question": query})
    elif analysis['needs_math']:
        # Use math chain for calculations
        chain = self.research_chains.get_math_chain()
        response = await chain.ainvoke({"math_expression": query})
    else:
        # Use Q&A chain for simple questions
        chain = self.research_chains.get_qa_chain()
        response = await chain.ainvoke({"question": query})
    
    return response
```

### 3. Parallel Chain Processing

```python
async def run_parallel_chains(self, query: str):
    """Run multiple chains simultaneously for comprehensive analysis"""
    parallel_chain = RunnableParallel(**{
        "qa_result": self.research_chains.get_qa_chain(),
        "reasoning_result": self.research_chains.get_reasoning_chain(),
        "summary_result": self.research_chains.get_summary_chain()
    })
    
    results = await parallel_chain.ainvoke({
        "question": query,
        "content": f"Question: {query}"
    })
    
    return {
        "comprehensive_answer": self.merge_results(results),
        "chains_used": ["Q&A", "Reasoning", "Summary"]
    }
```

### 4. Enhanced Web Search

```python
async def perform_web_search(self, query: str, max_results: int = 10) -> str:
    """Enhanced web search with better result processing"""
    try:
        # Use DuckDuckGo search with proper headers
        search_wrapper = DuckDuckGoSearchAPIWrapper(max_results=max_results)
        results = search_wrapper.run(query)
        
        # Process and format results
        formatted_results = self.format_search_results(results)
        return formatted_results
        
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return "Search temporarily unavailable. Please try again later."
```

### 5. Chain Orchestration Patterns

#### Sequential Processing
```python
def create_sequential_chain(self, chains: List[Runnable]) -> Runnable:
    """Create a sequential processing chain"""
    sequential_chain = chains[0]
    for chain in chains[1:]:
        sequential_chain = sequential_chain | chain
    return sequential_chain
```

#### Conditional Routing
```python
def create_conditional_chain(self):
    """Create conditional routing based on query analysis"""
    return RunnableBranch(
        (lambda x: x['needs_search'], self.research_chains.get_research_chain()),
        (lambda x: x['needs_math'], self.research_chains.get_math_chain()),
        (lambda x: x['needs_reasoning'], self.research_chains.get_reasoning_chain()),
        self.research_chains.get_qa_chain()  # Default
    )
```

## 🔄 Complete Request Flow

```mermaid
graph TD
    A[User Query] --> B[FastAPI Endpoint]
    B --> C[Query Analysis]
    C --> D{Needs Search?}
    D -->|Yes| E[DuckDuckGo Search]
    D -->|No| F{Needs Math?}
    F -->|Yes| G[Math Chain]
    F -->|No| H{Needs Reasoning?}
    H -->|Yes| I[Reasoning Chain]
    H -->|No| J[Q&A Chain]
    E --> K[Research Chain]
    G --> L[Math Processing]
    I --> M[Analytical Processing]
    J --> N[Simple Processing]
    K --> O[Response Formatting]
    L --> O
    M --> O
    N --> O
    O --> P[JSON Response]
    P --> Q[Frontend Display]
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- Docker & Docker Compose (optional)
- Google API Key (for Gemini)

### 🌐 **Live Demo (Production)**
- **Backend API**: https://langchainp4-ai-research-assistant.onrender.com
- **API Documentation**: https://langchainp4-ai-research-assistant.onrender.com/docs
- **Health Check**: https://langchainp4-ai-research-assistant.onrender.com/health

### Option 1: Docker Compose (Local Development)

```bash
# Clone and navigate to project
git clone <repository-url>
cd "AI Research Assistant"

# Create environment file
cp backend/.env.example backend/.env
# Edit backend/.env with your Google API key

# Start all services
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Manual Setup

#### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
echo GOOGLE_API_KEY=your_google_api_key_here > .env

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

### 🚀 **Production Deployment**

#### Backend Deployment (Render.com)
The backend is already deployed at: https://langchainp4-ai-research-assistant.onrender.com

To deploy your own backend:
1. Fork this repository
2. Connect to Render.com
3. Set your `GOOGLE_API_KEY` in Render dashboard
4. Deploy automatically from the `render.yaml` configuration

#### Frontend Deployment Options

**Option 1: Netlify**
```bash
# Build the frontend
cd frontend
npm run build

# Deploy to Netlify
# 1. Drag and drop the 'dist' folder to netlify.com
# 2. Or connect your GitHub repository to Netlify
# 3. The 'netlify.toml' file will handle configuration automatically
```

**Option 2: Vercel**
```bash
# Deploy to Vercel
# 1. Install Vercel CLI: npm i -g vercel
# 2. Run: vercel --prod
# 3. The 'vercel.json' file will handle configuration automatically
```

**Option 3: GitHub Pages**
```bash
# Build for GitHub Pages
cd frontend
npm run build

# Deploy using gh-pages
npm install -g gh-pages
gh-pages -d dist
```

### 🔗 **Connecting Frontend to Production Backend**

The frontend is already configured to connect to the deployed backend:
```javascript
// frontend/src/utils/api.js
const API_BASE_URL = 'https://langchainp4-ai-research-assistant.onrender.com';
```

To connect to your own backend:
1. Deploy your backend to Render.com
2. Update `API_BASE_URL` in `frontend/src/utils/api.js`
3. Redeploy the frontend

## 📝 API Documentation

### Main Endpoint: POST /api/query

Submit a research query to the AI assistant.

**Request Body:**
```json
{
  "query": "Your question here",
  "options": {
    "show_chain": true,
    "parallel_processing": false
  }
}
```

**Response:**
```json
{
  "status": "ok",
  "summary": "The AI's comprehensive response",
  "query": "Your original question",
  "tools_used": ["Search", "Calculator"],
  "chain_used": "Research Chain (with context)",
  "timeline": [
    {
      "step": 1,
      "tool": "Search",
      "output_summary": "Found relevant information..."
    },
    {
      "step": 2,
      "tool": "Research Chain",
      "output_summary": "Processed search results and generated response..."
    }
  ],
  "processing_time": 2.3,
  "model_used": "gemini-2.0-flash-exp"
}
```

### Admin Endpoint: GET /api/health

Check system health and status.

**Response:**
```json
{
  "status": "healthy",
  "model": "gemini-2.0-flash-exp",
  "services": {
    "search": "active",
    "math": "active",
    "reasoning": "active"
  },
  "uptime": "2h 34m"
}
```

## 🎨 Frontend Design System

### Color Palette
- **Pastel Pink**: `#FFD6E0`
- **Pastel Blue**: `#D6E5FF`
- **Pastel Purple**: `#E6D6FF`
- **Pastel Mint**: `#D6FFF5`
- **Pastel Lavender**: `#F0E6FF`

### Design Features
- **Glass Morphism**: Semi-transparent backgrounds with backdrop blur
- **Gradient Backgrounds**: Smooth color transitions
- **Rounded Corners**: Soft, modern aesthetics
- **Micro-interactions**: Hover states and smooth transitions
- **Responsive Design**: Mobile-first approach

### Components
- **QueryInput**: Beautiful input with auto-focus and validation
- **AgentTimeline**: Step-by-step visualization of AI processing
- **ToolIndicators**: Visual representation of tools used
- **CopyButton**: Easy copying of results
- **PrintButton**: Optimized printing formatting

## 🎓 Example Queries & Chain Usage

### Simple Q&A (Q&A Chain)
- "What is artificial intelligence?"
- "Who won the Nobel Prize in Physics in 2023?"
- **Chain Used**: Q&A Chain
- **Processing**: Direct model response

### Search-Required (Research Chain)
- "What are the latest developments in quantum computing?"
- "Current population of Tokyo"
- **Chain Used**: Research Chain + Search Tool
- **Processing**: Web search → Context analysis → Response generation

### Mathematical (Math Chain)
- "Calculate 25 * 4 + 10"
- "What is 15% of 250?"
- **Chain Used**: Math Chain
- **Processing**: Expression parsing → Step-by-step calculation

### Complex Reasoning (Reasoning Chain)
- "Compare renewable energy sources and their efficiency"
- "Analyze the impact of AI on job markets"
- **Chain Used**: Reasoning Chain
- **Processing**: Multi-step analysis → Logical breakdown → Comprehensive answer

### Multi-Tool (Multiple Chains)
- "What is the population of India and what is 25 * 4?"
- **Chains Used**: Research Chain + Math Chain
- **Processing**: Parallel tool execution → Result synthesis

### Parallel Processing (All Chains)
- "Provide comprehensive analysis of renewable energy benefits"
- **Chains Used**: Q&A + Reasoning + Summary (Parallel)
- **Processing**: Simultaneous chain execution → Result merging

## 🔧 Configuration

### Environment Variables

Edit `backend/.env` or `backend/app/.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google Gemini API key (required) | None |
| `DEFAULT_MODEL` | Gemini model to use | gemini-2.0-flash-exp |
| `DEFAULT_TEMPERATURE` | Model temperature (0-1) | 0.2 |
| `MAX_SEARCH_RESULTS` | Max search results | 10 |
| `DEBUG_MODE` | Enable debug logging | False |
| `REDIS_URL` | Redis connection string | redis://localhost:6379 |
| `DATABASE_URL` | PostgreSQL connection | postgresql://user:pass@localhost/research_db |

### Model Configuration

```python
# backend/app/services/llm_config.py
MODEL_CONFIGS = {
    "gemini-2.0-flash-exp": {
        "temperature": 0.2,
        "max_tokens": 1000,
        "timeout": 30
    },
    "gemini-pro": {
        "temperature": 0.3,
        "max_tokens": 2000,
        "timeout": 45
    }
}
```

## 🧪 Testing

### Backend Tests

```bash
# Run LangChain tests
cd backend
python test_langchain.py

# Run API tests
python test_backend.py

# Run with coverage
pytest --cov=app tests/
```

### Frontend Tests

```bash
cd frontend
npm test
npm run test:coverage
```

### Integration Tests

```bash
# Test complete flow
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"What is 25 * 4?\"}"
```

## 🐛 Troubleshooting

### Common Issues

**Issue**: `GOOGLE_API_KEY must be set`
- **Solution**: Create `.env` file in backend directory with valid API key

**Issue**: Frontend not connecting to backend
- **Solution**: Ensure backend is running on `http://localhost:8000` and check CORS settings

**Issue**: Search not working
- **Solution**: DuckDuckGo may have rate limits; wait and try again

**Issue**: Math calculations failing
- **Solution**: Verify mathematical expression syntax and operators

**Issue**: Docker container not starting
- **Solution**: Check Docker logs: `docker-compose logs backend`

### Debug Mode

Enable debug logging by setting `DEBUG_MODE=True` in `.env`:

```bash
# See detailed chain processing
export DEBUG_MODE=True
uvicorn app.main:app --reload
```

## 📊 Performance Metrics

### Chain Performance
- **Q&A Chain**: ~1-2 seconds
- **Research Chain**: ~3-5 seconds (includes search)
- **Math Chain**: ~1-2 seconds
- **Reasoning Chain**: ~2-4 seconds
- **Parallel Chains**: ~3-5 seconds (all chains)

### Resource Usage
- **Memory**: ~200-500MB (depending on query complexity)
- **CPU**: Moderate during chain processing
- **Network**: Required for web searches

## 🔜 Future Enhancements

### Planned Features
- [ ] **Conversation Memory** - Session-based context retention
- [ ] **Advanced Tools** - Wikipedia, web scraping, image analysis
- [ ] **Streaming Responses** - Real-time response streaming
- [ ] **User Authentication** - Personalized experiences
- [ ] **Advanced Visualizations** - Charts and graphs
- [ ] **Voice Input/Output** - Speech-to-text and text-to-speech
- [ ] **Mobile App** - React Native implementation
- [ ] **Cloud Deployment** - AWS/GCP/Azure deployment guides

### Technical Improvements
- [ ] **Vector Database** - Semantic search capabilities
- [ ] **Caching Layer** - Redis-based response caching
- [ ] **Rate Limiting** - API usage management
- [ ] **Monitoring** - Performance and error tracking
- [ ] **A/B Testing** - Chain performance comparison

## 📄 Architecture Decisions

### Why LangChain LCEL?
- **Modern Syntax**: Cleaner, more readable chain definitions
- **Better Performance**: Optimized execution patterns
- **Type Safety**: Improved error handling and debugging
- **Flexibility**: Easy to modify and extend chains

### Why Chain-Based Architecture?
- **Modularity**: Each chain has a specific responsibility
- **Testability**: Individual chains can be tested in isolation
- **Maintainability**: Easy to add new chain types
- **Performance**: Parallel processing capabilities

### Why Gemini 2.0 Flash Experimental?
- **Speed**: Faster response times
- **Quality**: High-quality reasoning capabilities
- **Cost**: More cost-effective than larger models
- **Features**: Latest AI capabilities

## 🤝 Contributing

### Development Guidelines
1. **Follow the existing code style** (Python: PEP 8, JavaScript: ESLint)
2. **Add tests for new features** (pytest for backend, Jest for frontend)
3. **Update documentation** (README, API docs, comments)
4. **Create pull requests** with clear descriptions

### Code Structure
- **Backend**: Follow FastAPI best practices
- **Frontend**: Use React hooks and functional components
- **Chains**: Keep chains focused and single-purpose
- **Tests**: Aim for >80% coverage

## 📄 License

This is a learning project for educational purposes. Feel free to fork, modify, and learn from it.

## 🙏 Acknowledgments

- **LangChain** - For the powerful chain-based AI framework
- **Google** - For the Gemini AI model
- **FastAPI** - For the modern, fast web framework
- **React** - For the beautiful frontend framework
- **DuckDuckGo** - For providing search API access

---

**Note**: This project demonstrates modern AI application development with LangChain, showcasing best practices in chain architecture, intelligent query routing, error handling, and user experience design. The implementation is production-ready while remaining simple enough for learning and extension.
