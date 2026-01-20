# AI-Powered UiPath PDD Generator - Complete Technical Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Backend Components](#backend-components)
4. [Frontend Components](#frontend-components)
5. [Data Flow](#data-flow)
6. [API Endpoints](#api-endpoints)
7. [Agent System](#agent-system)
8. [Security Components](#security-components)
9. [Configuration & Deployment](#configuration--deployment)

---

## Component Overview

This section provides a quick reference for all the technologies and components used in the PDD Generator, explained in simple terms.

### 🎨 Frontend Components (What Users See)

**What is Frontend?**
The frontend is the **user interface** - what users see and interact with in their browser. Think of it like the display screen and buttons on an ATM machine.

| Component | What It Does | Why It's Used |
|-----------|--------------|---------------|
| **React** | Manages UI components and their interactions | Makes it easy to build interactive, reusable pieces like forms and buttons |
| **Vite** | Runs the React app during development, reloads when code changes | Fast development experience - see changes instantly |
| **Axios** | Sends requests from frontend to backend and receives responses | Easier and more powerful than browser's built-in fetch API |
| **Mermaid.js** | Turns text code into visual diagrams | Draws flowcharts showing process steps automatically |
| **DOMPurify** | Cleans HTML to remove dangerous code | Security - prevents malicious scripts (XSS attacks) |

---

### ⚙️ Backend Components (The Server-Side Logic)

**What is Backend?**
The backend is the **server-side** of the application - the part users don't see but does all the work. Think of it like the kitchen in a restaurant: customers don't see it, but that's where all the food preparation happens.

| Component | What It Does | Why It's Used |
|-----------|--------------|---------------|
| **FastAPI** | Handles HTTP requests and returns responses | Fast, modern Python framework with automatic API documentation |
| **Uvicorn** | Web server that runs the Python application | FastAPI requires this type of server to run |
| **Pydantic** | Validates that incoming data has correct format | Prevents errors from bad data, provides clear error messages |
| **Jinja2** | Combines HTML templates with data to create final documents | Reusable templates with placeholders for AI-generated content |
| **LangChain** | Manages interactions with OpenAI's GPT models | Simplifies working with AI, handles prompts and responses |

---

### 🤖 AI Services (The Intelligence)

| Component | What It Does | Why It's Used |
|-----------|--------------|---------------|
| **GPT-4o** | Understands process descriptions and generates PDD content | Best AI model for understanding context and writing professional documentation |
| **Whisper API** | Transcribes audio from video files into text | Converts spoken explanations in videos into text that GPT-4o can process |

---

### 📄 Document Processing Libraries

| Component | What It Does | Why It's Used |
|-----------|--------------|---------------|
| **python-docx** | Creates and edits Microsoft Word (.docx) files | Exports PDDs as Word documents with proper formatting |
| **pypdf** | Reads and extracts text from PDF files | Allows users to upload PDFs as input for PDD generation |

---

### 🏗️ Architecture Patterns (How Code Is Organized)

| Pattern | What It Does | Why It's Used |
|---------|--------------|---------------|
| **Service Layer** | Separates business logic from API endpoints | Makes code easier to test, maintain, and reuse |
| **Agent System** | Different components handle different tasks (text, video, diagrams) | Clean separation - each component does one thing well |
| **Middleware** | Functions that run before/after requests (logging, rate limiting) | Applies features globally without repeating code |

---

### 🔒 Security Components (Protection)

| Component | What It Does | Why It's Used |
|-----------|--------------|---------------|
| **Rate Limiting (slowapi)** | Limits how many requests a user can make | Protects against API abuse and ensures fair usage |
| **CORS Middleware** | Allows frontend on one port to talk to backend on another | Browsers block cross-port requests by default for security |
| **Input Validation (Pydantic)** | Checks that incoming data is correct | Prevents crashes and security issues from bad data |

---

### ⚙️ Configuration System (Settings)

| Component | What It Does | Why It's Used |
|-----------|--------------|---------------|
| **Environment Variables (.env)** | Stores sensitive data like API keys outside code | Keeps secrets safe, allows different settings for dev/production |
| **config.yaml** | Central file with all application settings | Single place to manage settings without changing code |

---

### 🚀 Deployment Components (Going Live)

| Component | What It Does | Why It's Used |
|-----------|--------------|---------------|
| **Docker** | Packages app with all dependencies into a container | Ensures app runs the same everywhere (dev, staging, production) |
| **nginx** | Web server that serves the React frontend in production | Fast, efficient, handles HTTPS and caching |
| **docker-compose** | Runs multiple containers together (frontend + backend) | Simplifies running full-stack app locally and in production |

---

## System Overview

### Purpose
The AI-Powered PDD Generator is a full-stack web application that automates the creation of Process Design Documents (PDDs) for Robotic Process Automation (RPA) projects. It accepts multiple input types (text, PDF, Word documents, and videos) and uses LLM and STT models to generate structured, professional documentation with interactive editing capabilities.

### Key Features
- **Multi-modal Input Support**: Text, PDF, DOCX, MP4, MOV, AVI
- **AI-Powered Generation**: Uses GPT-4o for text processing and diagram generation
- **Video Transcription**: Uses Whisper API for audio-to-text conversion
- **Interactive Editing**: Real-time section editing with AI refinement
- **Visual Diagrams**: Automatic Mermaid.js flowchart generation
- **Export Options**: HTML, Word (DOCX), and PDF export
- **Modern UI**: Responsive React-based interface with blue theme

### Technology Stack Summary
| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React 18, Vite, Axios | User interface and API communication |
| **Backend** | FastAPI, Uvicorn, Python 3.11+ | RESTful API and business logic |
| **AI/ML** | LangChain, OpenAI (GPT-4o, Whisper) | Content generation and transcription |
| **Document Processing** | python-docx, pypdf | File parsing |
| **Diagramming** | Mermaid.js | Flowchart visualization |
| **Templating** | Jinja2 | HTML template rendering |
| **Styling** | CSS3 (custom) | UI styling with blue gradient theme |

---

## Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                 │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (React)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   App.jsx    │  │ PDDSection   │  │DiagramViewer │      │
│  │              │  │   .jsx       │  │    .jsx      │      │
│  │  - Main UI   │  │              │  │              │      │
│  │  - State Mgmt│  │  - Editing   │  │  - Mermaid   │      │
│  │  - API Calls │  │  - AI Refine │  │  - Rendering │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/JSON
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                         │
│  ┌───────────────────────────────────────────────────┐     │
│  │              main.py (Application Entry)           │     │
│  │  - FastAPI App Initialization                      │     │
│  │  - CORS Configuration                              │     │
│  │  - Router Registration                             │     │
│  └───────────────────────────────────────────────────┘     │
│                           │                                 │
│  ┌────────────────────────▼───────────────────────────┐     │
│  │         endpoints.py (API Router)                   │     │
│  │  - Request/Response Handling                        │     │
│  │  - File Upload Management                           │     │
│  │  - Agent Orchestration                              │     │
│  │  - Export Functionality                             │     │
│  └──────────────┬──────────────────────────────────────┘     │
│                 │                                            │
│  ┌──────────────▼──────────────────────────────────────┐     │
│  │              AGENTS LAYER                            │     │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────┐  │     │
│  │  │  Text Agent  │  │ Video Agent  │  │ Diagram │  │     │
│  │  │              │  │              │  │  Agent  │  │     │
│  │  │  - GPT-4o    │  │  - Whisper   │  │         │  │     │
│  │  │  - Sections  │  │  - Synthesis │  │- Mermaid│  │     │
│  │  └──────────────┘  └──────────────┘  └─────────┘  │     │
│  └───────────────────────────────────────────────────┘     │
│                 │                                            │
│  ┌──────────────▼──────────────────────────────────────┐     │
│  │            UTILITIES & TEMPLATES                     │     │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────┐  │     │
│  │  │ file_parser  │  │    pdd_      │  │  pdd_   │  │     │
│  │  │    .py       │  │ structure    │  │ template│  │     │
│  │  │              │  │    .yaml     │  │  .html  │  │     │
│  │  │  - PDF/DOCX  │  │              │  │         │  │     │
│  │  │  - Text Ext. │  │  - Sections  │  │  - Jinja2│  │     │
│  │  └──────────────┘  └──────────────┘  └─────────┘  │     │
│  └───────────────────────────────────────────────────┘     │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   EXTERNAL SERVICES                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  OpenAI API  │  │   Whisper    │  │   File Sys.  │      │
│  │              │  │     API      │  │              │      │
│  │  - GPT-4o    │  │              │  │  - Temp Files│      │
│  │  - LangChain │  │  - Audio     │  │  - Uploads   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## Backend Components

### Understanding the Backend

The **backend** is the **server-side** of the application - the part users don't see but does all the work. Think of it like the kitchen in a restaurant:

- **Frontend** = Dining area where customers sit (what users see)
- **Backend** = Kitchen where food is prepared (where the work happens)

When you click "Generate PDD" in the frontend, it sends a request to the backend. The backend processes your request using AI, then sends back the generated PDD document.

### Key Backend Technologies

#### FastAPI - The Web Framework
**What is it?**
FastAPI is a **Python framework** for building web APIs (Application Programming Interfaces). It's like a toolkit that makes it easy to create web servers.

**What it does in PDD Generator**
- Listens for incoming requests from the React frontend
- Routes each request to the right function (generate PDD, upload file, etc.)
- Validates incoming data
- Returns responses in JSON format
- Automatically generates API documentation at `/docs`

**Why it's used here**
- **Fast**: Built on Python's async features, handles many requests efficiently
- **Easy**: Simple, clean code that's quick to write and understand
- **Auto-docs**: Generates interactive API documentation automatically
- **Modern**: Uses latest Python features and best practices

#### Uvicorn - The Web Server
**What is it?**
Uvicorn is a web server that runs Python web applications.

**What it does in PDD Generator**
- Listens for HTTP requests on port 8000
- Passes requests to FastAPI for processing
- Handles multiple connections at once

**Why it's used here**
- FastAPI requires an ASGI server like Uvicorn to run
- Very fast and efficient
- Supports async operations

#### Pydantic - Data Validation
**What is it?**
Pydantic is a library for validating and parsing data.

**What it does in PDD Generator**
- Checks that incoming requests have the correct data types
- Ensures required fields are present
- Provides clear error messages when data is invalid
- Automatically converts data to the right format

**Why it's used here**
- Prevents crashes from bad data
- Catches errors early with helpful messages
- Works seamlessly with FastAPI

#### Jinja2 - Template Engine
**What is it?**
Jinja2 is a template engine for creating HTML dynamically.

**What it does in PDD Generator**
- Combines HTML templates with AI-generated content
- Fills in placeholders with actual PDD data
- Creates the final HTML PDD document

**Why it's used here**
- Allows reusable HTML templates
- Clean separation of design and data
- Flexible and powerful

#### LangChain - AI Framework
**What is it?**
LangChain is a framework for working with AI language models (LLMs).

**What it does in PDD Generator**
- Manages interactions with OpenAI's GPT models
- Handles prompt engineering
- Processes AI responses
- Simplifies working with multiple AI calls

**Why it's used here**
- Makes working with AI much easier
- Provides consistent interface to different models
- Handles complex AI workflows

---

### 1. Application Entry Point (`main.py`)

**File:** `backend/main.py`

**Purpose:** Initializes and configures the FastAPI application.

**Class/Function Details:**

#### FastAPI Application Instance
```python
app = FastAPI(
    title="PDD Generator API",
    description="AI-powered Process Design Document Generator",
    version="1.0.0"
)
```
- Creates the main FastAPI application instance
- Configures API metadata for automatic documentation
- Accessible at `http://localhost:8000/docs` for Swagger UI

#### CORS Middleware Configuration
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
**Purpose:** Enables Cross-Origin Resource Sharing (CORS)

**Parameters:**
- `allow_origins`: Whitelisted frontend URLs (Vite dev server and Create React App)
- `allow_credentials`: Allows cookies and authorization headers
- `allow_methods`: All HTTP methods (GET, POST, PUT, DELETE, etc.)
- `allow_headers`: All HTTP headers

**Why Important:** Without this, the frontend (running on port 5173) cannot make requests to the backend (port 8000) due to browser security policies.

#### Router Registration
```python
app.include_router(endpoints.router, tags=["pdd"])
```
- Imports and registers all API endpoints from `app.api.endpoints`
- Tags all endpoints under the "pdd" category for API documentation organization

#### Root Endpoint
```python
@app.get("/")
async def root():
    return {
        "message": "PDD Generator API",
        "version": "1.0.0",
        "docs": "/docs"
    }
```
- Health check endpoint
- Returns API metadata
- Provides link to interactive API documentation

---

### 2. API Endpoints (`endpoints.py`)

**File:** `backend/app/api/endpoints.py`

**Purpose:** Defines all RESTful API endpoints for PDD generation, file upload, section refinement, and export functionality.

#### Pydantic Models (Request/Response Schemas)

**GeneratePDDRequest**
```python
class GeneratePDDRequest(BaseModel):
    process_text: str
```
- Validates incoming POST request body for text-based PDD generation
- Ensures `process_text` field is present and is a string

**ExportPDDRequest**
```python
class ExportPDDRequest(BaseModel):
    process_name: str
    sections: List[Dict[str, str]]
    diagram_code: Optional[str]
    format: str
```
- Validates export requests
- `process_name`: Title of the PDD
- `sections`: List of PDD sections with names and content
- `diagram_code`: Optional Mermaid diagram syntax
- `format`: Export format ('pdf', 'docx', or 'html')

#### API Endpoints

##### 1. Generate PDD from Text (HTML Response)
```python
@router.post("/generate-pdd", response_class=HTMLResponse)
async def generate_pdd(request: Request, body: GeneratePDDRequest)
```

**Purpose:** Generates a fully-rendered HTML PDD from text description.

**Input:**
- JSON body: `{"process_text": "invoice process description..."}`

**Process Flow:**
1. **HTML Tag Stripping**
   ```python
   process_name_clean = re.sub('<[^<]+?>', '', process_name).strip()
   ```
   - Removes HTML tags from the project name for clean title display

2. **Section Extraction**
   - Calls `extract_pdd_sections(body.process_text)`
   - Returns list of 15 sections with content

3. **Diagram Generation** (if ≥6 sections exist)
   - Extracts "Detailed Process Steps" (6th section)
   - Calls `generate_mermaid_diagram()` with process steps
   - Returns Mermaid.js syntax

4. **HTML Rendering**
   - Loads Jinja2 template (`pdd_template.html`)
   - Renders with: process_name, sections, diagram_code
   - Returns complete HTML document

**Output:** Rendered HTML page (displayed in browser)

**Use Case:** Quick PDD generation when user doesn't need interactive editing

---

##### 2. Upload and Process File (HTML Response)
```python
@router.post("/upload-and-process", response_class=HTMLResponse)
async def upload_and_process(request: Request, file: UploadFile)
```

**Purpose:** Handles file uploads (PDF, DOCX, video) and returns HTML PDD.

**Input:**
- `multipart/form-data` with file

**Process Flow:**
1. **File Validation**
   ```python
   file_extension = '.' + file.filename.split('.').pop().lower()
   if file_extension not in ['.pdf', '.docx', '.mp4', '.mov', '.avi']:
       raise HTTPException(status_code=400, detail="Unsupported file type")
   ```

2. **File Storage**
   - Saves uploaded file to temporary location using `tempfile`
   - Generates unique filename with UUID

3. **Content Extraction**
   - **Documents (PDF/DOCX):** Calls `parse_document(temp_file_path)`
   - **Videos:** Calls video processing pipeline:
     ```python
     transcript = transcribe_audio_from_video(temp_file_path)
     visual_actions = analyze_video_frames(temp_file_path, transcript)
     process_text = synthesize_video_analysis(transcript, visual_actions)
     ```

4. **PDD Generation**
   - Passes extracted text to `extract_pdd_sections()`
   - Generates diagram if applicable
   - Renders HTML template

5. **Cleanup**
   - Deletes temporary file
   - Returns rendered HTML

**Output:** Rendered HTML page

---

##### 3. Generate PDD from Text (JSON Response)
```python
@router.post("/api/generate-pdd-json")
async def generate_pdd_json(request: Request, body: GeneratePDDRequest)
```

**Purpose:** Same as `/generate-pdd` but returns structured JSON for interactive UI.

**Process Flow:** Identical to `/generate-pdd` but returns JSON:
```json
{
  "process_name": "Invoice Processing Automation",
  "sections": [
    {"name": "Project Name", "content": "<p>Invoice Processing...</p>"},
    ...
  ],
  "diagram_code": "graph TD\nA[Start]..."
}
```

**Use Case:** Interactive UI where sections need to be editable

---

##### 4. Upload and Process File (JSON Response)
```python
@router.post("/api/upload-and-process-json")
async def upload_and_process_json(request: Request, file: UploadFile)
```

**Purpose:** File upload endpoint that returns JSON for interactive UI.

**Process:** Same as `/upload-and-process` but returns JSON structure

---

##### 5. Refine PDD Section
```python
@router.post("/refine-section")
async def refine_section(request: Request, body: Dict[str, str])
```

**Purpose:** AI-powered section rewriting based on user feedback.

**Input:**
```json
{
  "section_name": "Purpose",
  "current_content": "<p>Current content...</p>",
  "user_feedback": "Make it more detailed"
}
```

**Process Flow:**
1. Constructs refinement prompt:
   ```python
   refine_prompt = f"""
   You are an expert UiPath Business Analyst refining a PDD section.
   Section name: '{section_name}'
   Current content: {current_content}
   User feedback: {user_feedback}

   Rewrite the section content based on the user's feedback.
   IMPORTANT FORMATTING INSTRUCTIONS:
   - Use HTML tags: <p>, <ul>, <li>, <strong>, <em>
   - DO NOT include markdown formatting
   - DO NOT repeat the section name/title
   - Start immediately with the content
   """
   ```

2. Invokes GPT-4o via LangChain
3. Returns refined content

**Output:**
```json
{
  "refined_content": "<p>Refined content...</p>"
}
```

---

##### 6. Export PDD
```python
@router.post("/api/export-pdd")
async def export_pdd(request: Request, body: ExportPDDRequest)
```

**Purpose:** Exports PDD in various formats.

**Input:**
- JSON with process_name, sections, diagram_code, format

**Process by Format:**

**PDF:**
1. Renders HTML template with PDD data
2. Returns HTML string
3. Frontend opens in new window and triggers browser print dialog

**Word (DOCX):**
1. Creates `python-docx` Document object
2. Adds title and subtitle
3. **Finds diagram insertion point:**
   ```python
   for i, section in enumerate(sections):
       if section['name'] in ["Process Overview (AS IS)",
                              "High Level Process Map (AS IS)",
                              "Detailed Process Map (AS IS)"]:
           diagram_insert_after = i
           break
   ```
4. Iterates through sections:
   - Applies heading hierarchy (H1, H2, H3, H4)
   - Converts HTML to plain text
   - Detects list items (bullets and numbered)
   - Inserts diagram after target section
5. Saves to BytesIO buffer
6. Returns downloadable file

**HTML:**
1. Renders Jinja2 template
2. Diagram placement logic matches Word export
3. Returns complete HTML file for download

**Output:** File download with appropriate MIME type

---

### 3. Text Agent (`text_agent.py`)

**File:** `backend/app/agents/text_agent.py`

**Purpose:** Extracts structured PDD sections from text using GPT-4o.

#### Function: `load_pdd_structure()`
```python
def load_pdd_structure() -> Dict:
    """Load the PDD structure from YAML file."""
```

**Purpose:** Reads and parses the PDD section definitions.

**Process:**
1. Builds path to `pdd_structure.yaml`
2. Uses `yaml.safe_load()` to parse YAML
3. Returns dictionary with sections list

**YAML Structure:**
```yaml
sections:
  - name: "Project Name"
    prompt: "Extract the official name..."
  - name: "Purpose"
    prompt: "Summarize the overall purpose..."
  ... (15 sections total)
```

---

#### Function: `extract_pdd_sections()`
```python
def extract_pdd_sections(text_content: str) -> List[Dict[str, str]]
```

**Purpose:** Core function that extracts all PDD sections from input text.

**Parameters:**
- `text_content`: Raw process description (from text, document, or video)

**Returns:**
- List of dictionaries: `[{"name": "Section Name", "content": "HTML content"}, ...]`

**Process Flow:**

1. **Initialize LLM**
   ```python
   llm = ChatOpenAI(
       model="gpt-4o",
       temperature=0,
       api_key=os.getenv("OPENAI_API_KEY"),
       base_url=os.getenv("OPENAI_API_BASE")
   )
   ```
   - `temperature=0`: Consistent, deterministic outputs
   - Uses environment variables for API credentials

2. **Load PDD Structure**
   - Calls `load_pdd_structure()` to get section definitions
   - Retrieves list of 15 sections with prompts

3. **Process Each Section**
   ```python
   for section in sections:
       section_name = section["name"]
       section_prompt = section["prompt"]

       full_prompt = f"""{section_prompt}

       Process Description:
       {text_content}

       Please provide the content for the '{section_name}' section...

       IMPORTANT FORMATTING INSTRUCTIONS:
       - Use HTML tags for formatting...
       - DO NOT repeat the section name/title...
       """

       response = llm.invoke(full_prompt)
       content = response.content

       results.append({"name": section_name, "content": content})
   ```

   **Key Prompt Elements:**
   - Section-specific prompt from YAML
   - Full process description as context
   - HTML formatting instructions
   - Explicit instruction NOT to repeat section name in output

4. **Error Handling**
   - Wraps LLM calls in try-except
   - Raises descriptive error messages
   - Catches API errors, timeouts, etc.

**Sections Generated (in order):**
1. Project Name
2. Purpose
3. Objectives
4. Key Contacts
5. Pre-requisites
6. Process Overview (AS IS)
7. Detailed Process Steps (AS IS)
8. Business Rules & Exceptions
9. Known Issues
10. Reporting & Reconciliation
11. Other Considerations
12. TO BE Process Overview
13. Detailed Process Steps (TO BE)
14. Benefits/ROI
15. Risk Assessment & Mitigation

---

### 4. Video Agent (`video_agent.py`)

**File:** `backend/app/agents/video_agent.py`

**Purpose:** Processes video files to extract process information through audio transcription and synthesis.

**Key Innovation:** Works without ffmpeg by sending video files directly to Whisper API (which supports MP4, MOV, etc.).

#### Function: `transcribe_audio_from_video()`
```python
def transcribe_audio_from_video(video_path: str) -> str
```

**Purpose:** Transcribes audio from video file using OpenAI Whisper API.

**Parameters:**
- `video_path`: Full path to video file

**Returns:**
- Transcribed text as string

**Process:**
1. Opens video file in binary read mode
2. Calls Whisper API:
   ```python
   with open(video_path, 'rb') as video_file:
       transcription = client.audio.transcriptions.create(
           model="whisper-1",
           file=video_file,
           response_format="text"
       )
   ```
3. Returns transcription

**Supported Formats:** MP3, MP4, MPEG, MPGA, M4A, WAV, WEBM

**Key Feature:** No need for ffmpeg to extract audio - Whisper handles video files directly!

---

#### Function: `analyze_video_frames()`
```python
def analyze_video_frames(video_path: str, transcript: str) -> str
```

**Purpose:** Placeholder for visual frame analysis.

**Current Implementation:**
- Returns message: "Note: Visual frame analysis requires ffmpeg. Using audio transcription only."

**Original Design (Requires ffmpeg):**
- Extract frames every 3-5 seconds
- Analyze each frame with GPT-4o vision
- Describe UI actions (clicks, typing, navigation)

**Why Simplified:**
- ffmpeg not installed in environment
- Audio transcription provides sufficient process detail
- Reduces processing time and API costs

---

#### Function: `synthesize_video_analysis()`
```python
def synthesize_video_analysis(transcript: str, visual_actions: str) -> str
```

**Purpose:** Combines transcript (and optionally visual actions) into coherent step-by-step guide.

**Parameters:**
- `transcript`: Audio transcription from video
- `visual_actions`: Visual analysis (or note about skipping)

**Process:**
1. Initializes ChatOpenAI with GPT-4o
2. Constructs synthesis prompt:
   ```python
   synthesis_prompt = f"""
   You are an expert UiPath Business Analyst.
   Create a detailed, step-by-step text guide from a screen recording.

   Audio transcript: {transcript}
   Visual analysis note: {visual_actions}

   Based on the audio transcript, create a comprehensive guide:
   - Focus on specific actions, inputs, and decisions
   - Include field names, button names, navigation steps
   - Organize into clear, sequential steps
   - Add business rules and conditions

   Output ONLY the step-by-step guide.
   """
   ```
3. Invokes LLM
4. Returns synthesized guide

**Use Case:** Converts conversational audio into structured process documentation

---

### 5. Diagram Agent (`diagram_agent.py`)

**File:** `backend/app/agents/diagram_agent.py`

**Purpose:** Generates Mermaid.js flowchart syntax from process steps.

#### Function: `generate_mermaid_diagram()`
```python
def generate_mermaid_diagram(process_steps: str) -> str
```

**Purpose:** Converts textual process steps into visual Mermaid diagram.

**Parameters:**
- `process_steps`: Content from "Detailed Process Steps" section

**Returns:**
- Mermaid.js syntax string (e.g., "graph TD\nA[Start] --> B{Decision}")

**Process:**
1. Initialize ChatOpenAI with GPT-4o
2. Construct diagram prompt:
   ```python
   diagram_prompt = f"""
   You are an expert in business process modeling.
   Convert the following process steps into a Mermaid.js flowchart.

   Use graph TD (top-down) syntax.
   - Represent steps as nodes: A[Step description]
   - Decisions as diamonds: B{Condition?}
   - Connect nodes: A --> B
   - Keep node text concise
   - ONLY output valid Mermaid code, no markdown

   Process Steps:
   {process_steps}
   """
   ```
3. Invoke LLM
4. Clean response (remove markdown if present)
5. Return raw Mermaid code

**Example Output:**
```
graph TD
    A[Start] --> B{Invoice valid?}
    B -->|Yes| C[Check amount]
    B -->|No| D[Return to sender]
    C --> E{Amount > $1000?}
    E -->|Yes| F[Manager approval]
    E -->|No| G[Auto approve]
    F --> H[Process payment]
    G --> H
```

---

### 6. File Parser (`file_parser.py`)

**File:** `backend/app/utils/file_parser.py`

**Purpose:** Extracts text from PDF and Word documents.

#### Function: `parse_document()`
```python
def parse_document(file_path: str) -> str
```

**Purpose:** Main parser function that routes to specific parser based on file extension.

**Parameters:**
- `file_path`: Path to document file

**Returns:**
- Extracted text as string

**Process:**
1. Validates file existence
2. Extracts file extension
3. Routes to appropriate parser:
   - `.docx` → `_parse_docx()`
   - `.pdf` → `_parse_pdf()`
4. Raises error for unsupported types

---

#### Function: `_parse_docx()`
```python
def _parse_docx(file_path: str) -> str
```

**Purpose:** Extracts text from Microsoft Word documents.

**Library:** `python-docx`

**Process:**
1. Opens DOCX file
2. Extracts all paragraphs
3. Filters out empty paragraphs
4. Joins with double newlines

**Code:**
```python
doc = Document(file_path)
paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
return '\n\n'.join(paragraphs)
```

**Limitations:**
- Does not extract tables, images, or formatting
- Plain text only

---

#### Function: `_parse_pdf()`
```python
def _parse_pdf(file_path: str) -> str
```

**Purpose:** Extracts text from PDF documents.

**Library:** `pypdf`

**Process:**
1. Creates PdfReader instance
2. Iterates through all pages
3. Extracts text from each page
4. Filters out empty pages
5. Joins with double newlines

**Code:**
```python
reader = PdfReader(file_path)
text_parts = []
for page in reader.pages:
    text = page.extract_text()
    if text and text.strip():
        text_parts.append(text.strip())
return '\n\n'.join(text_parts)
```

**Limitations:**
- Works only on text-based PDFs
- **Does NOT work on scanned PDFs** (images)
- For scanned PDFs, OCR library like `pytesseract` or `pdf2image` would be needed

---

### 7. PDD Structure (`pdd_structure.yaml`)

**File:** `backend/app/core/pdd_structure.yaml`

**Purpose:** Defines all PDD sections and their extraction prompts.

**Structure:**
```yaml
sections:
  - name: "Project Name"
    prompt: "Extract the official name..."
  - name: "Purpose"
    prompt: "Summarize the overall purpose..."
  ... (15 sections)
```

**Purpose of YAML:**
- **Easy Modification:** Add/remove sections without code changes
- **Prompt Versioning:** Track changes to extraction prompts
- **Consistency:** Single source of truth for PDD structure

**All Sections:**
1. Project Name - Official process title
2. Purpose - Overall goal and objective
3. Objectives - Specific measurable goals
4. Key Contacts - Stakeholders and their roles
5. Pre-requisites - Required conditions/systems
6. Process Overview (AS IS) - Current state description
7. Detailed Process Steps (AS IS) - Step-by-step current process
8. Business Rules & Exceptions - Conditions and error handling
9. Known Issues - Current problems
10. Reporting & Reconciliation - Audit and reporting requirements
11. Other Considerations - Additional relevant information
12. TO BE Process Overview - Future state description
13. Detailed Process Steps (TO BE) - Future process steps
14. Benefits/ROI - Expected improvements and value
15. Risk Assessment & Mitigation - Potential risks and mitigation strategies

---

### 8. PDD Template (`pdd_template.html`)

**File:** `backend/app/templates/pdd_template.html`

**Purpose:** Jinja2 template for rendering HTML PDDs.

**Key Features:**

**1. Mermaid.js Integration**
```html
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
```
- Loads Mermaid library for diagram rendering
- Version 10.x (current stable)

**2. Professional Styling**
```css
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #333;
    background-color: #f5f5f5;
}
.container {
    max-width: 1200px;
    background-color: white;
    padding: 40px;
    border-radius: 8px;
}
```
- Clean, professional design
- Optimized for printing (A4 page size)
- Responsive layout

**3. Dynamic Diagram Placement**
```jinja
{% set diagram_inserted = false %}
{% for section in sections %}
    {# Render section #}

    {% if not diagram_inserted and diagram_code and
          (section.name == "Process Overview (AS IS)" or
           section.name == "High Level Process Map (AS IS)" or
           section.name == "Detailed Process Map (AS IS)") %}
        {% set diagram_inserted = true %}
        <div class="diagram-container">
            <h2>Process Flow Diagram</h2>
            <div class="mermaid">{{ diagram_code }}</div>
        </div>
    {% endif %}
{% endfor %}
```
- Places diagram after first matching section
- Ensures diagram appears only once
- Uses Jinja2 set/conditionals

**4. HTML Content Rendering**
```jinja
<div class="section-content">
    {{ section.content | safe }}
</div>
```
- `| safe` filter tells Jinja2 to render HTML tags
- Without it, HTML would be escaped and displayed as text

**5. Print Optimization**
```css
@media print {
    .diagram-container {
        page-break-inside: avoid;
    }
    h2 {
        page-break-after: avoid;
    }
}
```
- Prevents diagram from being split across pages
- Ensures headings stay with following content

---

## Frontend Components

### Understanding the Frontend

The **frontend** is the **user interface** - what users see and interact with in their browser. Think of it like the display screen and buttons on an ATM machine:

- **Frontend** = The screen and buttons you interact with
- **Backend** = The computer behind the wall that processes your requests

When you open the PDD Generator in your browser, you're seeing the frontend. When you click buttons or type text, the frontend sends your actions to the backend and displays the results.

### Key Frontend Technologies

#### React - The UI Library
**What is it?**
React is a **JavaScript library** for building user interfaces. It's like a box of LEGO blocks for websites - you build complex interfaces by combining simple, reusable pieces.

**What it does in PDD Generator**
- Creates the UI components (forms, buttons, displays)
- Manages what appears on the screen
- Handles user interactions (clicks, typing, file uploads)
- Updates the display when data changes

**Why it's used here**
- **Component-based**: Build once, reuse everywhere
- **Interactive**: Smooth updates without reloading the page
- **Popular**: Huge community and lots of help available
- **Fast**: Efficient updates to the UI

#### Vite - The Build Tool
**What is it?**
Vite is a **build tool** that runs the React app during development.

**What it does in PDD Generator**
- Serves the React application in development
- Reloads the browser automatically when code changes
- Bundles everything for production

**Why it's used here**
- **Lightning fast**: Uses native browser modules
- **Instant updates**: See changes immediately
- **Modern**: Built with latest web standards

#### Axios - The HTTP Client
**What is it?**
Axios is a **library for making HTTP requests** to backend servers.

**What it does in PDD Generator**
- Sends data from frontend to backend (text, files)
- Receives responses from the backend
- Handles loading states and errors
- Manages async operations smoothly

**Why it's used here**
- **Simple**: Easier to use than browser's fetch API
- **Powerful**: Automatic JSON conversion, request cancellation
- **Reliable**: Good error handling

#### Mermaid.js - The Diagram Library
**What is it?**
Mermaid is a **library that turns text into diagrams**.

**What it does in PDD Generator**
- Takes diagram code from the backend
- Draws flowcharts showing process steps
- Makes diagrams interactive and readable

**Why it's used here**
- **Text-based**: Easy to store and transfer
- **Automatic**: No manual diagram drawing
- **Professional**: Clean, readable diagrams

#### DOMPurify - The Security Library
**What is it?**
DOMPurify is a **security library** that cleans HTML.

**What it does in PDD Generator**
- Removes dangerous code from HTML before displaying it
- Prevents XSS (Cross-Site Scripting) attacks
- Keeps safe HTML formatting

**Why it's used here**
- **Security**: Blocks malicious scripts
- **Safe**: Allows HTML formatting without risk
- **Necessary**: AI-generated HTML could contain anything

---

### 1. Main Application (`App.jsx`)

**File:** `frontend/src/App.jsx`

**Purpose:** Root React component managing application state and UI.

#### State Management
```javascript
const [processText, setProcessText] = useState('')
const [uploadedFile, setUploadedFile] = useState(null)
const [pddData, setPddData] = useState(null)
const [loading, setLoading] = useState(false)
const [error, setError] = useState('')
```

**State Variables:**
- `processText`: User-entered process description (optional)
- `uploadedFile`: File object for document/video upload (optional)
- `pddData`: Generated PDD data (process_name, sections, diagram_code)
- `loading`: Loading indicator during API calls
- `error`: Error message display

**Key Point:** Both text and file can be provided simultaneously

---

#### Function: `generatePDD()`
```javascript
const generatePDD = async () => {
    if (!processText.trim() && !uploadedFile) {
        setError('Please enter a process description or upload a file')
        return
    }

    setLoading(true)
    setError('')
    setPddData(null)

    try {
        if (uploadedFile) {
            // File upload processing
            const formData = new FormData()
            formData.append('file', uploadedFile)

            const response = await axios.post(
                '/api/upload-and-process-json',
                formData,
                { headers: { 'Content-Type': 'multipart/form-data' } }
            )

            setPddData(response.data)
        } else if (processText.trim()) {
            // Text input processing
            const response = await axios.post('/api/generate-pdd-json', {
                process_text: processText
            })

            setPddData(response.data)
        }
    } catch (err) {
        // Error handling
    } finally {
        setLoading(false)
    }
}
```

**Process Flow:**
1. Validates at least one input is provided
2. Clears previous PDD data
3. Routes to appropriate endpoint:
   - File upload: `/api/upload-and-process-json`
   - Text input: `/api/generate-pdd-json`
4. Updates state with response data
5. Handles errors with user-friendly messages

---

#### Function: `exportDocument()`
```javascript
const exportDocument = async (format) => {
    if (!pddData) return

    setLoading(true)
    try {
        if (format === 'pdf') {
            // Open HTML in new window for printing
            const response = await axios.post('/api/export-pdd', {
                process_name: pddData.process_name,
                sections: pddData.sections,
                diagram_code: pddData.diagram_code,
                format: format
            })

            const printWindow = window.open('', '_blank')
            printWindow.document.write(response.data)
            printWindow.document.close()
            setTimeout(() => printWindow.print(), 500)
        } else {
            // Download Word or HTML file
            const response = await axios.post('/api/export-pdd', {
                process_name: pddData.process_name,
                sections: pddData.sections,
                diagram_code: pddData.diagram_code,
                format: format
            }, { responseType: 'blob' })

            const blob = new Blob([response.data])
            const url = URL.createObjectURL(blob)
            const a = window.document.createElement('a')
            a.href = url
            a.download = `PDD_${pddData.process_name.replace(/[^a-z0-9]/gi, '_')}.${format === 'docx' ? 'docx' : 'html'}`
            a.click()
            URL.revokeObjectURL(url)
        }
    } catch (error) {
        alert(`Failed to export as ${format.toUpperCase()}`)
    } finally {
        setLoading(false)
    }
}
```

**PDF Export Strategy:**
- Backend returns HTML string
- Frontend opens in new window
- Triggers browser print dialog
- User saves as PDF

**Word/HTML Export Strategy:**
- Backend returns binary data (blob)
- Frontend creates download URL
- Programmatically triggers download
- Sanitizes filename (removes special characters)

---

#### JSX Structure

**Input Section:**
```jsx
<div className="input-section">
    {/* Text Input */}
    <label>Process Description (Optional)</label>
    <textarea value={processText} onChange={...} rows={8} />

    {/* Divider */}
    <div className="divider">OR</div>

    {/* File Upload */}
    <label>Upload Document or Video (Optional)</label>
    <input type="file" accept=".pdf,.docx,.mp4,.mov,.avi" onChange={...} />

    {/* Buttons */}
    <button onClick={generatePDD} disabled={loading || (!processText.trim() && !uploadedFile)}>
        {loading ? 'Processing...' : 'Generate PDD'}
    </button>
    <button onClick={clearForm} disabled={loading}>Clear</button>

    {/* Export Buttons (shown after PDD generated) */}
    {pddData && (
        <div className="export-section">
            <label>Export Options</label>
            <button onClick={exportToPDF}>Export PDF</button>
            <button onClick={exportToWord}>Export Word</button>
            <button onClick={exportToHTML}>Export HTML</button>
        </div>
    )}
</div>
```

**Output Section (with Conditional Diagram):**
```jsx
{pddData && (
    <div className="output-section">
        <h2>{pddData.process_name}</h2>

        <div className="sections-container">
            {pddData.sections.map((section, index) => {
                // Find first matching section for diagram
                const diagramSectionIndex = pddData.sections.findIndex(s =>
                    s.name === "Process Overview (AS IS)" ||
                    s.name === "High Level Process Map (AS IS)" ||
                    s.name === "Detailed Process Map (AS IS)"
                )
                const showDiagramAfter = diagramSectionIndex >= 0 && index === diagramSectionIndex

                return (
                    <React.Fragment key={index}>
                        <PDDSection section={section} onRefine={handleSectionRefine} />
                        {showDiagramAfter && pddData.diagram_code && (
                            <DiagramViewer diagramCode={pddData.diagram_code} />
                        )}
                    </React.Fragment>
                )
            })}
        </div>
    </div>
)}
```

**Key Design Decisions:**
- Calculates diagram position once (using `findIndex`)
- Only shows diagram after first matching section
- Uses `React.Fragment` to avoid extra DOM nodes

---

### 2. PDD Section Component (`PDDSection.jsx`)

**File:** `frontend/src/components/PDDSection.jsx`

**Purpose:** Renders individual PDD sections with editing and AI refinement capabilities.

#### Component State
```javascript
const [isEditing, setIsEditing] = useState(false)
const [editedContent, setEditedContent] = useState(section.content)
const [showRefine, setShowRefine] = useState(false)
const [refineFeedback, setRefineFeedback] = useState('')
const [refining, setRefining] = useState(false)
const [originalContent, setOriginalContent] = useState(section.content)
const [isComparing, setIsComparing] = useState(false)
```

**State Explanations:**
- `isEditing`: Toggle edit mode (manual editing)
- `editedContent`: Temporary content during editing
- `showRefine`: Toggle AI refine input panel
- `refineFeedback`: User's feedback for AI refinement
- `refining`: Loading state during AI refinement
- `originalContent`: Saved copy before refinement for comparison
- `isComparing`: Shows side-by-side comparison view

---

#### View Modes

**1. Display Mode (Default)**
```jsx
<div className="section-content" dangerouslySetInnerHTML={{ __html: section.content }} />
```
- Renders HTML content safely
- `dangerouslySetInnerHTML` allows HTML rendering
- "Dangerous" name warns about XSS risks (content is from trusted AI)

**2. Edit Mode (Manual)**
```jsx
<textarea
    className="edit-textarea"
    value={editedContent}
    onChange={(e) => setEditedContent(e.target.value)}
    rows={10}
/>
<div className="edit-actions">
    <button onClick={handleSave}>Save</button>
    <button onClick={handleCancel}>Cancel</button>
</div>
```
- Full content editing
- Save updates parent state via `onRefine` callback
- Cancel reverts to original content

**3. Compare Mode (After AI Refinement)**
```jsx
<div className="comparison-view">
    <div className="comparison-panel">
        <h4>Original</h4>
        <div className="comparison-content original">{originalContent}</div>
    </div>
    <div className="comparison-panel">
        <h4>Refined</h4>
        <div className="comparison-content refined">{editedContent}</div>
    </div>
    <div className="comparison-actions">
        <button onClick={acceptRefined}>Accept Refined</button>
        <button onClick={rejectRefined}>Reject</button>
    </div>
</div>
```
- Side-by-side comparison
- Visual distinction (red/green backgrounds)
- Accept or Reject buttons

---

#### AI Refinement Flow

```javascript
const handleRefine = async () => {
    if (!refineFeedback.trim()) return

    setRefining(true)
    try {
        const response = await axios.post('/refine-section', {
            section_name: section.name,
            current_content: section.content,
            user_feedback: refineFeedback
        })

        setOriginalContent(section.content)  // Save current for comparison
        setEditedContent(response.data.refined_content)  // Update with refined
        setIsComparing(true)  // Show comparison view
        setShowRefine(false)  // Hide refine panel
        setRefineFeedback('')  // Clear feedback input
    } catch (error) {
        alert('Failed to refine section. Please try again.')
    } finally {
        setRefining(false)
    }
}
```

**Steps:**
1. User clicks ✨ AI Refine button
2. Textarea appears for feedback input
3. User enters feedback (e.g., "Add more details about error handling")
4. On submit, calls `/refine-section` endpoint
5. Backend uses GPT-4o to rewrite content
6. Frontend displays side-by-side comparison
7. User accepts or rejects the refinement

---

### 3. Diagram Viewer Component (`DiagramViewer.jsx`)

**File:** `frontend/src/components/DiagramViewer.jsx`

**Purpose:** Renders Mermaid.js flowchart diagrams.

#### Mermaid Initialization
```javascript
useEffect(() => {
    mermaid.initialize({
        startOnLoad: true,
        theme: 'default',
        flowchart: {
            useMaxWidth: true,
            htmlLabels: true,
            curve: 'basis'
        },
        securityLevel: 'loose'
    })
}, [])
```

**Configuration Options:**
- `startOnLoad: true`: Auto-render diagrams on page load
- `theme: 'default'`: Mermaid theme (default, forest, dark, neutral)
- `useMaxWidth: true`: Responsive diagram width
- `htmlLabels: true`: Allow HTML in node labels
- `curve: 'basis'`: Smooth curved connector lines
- `securityLevel: 'loose'`: Allow HTML in labels (required for rich formatting)

---

#### Diagram Rendering
```javascript
useEffect(() => {
    if (containerRef.current && diagramCode) {
        // Clear previous content
        containerRef.current.innerHTML = ''

        // Generate unique ID
        const id = `mermaid-${Math.random().toString(36).substr(2, 9)}`

        // Render diagram
        mermaid.render(id, diagramCode).then((result) => {
            if (containerRef.current) {
                containerRef.current.innerHTML = result.svg
            }
        }).catch((error) => {
            console.error('Mermaid rendering error:', error)
            if (containerRef.current) {
                containerRef.current.innerHTML = `<p class="error">Failed to render diagram</p>`
            }
        })
    }
}, [diagramCode])
```

**Process:**
1. Clears previous diagram (if any)
2. Generates unique element ID (avoids conflicts)
3. Calls `mermaid.render()` with:
   - Element ID
   - Mermaid diagram code
4. On success: Injects SVG into DOM
5. On error: Displays error message

**Why Unique ID?**
- Multiple diagrams could exist on same page
- Mermaid requires unique IDs for each
- Random string ensures no collisions

**Why `useRef` for Container?**
- Direct DOM manipulation needed (innerHTML)
- Avoids React re-renders during Mermaid processing
- Better performance for complex diagrams

---

## Security Components

### Understanding Web Security

**Web security** means protecting the application from bad actors who might try to:
- Steal data
- Break the application
- Use the API unfairly
- Inject malicious code

Think of web security like the locks and security guards at a bank:
- **Locks** = Authentication (only authorized users can enter)
- **Security guards** = Validation (checking IDs at the door)
- **Cameras** = Logging (recording what happens)
- **Alarm systems** = Rate limiting (alerting on suspicious activity)

### Key Security Features in PDD Generator

#### Rate Limiting - Preventing Abuse
**What is it?**
Rate limiting restricts how many requests a user can make in a time period.

**What it does in PDD Generator**
- Limits PDD generation to 10 requests per minute
- Limits file uploads to 5 requests per minute
- Limits section refinement to 20 requests per minute
- Returns error message when limits are exceeded

**Why it's used here**
- **Prevents abuse**: Stops users from overwhelming the server
- **Fair usage**: Ensures everyone gets equal access
- **Cost control**: Limits OpenAI API costs
- **Stability**: Prevents server crashes from too many requests

**Technical Implementation**: Uses the `slowapi` library to track requests by IP address and enforce limits.

#### CORS - Cross-Origin Resource Sharing
**What is it?**
CORS is a security feature that controls which websites can talk to the backend.

**What it does in PDD Generator**
- Allows frontend on localhost:5173 to talk to backend on localhost:8000
- Blocks requests from unauthorized websites
- Configurable for production domains

**Why it's used here**
- **Browser security**: Browsers block cross-port requests by default
- **Protection**: Prevents malicious websites from using the API
- **Flexibility**: Can whitelist trusted domains

**Technical Implementation**: FastAPI CORS middleware checks the `Origin` header and allows or blocks requests.

#### Input Validation - Checking Data
**What is it?**
Input validation ensures incoming data is correct and safe.

**What it does in PDD Generator**
- Checks that required fields are present
- Verifies data types (text, numbers, files)
- Validates file types (only PDF, DOCX, MP4, etc.)
- Limits file sizes (max 100MB)

**Why it's used here**
- **Prevents crashes**: Bad data can't break the system
- **Security**: Blocks malicious input
- **Clear errors**: Tells users exactly what's wrong
- **Early detection**: Catches problems before processing

**Technical Implementation**: Uses Pydantic models to automatically validate and type-check all incoming data.

#### XSS Protection - Preventing Malicious Scripts
**What is it?**
XSS (Cross-Site Scripting) protection blocks malicious scripts in user-generated content.

**What it does in PDD Generator**
- DOMPurify removes dangerous code from HTML before displaying
- Allows safe HTML formatting (bold, lists, etc.)
- Blocks script tags and event handlers

**Why it's used here**
- **Security**: AI-generated content could contain anything
- **Safety**: Prevents attacks through PDD content
- **Flexibility**: Still allows HTML formatting

**Technical Implementation**: DOMPurify sanitizes all AI-generated HTML before rendering in React components.

#### Environment Variables - Protecting Secrets
**What is it?**
Environment variables store sensitive configuration outside the code.

**What it does in PDD Generator**
- Stores OpenAI API key
- Holds configuration settings
- Different values for development/production

**Why it's used here**
- **Security**: API keys never in code or git
- **Flexibility**: Change settings without code changes
- **Best practice**: Standard industry approach

**Technical Implementation**: Uses `.env` file (not in git) and `config.yaml` for settings.

#### Request Logging - Audit Trail
**What is it?**
Request logging records all API requests for monitoring and debugging.

**What it does in PDD Generator**
- Logs every API request with method, path, and timing
- Records response status codes
- Tracks client IP addresses
- Helps debug issues

**Why it's used here**
- **Debugging**: See what's happening in the system
- **Security**: Detect suspicious patterns
- **Performance**: Identify slow endpoints
- **Audit**: Know who accessed what

**Technical Implementation**: Custom middleware logs all requests before and after processing.

### Security Best Practices Implemented

✅ **Rate limiting** on all endpoints
✅ **CORS** configured for allowed origins only
✅ **Input validation** on all requests
✅ **XSS protection** with DOMPurify
✅ **API keys** in environment variables
✅ **Request logging** for audit trail
✅ **Error handling** without exposing sensitive information
✅ **File type validation** for uploads
✅ **File size limits** to prevent denial of service
✅ **Non-root Docker user** for container security

---

## Data Flow

### Complete End-to-End Flow

#### Scenario 1: Text Input → PDD Generation

```
1. USER enters text in textarea
   ↓
2. USER clicks "Generate PDD"
   ↓
3. FRONTEND: generatePDD()
   - Validates input
   - Shows loading spinner
   ↓
4. API CALL: POST /api/generate-pdd-json
   Body: {"process_text": "..."}
   ↓
5. BACKEND: generate_pdd_json()
   - Strips HTML tags from process name
   ↓
6. BACKEND: extract_pdd_sections()
   For each of 15 sections:
   a. Load section definition from YAML
   b. Construct prompt with:
      - Section-specific instructions
      - Full process description
      - HTML formatting requirements
   c. Call OpenAI GPT-4o API
   d. Parse response
   e. Store in results array
   ↓
7. BACKEND: generate_mermaid_diagram()
   - Extracts "Detailed Process Steps"
   - Constructs diagram prompt
   - Calls GPT-4o
   - Returns Mermaid code
   ↓
8. BACKEND: Returns JSON response
   {
     "process_name": "Invoice Processing",
     "sections": [...],
     "diagram_code": "graph TD..."
   }
   ↓
9. FRONTEND: Receives response
   - Updates pddData state
   - Hides loading spinner
   ↓
10. FRONTEND: Renders PDD
    - Displays process name
    - Renders sections
    - Inserts diagram after "Process Overview (AS IS)"
    - Shows export buttons
```

---

#### Scenario 2: Video Upload → PDD Generation

```
1. USER selects .mp4 file
   ↓
2. USER clicks "Generate PDD"
   ↓
3. FRONTEND: generatePDD()
   - Creates FormData
   - Appends file
   ↓
4. API CALL: POST /api/upload-and-process-json
   Content-Type: multipart/form-data
   ↓
5. BACKEND: upload_and_process_json()
   - Validates file extension (.mp4)
   - Saves to temp file
   ↓
6. BACKEND: transcribe_audio_from_video()
   - Opens video file
   - Calls Whisper API
   - Returns transcript
   ↓
7. BACKEND: analyze_video_frames()
   - Returns: "Using audio transcription only"
   ↓
8. BACKEND: synthesize_video_analysis()
   - Constructs synthesis prompt
   - Calls GPT-4o with transcript
   - Returns structured guide
   ↓
9. BACKEND: extract_pdd_sections()
   - Processes synthesized guide
   - Generates 15 sections
   ↓
10. BACKEND: generate_mermaid_diagram()
    - Creates flowchart
    ↓
11. BACKEND: Cleanup
    - Deletes temp video file
    ↓
12. BACKEND: Returns JSON response
    ↓
13. FRONTEND: Renders PDD
```

---

#### Scenario 3: AI Refinement Flow

```
1. USER clicks ✨ (AI Refine) button on section
   ↓
2. FRONTEND: Shows refine textarea
   "Describe how you'd like to improve this section..."
   ↓
3. USER enters feedback: "Add more details about error handling"
   ↓
4. USER clicks "✨ AI Refine" button
   ↓
5. FRONTEND: handleRefine()
   - Sets refining=true
   - Calls /refine-section endpoint
   ↓
6. API CALL: POST /refine-section
   {
     "section_name": "Business Rules & Exceptions",
     "current_content": "<p>Current content...</p>",
     "user_feedback": "Add more details about error handling"
   }
   ↓
7. BACKEND: refine_section()
   - Constructs refinement prompt
   - Calls GPT-4o
   ↓
8. BACKEND: Returns refined content
   {
     "refined_content": "<p>Enhanced content with error handling details...</p>"
   }
   ↓
9. FRONTEND: Receives response
   - Saves original content
   - Updates edited content
   - Sets isComparing=true
   ↓
10. FRONTEND: Renders comparison view
    - Left panel: Original (red background)
    - Right panel: Refined (green background)
    - Buttons: "Accept Refined", "Reject"
    ↓
11. USER clicks "Accept Refined"
    ↓
12. FRONTEND: acceptRefined()
    - Calls onRefine(section.name, editedContent)
    - Updates parent state
    - Exits comparison mode
```

---

#### Scenario 4: Export to Word

```
1. USER clicks "Export Word" button
   ↓
2. FRONTEND: exportToWord()
   - Sets loading=true
   ↓
3. API CALL: POST /api/export-pdd
   {
     "process_name": "Invoice Processing",
     "sections": [...],
     "diagram_code": "graph TD...",
     "format": "docx"
   }
   ↓
4. BACKEND: export_pdd()
   ↓
5. BACKEND: _create_word_document()
   a. Create python-docx Document
   b. Add title: "Invoice Processing"
   c. Add subtitle: "Process Definition Document (PDD)"
   d. Find diagram insertion point (section index)
   e. For each section:
      - Determine heading level (H1-H4)
      - Convert HTML to plain text
      - Detect lists and apply list style
      - Add paragraph
      - If this is diagram section, insert diagram
   f. Save to BytesIO
   g. Return bytes
   ↓
6. BACKEND: Returns file with headers
   Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document
   Content-Disposition: attachment; filename="PDD_Invoice_Processing.docx"
   ↓
7. FRONTEND: Receives blob
   - Creates object URL
   - Creates hidden <a> element
   - Sets download attribute
   - Programmatically clicks link
   - Revokes object URL
   ↓
8. BROWSER: Downloads file
   PDD_Invoice_Processing.docx
```

---

## API Endpoints Summary

### Complete Endpoint List

| Method | Endpoint | Request | Response | Purpose |
|--------|----------|---------|----------|---------|
| POST | `/generate-pdd` | JSON: `{process_text}` | HTML | Generate HTML PDD from text |
| POST | `/upload-and-process` | File (multipart) | HTML | Generate HTML PDD from file |
| POST | `/api/generate-pdd-json` | JSON: `{process_text}` | JSON | Generate JSON PDD from text |
| POST | `/api/upload-and-process-json` | File (multipart) | JSON | Generate JSON PDD from file |
| POST | `/refine-section` | JSON: `{section_name, current_content, user_feedback}` | JSON: `{refined_content}` | AI-powered section refinement |
| POST | `/api/export-pdd` | JSON: `{process_name, sections, diagram_code, format}` | File/HTML | Export PDD to PDF/Word/HTML |

---

### Request/Response Examples

#### 1. Generate PDD (JSON)

**Request:**
```bash
curl -X POST http://localhost:8000/api/generate-pdd-json \
  -H "Content-Type: application/json" \
  -d '{
    "process_text": "The invoice processing process begins when an invoice is received via email..."
  }'
```

**Response:**
```json
{
  "process_name": "Invoice Processing Automation",
  "sections": [
    {
      "name": "Project Name",
      "content": "<p>Invoice Processing Automation</p>"
    },
    {
      "name": "Purpose",
      "content": "<p>To automate the processing of vendor invoices...</p>"
    }
  ],
  "diagram_code": "graph TD\nA[Start]..."
}
```

---

#### 2. Upload File

**Request:**
```bash
curl -X POST http://localhost:8000/api/upload-and-process-json \
  -F "file=@invoice_process.mp4"
```

**Response:**
```json
{
  "process_name": "Invoice Processing from Video",
  "sections": [...],
  "diagram_code": "..."
}
```

---

#### 3. Refine Section

**Request:**
```bash
curl -X POST http://localhost:8000/refine-section \
  -H "Content-Type: application/json" \
  -d '{
    "section_name": "Business Rules & Exceptions",
    "current_content": "<p>Current rules...</p>",
    "user_feedback": "Add specific approval thresholds"
  }'
```

**Response:**
```json
{
  "refined_content": "<p>Invoices under $1000 are auto-approved. Amounts between $1000-$5000 require manager approval. Amounts over $5000 require director approval...</p>"
}
```

---

## Agent System

### Agent Architecture

The agent system follows the **Chain of Responsibility** pattern with specialized agents for different input types:

```
┌─────────────────────────────────────────┐
│         API Layer (endpoints.py)         │
│  - Receives requests                     │
│  - Validates input                       │
│  - Routes to appropriate agent           │
└──────────────┬──────────────────────────┘
               │
       ┌───────┴────────┐
       │                │
       ▼                ▼
┌──────────────┐  ┌──────────────┐
│  Text Agent  │  │ Video Agent  │
│              │  │              │
│  - GPT-4o    │  │  - Whisper   │
│  - Sections  │  │  - GPT-4o    │
│  - Diagram   │  │  - Synthesis │
└──────────────┘  └──────────────┘
       │
       ▼
┌──────────────┐
│Diagram Agent │
│              │
│  - GPT-4o    │
│  - Mermaid   │
└──────────────┘
```

### Agent Responsibilities

| Agent | Input | Output | Models Used |
|-------|-------|--------|------------|
| **Text Agent** | Process description (text) | 15 structured sections | GPT-4o |
| **Video Agent** | Video file | Structured guide | Whisper + GPT-4o |
| **Diagram Agent** | Process steps | Mermaid syntax | GPT-4o |

---

### Agent Communication

**Sequential Processing:**
```
Request → Video Agent → Text Agent → Diagram Agent → Response
         (transcribe) (extract)   (generate)
```

**Example: Video Upload Flow**
1. **Video Agent:** Transcribes audio → Returns text guide
2. **Text Agent:** Receives guide → Extracts 15 sections
3. **Diagram Agent:** Receives step 6 → Generates diagram
4. **API Layer:** Combines all → Returns to frontend

---

## Configuration & Deployment

### Understanding Configuration

**Configuration** is how you customize an application's behavior without changing its code. Think of it like the settings on your phone:

- **Code** = The phone's operating system (doesn't change)
- **Configuration** = Your settings (wallpaper, notifications, etc.)

**Why separate configuration from code?**
- **Security**: Sensitive data (API keys) never in code or git
- **Flexibility**: Different settings for development vs production
- **Convenience**: Change behavior without rewriting code
- **Best practice**: Industry-standard approach

### Configuration System Components

#### Environment Variables (.env)
**What is it?**
Environment variables are **settings stored outside the code** in a file called `.env`.

**What it does in PDD Generator**
- Stores the OpenAI API key (secret!)
- Holds server settings (host, port)
- Configures AI models (which model to use)
- Sets environment type (development, production)

**Why it's used here**
- **Security**: API keys never committed to git
- **Flexibility**: Different settings for each environment
- **Standard**: All web apps use this approach
- **Safe**: `.env` file is in `.gitignore` (never uploaded)

**Example**:
```bash
# .env file (NEVER commit this to git)
OPENAI_API_KEY=sk-secret-key-here
OPENAI_MODEL=gpt-4o
APP_ENV=development
```

#### config.yaml - Central Configuration
**What is it?**
A **YAML file** that contains all application settings with default values.

**What it does in PDD Generator**
- Stores default values for 200+ configuration options
- Organizes settings by category (app, server, openai, security, etc.)
- Provides documentation for each setting
- Allows changes without code modification

**Why it's used here**
- **Centralized**: One place for all settings
- **Documented**: Each setting has explanation
- **Flexible**: Override with environment variables when needed
- **Organized**: Grouped by feature (logging, security, etc.)

**Priority System**:
1. **Environment variables** (highest priority) - Override everything
2. **config.yaml** - Default configuration
3. **Code defaults** (lowest priority) - Fallback values

**Example**:
```yaml
# config.yaml
app:
  environment: production
  log_level: INFO

openai:
  llm_model: gpt-4o  # Can be overridden by OPENAI_API_KEY env var
  temperature: 0.0

rate_limiting:
  enabled: true
  limits:
    pdd_generation: 10/minute
```

#### Configuration Priority
**How it works**:
If you set `OPENAI_MODEL=gpt-3.5-turbo` in your `.env` file, it will override the `gpt-4o` value in `config.yaml`. This gives you maximum flexibility.

**Example Scenario**:
```bash
# Developer's machine
.env file: OPENAI_MODEL=gpt-3.5-turbo  (cheaper for testing)
config.yaml: llm_model: gpt-4o
Result: Uses gpt-3.5-turbo ✅

# Production server
.env file: (no OPENAI_MODEL set)
config.yaml: llm_model: gpt-4o
Result: Uses gpt-4o ✅
```

---

### Environment Variables

Create `.env` file in `backend/` directory:

```bash
# OpenAI API Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_API_BASE=https://api.openai.com/v1  # Optional: for custom endpoints

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

**Getting OpenAI API Key:**
1. Go to https://platform.openai.com/api-keys
2. Create new API key
3. Copy and paste into `.env` file

---

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
# Create .env file with your OPENAI_API_KEY

# Run server
uvicorn main:app --reload --port 8000
```

**Server runs at:** http://localhost:8000

**API Documentation:** http://localhost:8000/docs (Swagger UI)

---

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

**Server runs at:** http://localhost:5173

---

### Understanding Deployment

**Deployment** means making your application available to users on the internet. Think of it like opening a store:

- **Development** = Practicing in your garage (localhost, only you can access)
- **Deployment** = Opening the store to the public (internet, anyone can access)

**Why is deployment important?**
- **Accessibility**: Users can access your app from anywhere
- **Reliability**: Professional hosting ensures it's always available
- **Performance**: Optimized servers handle many users
- **Security**: Production environments have extra protections

### Deployment Technologies

#### Docker - Containerization
**What is it?**
Docker is a **containerization platform** that packages applications with everything they need to run. Think of it like a shipping container - it holds everything needed in one standardized box.

**What it does in PDD Generator**
- Packages the backend with Python and all dependencies
- Packages the frontend with Node.js and build tools
- Ensures the app runs the same everywhere
- Simplifies deployment to any cloud platform

**Why it's used here**
- **Consistency**: Works the same on your machine and in production
- **Isolation**: No conflicts with other apps or system libraries
- **Scalability**: Easy to run multiple copies if needed
- **Standard**: Industry-standard for deployment

**Key Benefits**:
- "Works on my machine" problem solved
- Easy to move between cloud providers
- Automatic dependency management
- Fast startup and shutdown

#### nginx - Web Server
**What is it?**
nginx is a **high-performance web server** that serves files to users.

**What it does in PDD Generator**
- Serves the React frontend (HTML, CSS, JS files)
- Handles HTTPS encryption
- Manages caching for faster loading
- Can act as a reverse proxy for the backend

**Why it's used here**
- **Fast**: One of the fastest web servers available
- **Efficient**: Handles thousands of connections easily
- **Production-ready**: Battle-tested on millions of websites
- **Lightweight**: Uses minimal resources

**Key Benefits**:
- Static file serving (React app)
- SSL/TLS termination (HTTPS)
- Load balancing (can distribute traffic)
- Caching (faster responses)

#### docker-compose - Multi-Container Orchestration
**What is it?**
docker-compose is a **tool for running multiple Docker containers together**.

**What it does in PDD Generator**
- Starts both frontend and backend containers
- Connects them so they can talk to each other
- Manages shared resources (networks, volumes)
- Makes local development and production similar

**Why it's used here**
- **Simplicity**: One command to start the whole stack
- **Consistency**: Same setup locally and in production
- **Convenience**: No need to install Python, Node.js, etc.
- **Standard**: Most common way to run multi-container apps

**Key Benefits**:
- `docker-compose up` - that's it!
- Automatic networking between containers
- Easy to add more services (databases, etc.)
- Great for development and production

### Deployment Process Overview

**From Development to Production**:
```
1. Development (Your Computer)
   ├── Frontend: React running on port 5173
   └── Backend: Python running on port 8000

2. Building (Create Containers)
   ├── Frontend: Build React app → Package in Docker image
   └── Backend: Package Python app in Docker image

3. Deployment (Push to Cloud)
   ├── Push Docker images to registry
   ├── Start containers on cloud platform
   └── Configure domain, SSL, environment variables

4. Production (Live on Internet)
   ├── Users access via your domain
   ├── nginx serves frontend
   └── Backend handles API requests
```

---

### Production Deployment

#### Backend (Docker)

**Create `backend/Dockerfile`:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Frontend (Docker)

**Create `frontend/Dockerfile`:**
```dockerfile
# Build stage
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

#### Docker Compose

**Create `docker-compose.yml`:**
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./backend:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
```

**Run:**
```bash
docker-compose up --build
```

---

## Troubleshooting

### Common Issues

#### 1. CORS Error
**Problem:** Frontend cannot connect to backend
```
Access to XMLHttpRequest at 'http://localhost:8000' from origin 'http://localhost:5173' has been blocked by CORS policy
```

**Solution:** Check `main.py` CORS configuration includes your frontend URL

#### 2. OpenAI API Error
**Problem:** `Error extracting PDD sections: Incorrect API key provided`

**Solution:**
- Verify `.env` file exists in `backend/` directory
- Check `OPENAI_API_KEY` is valid
- Restart backend after updating `.env`

#### 3. Mermaid Diagram Not Rendering
**Problem:** Diagram code shows but no visual

**Solution:**
- Open browser console (F12)
- Check for Mermaid syntax errors
- Verify diagram code is valid Mermaid syntax

#### 4. Video Upload Fails
**Problem:** "Unsupported file type" error

**Solution:**
- Check file extension is supported (.mp4, .mov, .avi)
- Verify file is not corrupted
- Check backend logs for specific error

#### 5. PDF Text Extraction Returns Empty
**Problem:** PDF upload returns empty PDD

**Solution:**
- PDF may be scanned/image-based (not text-based)
- pypdf only works on text PDFs
- Use OCR library (pytesseract) for scanned PDFs

---

## Performance Considerations

### API Response Times

| Operation | Typical Time | Bottleneck |
|-----------|--------------|------------|
| Text PDD Generation | 15-30 seconds | 15 GPT-4o API calls (one per section) |
| PDF Processing | 1-3 seconds | File I/O + text extraction |
| Video Transcription | 5-15 seconds | Whisper API processing |
| Diagram Generation | 2-5 seconds | Single GPT-4o call |
| Section Refinement | 3-5 seconds | Single GPT-4o call |
| Word Export | 1-2 seconds | python-docx processing |

**Optimization Tips:**
- Use streaming responses for long-running operations
- Implement caching for repeated requests
- Consider async processing with WebSocket updates
- Batch API calls where possible

### Cost Analysis

**OpenAI API Costs (as of 2024):**

| Model | Input Price | Output Price | Typical Cost per PDD |
|-------|-------------|--------------|---------------------|
| GPT-4o | $2.50/M tokens | $10.00/M tokens | ~$0.50 - $1.00 |
| Whisper | $0.006/minute | - | ~$0.01 - $0.05 per video |

**Per PDD Generation:**
- Text input: ~$0.50 - $1.00
- Video input: ~$0.60 - $1.10
- With 1 refinement: ~$0.05 extra

**Monthly Estimates:**
- 100 PDDs: $50 - $110
- 1000 PDDs: $500 - $1100

---

## Security Considerations

### Current Security State

| Aspect | Status | Recommendation |
|--------|--------|----------------|
| **Authentication** | ❌ Not implemented | Add JWT-based auth |
| **Rate Limiting** | ❌ Not implemented | Add rate limit middleware |
| **Input Validation** | ⚠️ Basic (Pydantic) | Add comprehensive validation |
| **File Upload Security** | ⚠️ Basic (type check) | Add file size limits, virus scan |
| **SQL Injection** | ✅ N/A (no SQL yet) | Will need with database |
| **XSS** | ⚠️ Frontend uses dangerouslySetInnerHTML | Sanitize HTML content |
| **CORS** | ✅ Configured | Keep origins whitelist updated |

### Security Best Practices

1. **Never commit `.env` file** - Add to `.gitignore`
2. **Use environment-specific configs** - Separate dev/prod environments
3. **Validate file uploads** - Size limits, type checking, content scanning
4. **Sanitize user input** - Especially before rendering HTML
5. **Implement rate limiting** - Prevent API abuse
6. **Add API authentication** - Require valid tokens for all endpoints
7. **Log all requests** - Audit trail for security incidents
8. **Keep dependencies updated** - Regular `pip install` and `npm update`

---

## Future Enhancements

### Phase 4 Implementation Roadmap

#### 1. User Authentication (Priority: HIGH)
**What:** Add login/register system with JWT tokens

**Files to Create:**
- `backend/app/auth.py` - Authentication logic
- `backend/app/models/user.py` - User model
- `frontend/src/pages/Login.jsx` - Login page
- `frontend/src/utils/auth.js` - Auth utility functions

**Key Features:**
- Password hashing with bcrypt
- JWT token generation/validation
- Protected routes
- Session management

---

#### 2. Database Integration (Priority: HIGH)
**What:** Add PostgreSQL for persistent storage

**Files to Create:**
- `backend/app/database.py` - Database connection
- `backend/app/models/pdd.py` - PDD model
- `backend/app/models/user.py` - User model
- `backend/alembic/` - Database migrations

**Schema:**
```sql
users (id, email, hashed_password, created_at)
pdds (id, user_id, process_name, sections, diagram_code, created_at)
sessions (id, user_id, token, expires_at)
```

---

#### 3. Docker Deployment (Priority: MEDIUM)
**What:** Containerize application

**Files to Create:**
- `backend/Dockerfile`
- `frontend/Dockerfile`
- `docker-compose.yml`
- `.dockerignore`

**Benefits:**
- Consistent deployment across environments
- Easy scaling
- Isolated dependencies

---

#### 4. CI/CD Pipeline (Priority: MEDIUM)
**What:** Automated testing and deployment

**Files to Create:**
- `.github/workflows/test.yml`
- `.github/workflows/deploy.yml`

**Stages:**
1. Linting (ESLint, Pylint)
2. Unit tests (Jest, pytest)
3. Build (Docker images)
4. Deploy to staging/production

---

#### 5. Testing Suite (Priority: MEDIUM)
**What:** Comprehensive test coverage

**Backend Tests:**
```python
# tests/test_text_agent.py
def test_extract_pdd_sections():
    result = extract_pdd_sections("Test process")
    assert len(result) == 15
    assert result[0]["name"] == "Project Name"

# tests/test_video_agent.py
def test_transcribe_audio():
    result = transcribe_audio_from_video("test.mp4")
    assert isinstance(result, str)

# tests/test_diagram_agent.py
def test_generate_diagram():
    result = generate_mermaid_diagram("Step 1, Step 2")
    assert "graph TD" in result
```

**Frontend Tests:**
```javascript
// src/components/__tests__/PDDSection.test.jsx
describe('PDDSection', () => {
  test('renders section name and content', () => {
    render(<PDDSection section={mockSection} />)
    expect(screen.getByText('Purpose')).toBeInTheDocument()
  })
})
```

---

## Conclusion

This AI-Powered PDD Generator demonstrates a modern, production-ready approach to automating RPA documentation. By leveraging:
- **OpenAI GPT-4o** for intelligent content extraction
- **Whisper API** for video transcription
- **LangChain** for LLM orchestration
- **FastAPI** for high-performance API
- **React** for responsive UI

The system successfully reduces PDD creation time from hours to minutes while maintaining professional quality and enabling iterative refinement through AI-human collaboration.

---

## Quick Reference

### Start Development Servers
```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

### Access Points
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### File Locations
- **Backend Config:** `backend/app/core/pdd_structure.yaml`
- **Frontend Entry:** `frontend/src/main.jsx`
- **API Routes:** `backend/app/api/endpoints.py`
- **Agents:** `backend/app/agents/`

### Key Dependencies
- **Backend:** FastAPI, LangChain, OpenAI, python-docx, pypdf, Jinja2
- **Frontend:** React, Axios, Mermaid.js, Vite

---

**Document Version:** 1.0
**Last Updated:** January 2026
**Maintained By:** Development Team
