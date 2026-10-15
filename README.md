# Customer Support AI Agent

**An AI-powered customer support platform built with RAG, LangGraph, Groq, FastAPI, FAISS, and Model Context Protocol (MCP).**

The Customer Support AI Agent is a modular application designed to automate customer support workflows through intelligent question answering, knowledge retrieval, order tracking, and support ticket creation.

By combining large language models with retrieval-augmented generation (RAG) and standardized tool integration, the system provides context-aware responses while enabling operational actions through dedicated MCP tools.

## Key Features

- **AI-Powered Responses** — Generate natural-language responses using Groq-hosted large language models.
- **Retrieval-Augmented Generation (RAG)** — Ground responses in company policies, FAQs, and internal documentation.
- **Semantic Search** — Retrieve relevant document chunks using Hugging Face embeddings and FAISS.
- **Agent Orchestration** — Coordinate retrieval, reasoning, and tool execution with LangGraph.
- **Order Tracking** — Retrieve order status and estimated delivery information through MCP tools.
- **Support Ticket Creation** — Escalate customer issues through a dedicated ticket tool.
- **MCP Integration** — Separate tool providers from the AI application using the Model Context Protocol.
- **REST API** — Expose customer-support functionality through FastAPI.
- **Input Validation** — Validate API requests and responses using Pydantic.
- **Automated Testing** — Test application behavior with pytest.
- **Containerized Deployment** — Package and run services with Docker and Docker Compose.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Groq | Large language model inference |
| LangChain | LLM and tool integration |
| LangGraph | Agent workflow orchestration |
| Hugging Face | Text embedding generation |
| FAISS | Vector indexing and similarity search |
| FastAPI | REST API framework |
| Pydantic | Data validation and configuration |
| Model Context Protocol | Standardized client-server tool communication |
| Pytest | Automated testing |
| Docker | Application containerization |
| Docker Compose | Multi-service orchestration |

## System Architecture

```text
                         Customer
                            |
                            v
                     FastAPI REST API
                            |
                            v
                         LangGraph
                            |
                            v
                       Groq LLM
                            |
                  +---------+---------+
                  |                   |
                  v                   v
             RAG Pipeline         MCP Client
                  |                   |
                  v                   v
              FAISS Index         MCP Server
                  |                   |
                  v             +-----+------+
            Knowledge Base      |            |
                                v            v
                           Order Tools   Ticket Tools
                                |            |
                                v            v
                           Order Data   Ticket System
```

### Request Lifecycle

1. A customer submits a question through the REST API.
2. FastAPI validates the incoming request.
3. LangGraph coordinates the agent workflow.
4. The agent retrieves relevant knowledge-base content when needed.
5. The LLM determines whether a tool call is appropriate.
6. The MCP client sends the tool request to the MCP server.
7. The MCP server executes the requested operation and returns its result.
8. The agent generates a response and returns it through the API.

Depending on the question and implemented routing logic, the workflow may use document retrieval, MCP tools, or both.

## Project Structure

```text
customer-support-agent/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── schemas.py
│   ├── ingestion.py
│   ├── vector_store.py
│   ├── prompts.py
│   ├── tools.py
│   ├── graph.py
│   ├── mcp_client.py
│   └── main.py
│
├── mcp_server/
│   ├── __init__.py
│   ├── server.py
│   ├── order_tools.py
│   └── ticket_tools.py
│
├── knowledge_base/
│   ├── returns_policy.md
│   ├── shipping_policy.txt
│   └── faq.pdf
│
├── data/
│   └── faiss_index/
│
├── tests/
│   ├── __init__.py
│   ├── test_tools.py
│   └── test_api.py
│
├── .env.example
├── .gitignore
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── run_indexing.py
├── run_agent.py
└── README.md
```

### Core Modules

