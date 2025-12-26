# AI-Powered PDD Generator

An AI-powered application that generates UiPath-standard Process Design Documents (PDDs) from text descriptions using OpenAI's GPT-4o.

## Features (Phase 1 - MVP)

- Text-based process description input
- Automated extraction of PDD sections using GPT-4o:
  - Process Name
  - Process Description
  - Actors & Systems
  - Input Data
  - Output Data
  - Detailed Process Steps
  - Business Rules & Exceptions
- Clean, responsive web interface
- Print/Save as PDF functionality

## Prerequisites

- **Python 3.11+**
- **Node.js 18+** (for the frontend)
- **OpenAI API Key** - Get one from [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

## Installation & Setup

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a Python virtual environment:**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

5. **Start the backend server:**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

   The API will be available at `http://localhost:8000`
   - API docs: `http://localhost:8000/docs`
   - Health check: `http://localhost:8000/health`

### Frontend Setup

1. **Navigate to the frontend directory (in a new terminal):**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

   The application will be available at `http://localhost:5173`

## Usage

1. Open `http://localhost:5173` in your browser
2. Enter a process description in the text area. For example:
   ```
   The invoice processing process begins when an invoice is received via email.
   The finance clerk opens the email attachment and verifies the invoice amount
   against the purchase order. If the amount is correct and under $1000, they
   approve it for payment. If the amount is over $1000, manager approval is
   required. Once approved, the invoice is entered into the ERP system and
   marked for payment.
   ```
3. Click "Generate PDD"
4. View the generated PDD document
5. Use "Print / Save as PDF" to export

## Project Structure

```
AutoPDDGeneration/
├── backend/
│   ├── main.py                      # FastAPI application entry point
│   ├── requirements.txt             # Python dependencies
│   ├── .env.example                 # Environment variables template
│   └── app/
│       ├── api/
│       │   └── endpoints.py         # API endpoints (/generate-pdd)
│       ├── agents/
│       │   └── text_agent.py        # GPT-4o text processing logic
│       ├── core/
│       │   └── pdd_structure.yaml   # PDD section definitions
│       └── templates/
│           └── pdd_template.html    # Jinja2 template for PDD rendering
│
└── frontend/
    ├── src/
    │   ├── App.jsx                  # Main React component
    │   └── App.css                  # Component styles
    ├── vite.config.js               # Vite configuration with proxy
    └── package.json                 # Node dependencies
```

## Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **LangChain** - LLM integration framework
- **OpenAI GPT-4o** - AI model for text processing
- **Jinja2** - Template engine for HTML generation

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Axios** - HTTP client

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/generate-pdd` | Generate PDD from text (expects `{"process_text": "..."}`) |
| GET | `/health` | Health check endpoint |
| GET | `/` | API root with documentation links |

## Roadmap

- **Phase 2**: Multi-modal input support (PDF, Word, video files)
- **Phase 3**: Diagram generation (Mermaid.js flowcharts), interactive review
- **Phase 4**: Authentication, Docker deployment, UiPath export

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'langchain_openai'`
- **Solution**: Make sure you activated the virtual environment and ran `pip install -r requirements.txt`

**Problem**: OpenAI API errors
- **Solution**: Verify your API key in `backend/.env` is correct and has credits

### Frontend Issues

**Problem**: Frontend can't connect to backend
- **Solution**: Make sure the backend is running on `http://localhost:8000`

**Problem**: CORS errors
- **Solution**: The Vite proxy should handle this. Verify `vite.config.js` has the proxy configuration.

## License

MIT
