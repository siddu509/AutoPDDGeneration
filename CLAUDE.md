# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an **AI-powered UiPath Process Design Document (PDD) Generator** - a full-stack application that automates the creation of professional RPA documentation from multiple input sources (text descriptions, PDF/Word documents, and video recordings).

**Current Status**: This repository contains **implementation specifications only** - no production code exists yet. The `Process.md` file contains detailed prompts for implementing the system in phases.

## Intended Architecture

The system follows a **4-layer architecture**:

1. **Frontend**: React web application with Material-UI for user interaction
2. **Backend API**: FastAPI (Python) service orchestrating the workflow
3. **Agent Orchestrator**: Routes inputs to specialized AI agents based on type
4. **AI Model Layer**: OpenAI API (GPT-4o, Whisper) and LangChain for processing

### Agent Architecture

The system uses a **multi-agent pattern** where specialized agents handle different input types:

- **Text Agent**: Processes text descriptions using GPT-4o
- **Video Agent**: Transcribes audio (Whisper), analyzes frames (GPT-4o vision), and synthesizes into step-by-step guide
- **Diagram Agent**: Converts process steps into Mermaid.js flowchart syntax
- **Logic Agent**: Identifies decision points and exception handling paths

## Development Phases

The implementation plan is structured in 4 phases (see `Process.md` for detailed prompts):

1. **Phase 1 - Foundation (MVP)**: Text input only, basic PDD generation
2. **Phase 2 - Multi-Modal Input**: Add PDF/Word parsing and video processing
3. **Phase 3 - Advanced Features**: Diagram generation, interactive review, AI refinement
4. **Phase 4 - Production**: Authentication, Docker, CI/CD, UiPath export

## Technology Stack

### Backend (Python)
- **Framework**: FastAPI with Uvicorn server
- **AI/ML**: LangChain, OpenAI (gpt-4o, whisper-1)
- **Document Processing**: python-docx, pypdf, ffmpeg-python
- **Templating**: Jinja2 for HTML PDD generation
- **Future**: python-jose (JWT), passlib (auth)

### Frontend (React)
- **Framework**: React with JavaScript/TypeScript
- **UI Library**: Material-UI
- **HTTP Client**: axios
- **Diagramming**: Mermaid.js for flowcharts
- **Build Tool**: npx create-react-app (or Vite)

## Key Technical Patterns

### Video Processing Pipeline

Video files undergo a three-stage analysis:

1. **Audio Transcription**: ffmpeg extracts audio → Whisper API transcribes with timestamps
2. **Frame Analysis**: ffmpeg extracts frames (1 per 3-5 seconds) → GPT-4o vision analyzes each frame for UI actions
3. **Synthesis**: GPT-4o combines transcript + visual analysis into coherent step-by-step guide

### Template-Based PDD Generation

The system uses a **YAML-defined PDD structure** (`pdd_structure.yaml`) where each section has:
- A `name` for the section heading
- A `prompt` that guides the LLM on what to extract

The Jinja2 template (`pdd_template.html`) renders the extracted content. This approach makes the system extensible - adding new PDD sections only requires YAML updates.

### Agent Routing Pattern

The `/upload-and-process` endpoint acts as a router:
- `.mp4`, `.mov` → Video Agent (transcribe → analyze frames → synthesize)
- `.pdf`, `.docx` → Document Parser (text extraction) → Text Agent
- Plain text → Text Agent directly

All paths converge on the same PDD generation pipeline.

## Project Structure (Planned)

```
/pdd-generator
├── /backend
│   ├── main.py                    # FastAPI app entry point
│   ├── requirements.txt
│   └── /app
│       ├── /api
│       │   └── endpoints.py       # API endpoints (/generate-pdd, /upload-and-process, etc.)
│       ├── /agents
│       │   ├── text_agent.py      # Text processing with GPT-4o
│       │   ├── video_agent.py     # Video transcription & analysis
│       │   └── diagram_agent.py   # Mermaid diagram generation
│       ├── /core
│       │   └── pdd_structure.yaml # PDD section definitions
│       ├── /templates
│       │   └── pdd_template.html  # Jinja2 template
│       └── /utils
│           └── file_parser.py     # PDF/Word parsing
│
├── /frontend
│   ├── /src
│   │   ├── App.js
│   │   └── /components
│   └── package.json
│
└── README.md
```

## Environment Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npx create-react-app .
npm install axios @mui/material @emotion/react @emotion/styled mermaid
npm start
```

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/generate-pdd` | POST | Accepts `{"process_text": "..."}`, returns rendered HTML PDD |
| `/upload-and-process` | POST | Accepts multipart file upload, routes to appropriate agent |
| `/refine-section` | POST | AI-rewrites PDD section based on user feedback |
| `/chat` | POST | Conversational interface for PDD clarification |
| `/export-pdd/{format}` | GET | Exports PDD as JSON or Excel (Phase 4) |
| `/register`, `/login` | POST | JWT authentication (Phase 4) |

## OpenAI API Requirements

The system requires these OpenAI models:
- **gpt-4o**: Main text processing, vision analysis for video frames
- **whisper-1**: Audio transcription from videos

Set the `OPENAI_API_KEY` environment variable before running the backend.

## Important Implementation Notes

1. **Video Frame Extraction Strategy**: Extract 1 frame every 3-5 seconds. This balances detail vs. API costs. The vision prompt should focus on: "What is being clicked? What data is being typed? What is being selected?"

2. **Mermaid.js Rendering**: The diagram agent outputs ONLY raw Mermaid code (no markdown formatting). Frontend must initialize Mermaid and render the code dynamically.

3. **CORS Configuration**: Backend must allow CORS for `http://localhost:3000` (or appropriate frontend URL).

4. **File Handling**: Uploaded files should be stored temporarily and cleaned up after processing to avoid disk space issues.

5. **Error Handling**: All LLM API calls should be wrapped in try-except blocks with meaningful error messages returned to the frontend.

## Reference Documentation

- **Process.md**: Comprehensive 467-line implementation guide with detailed LLM prompts for each phase
- **process-gemini.md**: High-level 36-line overview focused on Gemini 1.5 Pro integration

When implementing features, reference `Process.md` which contains exact prompts to use with LLM coding agents.