| Module | Responsibility |
|---|---|
| `app/main.py` | FastAPI application and HTTP endpoints |
| `app/graph.py` | LangGraph workflow and agent orchestration |
| `app/ingestion.py` | Document loading and text splitting |
| `app/vector_store.py` | FAISS index creation and retrieval |
| `app/prompts.py` | LLM instructions and prompt templates |
| `app/tools.py` | Agent tool definitions and integrations |
| `app/mcp_client.py` | MCP session management and tool invocation |
| `app/schemas.py` | Request and response schemas |
| `app/config.py` | Environment-based application configuration |
| `mcp_server/server.py` | MCP server and tool registration |
| `mcp_server/order_tools.py` | Order lookup operations |
| `mcp_server/ticket_tools.py` | Support ticket operations |

## Prerequisites

Install the following before running the project:

- Python 3.11 or another version supported by the dependencies
- pip
- Git
- A Groq API key
- Docker Desktop with Docker Compose, for containerized deployment

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd customer-support-agent
```

If the repository already exists locally, open a terminal in the project directory instead.

### 2. Create and activate a virtual environment

**Windows — Git Bash**

```bash
python -m venv .venv
source .venv/Scripts/activate
```

**Windows — PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Ensure `requirements.txt` contains the dependencies required by the implemented application, including the relevant LangChain integrations, LangGraph, FAISS, Hugging Face embeddings, FastAPI, Uvicorn, the MCP SDK, and pytest.

### 4. Configure environment variables

Create a `.env` file in the project root based on `.env.example`.

```dotenv
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile

MCP_SERVER_URL=http://127.0.0.1:8001/mcp
```

Use a model currently available to your Groq account and ensure the application configuration reads the corresponding environment variables.

**Security:** Never commit `.env` files, API keys, or other credentials to version control.

## Knowledge Base and RAG

The application can use company documentation as a knowledge source for customer questions.

### Supported document formats

- PDF
- TXT
- Markdown

Add the supported files to the `knowledge_base/` directory.

### Build the vector index

```bash
python run_indexing.py
```

The indexing workflow should:

1. Load documents from the knowledge base.
2. Split documents into smaller text chunks.
3. Generate embeddings for the chunks.
4. Store vectors and associated document metadata in FAISS.
5. Persist the index for subsequent retrieval.

The index location should match the configuration in `app/vector_store.py`.

Rebuild the index when the source documents change. Ensure that PDFs are valid documents rather than empty placeholder files.

## Running Locally

Run the MCP server and FastAPI application in separate terminals. Activate the virtual environment in each terminal before executing commands.

### 1. Start the MCP server

```bash
python -m mcp_server.server
```

The development server uses the following endpoint:

```text
http://127.0.0.1:8001/mcp
```

Available tools:

- `lookup_order` — retrieve order status and estimated delivery information.
- `create_ticket` — create a support ticket for an issue requiring assistance.

### 2. Verify MCP connectivity

Open another terminal and run:

```bash
python -m app.mcp_client
```

The client should initialize a session, discover available tools, and execute its configured test call.

The MCP endpoint is a protocol endpoint, not a conventional webpage. Use an MCP client or MCP Inspector to test connectivity.

### 3. Start the FastAPI application

Open another terminal and run:

```bash
uvicorn app.main:app --reload
```

If the application starts successfully, the local endpoints are typically available at:

| Resource | URL |
|---|---|
| API base URL | `http://127.0.0.1:8000` |
| Interactive API documentation | `http://127.0.0.1:8000/docs` |
| Alternative API documentation | `http://127.0.0.1:8000/redoc` |

These URLs assume the corresponding routes and documentation are enabled in `app/main.py`.

## API Usage

The following examples illustrate a possible API contract. Confirm the actual request and response schemas in `app/main.py` and `app/schemas.py`.

### Submit a customer question

**Endpoint:** `POST /chat`

Example request:

```json
{
  "question": "What is your return policy?"
}
```

Illustrative response:

```json
{
  "answer": "Eligible items may be returned according to the applicable return policy.",
  "success": true
}
```

The response depends on the configured knowledge base, agent workflow, and model output.

### Example customer queries

**Knowledge-base questions**

- What is your return policy?
- How long does shipping take?
- Can I return an item after delivery?

**Order-related questions**

- Can you check the status of order ORD1001?
- What is the estimated delivery date for ORD1002?

**Support escalation**

- My delivered item arrived damaged. Can you create a support ticket?

The agent should route each request to the appropriate retrieval or tool workflow according to its implementation.

## MCP Tool Reference

### `lookup_order`

Retrieves order status and estimated delivery information.

Example input:

```json
{
  "order_id": "ORD1001"
}
```

Illustrative output:

```text
Order ORD1001 is shipped.
Estimated delivery: 2026-10-18
```

### `create_ticket`

Creates a support ticket for an issue that requires human assistance.

Example input:

```json
{
  "issue": "The delivered item arrived damaged.",
  "order_id": "ORD1001"
}
```

Illustrative output:

```text
Support ticket created successfully.
Ticket ID: TICKET-1001
Status: Open
```

The actual output and persistence behavior depend on the implementation of the corresponding business functions.

### MCP integration responsibilities

- **MCP server:** Exposes tools through the Model Context Protocol.
- **MCP client:** Discovers tools, establishes sessions, and sends tool-call requests.
- **AI agent:** Selects the appropriate operation as part of its tool-calling workflow.
- **Business functions:** Execute the requested operation against the configured data source or business system.

Tool discovery by itself does not automatically enable LLM tool selection. The MCP tools must be integrated into the agent's execution workflow.

## Testing

Run the complete test suite:

```bash
python -m pytest -v
```

Run a specific test module:

```bash
python -m pytest tests/test_api.py -v
```

Display test output:

```bash
python -m pytest -s
```

Tests can cover API validation, document ingestion, retrieval behavior, tool execution, and error handling.

For reliable automated testing, mock external model calls where appropriate and test live MCP connectivity separately as an integration test.

## Docker Deployment

Docker Compose can run the API and MCP server as separate services.

### Build and start the services

```bash
docker compose up --build
```

### View logs

```bash
docker compose logs -f
```

View an individual service:

```bash
docker compose logs -f api
docker compose logs -f mcp-server
```

### Stop the services

```bash
docker compose down
```

### Container networking

When both services run in the same Compose network, the API container should connect to the MCP server through its Compose service name, for example:

```text
http://mcp-server:8001/mcp
```

Configure the MCP server to bind to `0.0.0.0` inside its container, and configure `MCP_SERVER_URL` appropriately for the deployment environment.

For local development outside Docker, the client can use:

```text
http://127.0.0.1:8001/mcp
```

Use Docker volumes if the FAISS index must persist across container recreation. Ensure the Compose configuration, Dockerfile, and application commands match the actual repository.

## Security and Reliability

Before exposing the application to real customers, consider implementing:

- Secure secret management for API keys and credentials.
- API authentication and rate limiting.
- Authorization checks before retrieving customer-specific order information.
- Input validation and controlled tool execution.
- Persistent storage for support tickets and order records.
- Request timeouts, structured logging, and error monitoring.
- Graceful handling of LLM-provider and MCP connection failures.
- Protection against malicious instructions embedded in retrieved documents.
- Automated tests for invalid inputs, permissions, and failure scenarios.
- Appropriate access controls for customer data and stored vector indexes.

## Current Scope and Limitations

The project's capabilities depend on the integrations and implementations configured in the repository.

If order lookup or ticket creation uses in-memory sample data, the results are illustrative and may not persist after a process restarts. Production usage requires persistent storage or integration with the appropriate business systems.

Likewise, actual retrieval quality, tool selection, API behavior, and deployment readiness should be verified against the implemented code and automated tests.

## Future Enhancements

Potential improvements include:

- Integration with live order management systems.
- Database-backed ticket management.
- Conversation history and session management.
- Human-agent handoff and escalation workflows.
- Authentication and role-based access control.
- Streaming responses.
- RAG evaluation and answer-quality monitoring.
- Observability, tracing, and performance metrics.
- CI/CD automation and cloud deployment.

## License

Add an appropriate open-source or proprietary license before distributing the project. Ensure that third-party dependencies and included documentation are used according to their applicable licenses and permissions.

---

**Customer Support AI Agent**  
*Bringing together intelligent retrieval, agent orchestration, and standardized tool integration to streamline customer support workflows.*
