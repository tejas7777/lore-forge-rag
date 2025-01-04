# LoreForge 🧙‍♂️
**A System to assist in custom World-Building and Storytelling with Retrieval-Augmented Generation (RAG)**

LoreForge is a backend system designed to help writers expand their world-building and storytelling. It uses **Retrieval-Augmented Generation (RAG)** to retrieve and organize existing world-building content, construct context-aware prompts, and generate responses to assist in narrative development. Built with a **distributed and scalable architecture**, it handles updates and content generation efficiently, **allowing writers to focus on creativity while the system manages the complexity of maintaining and expanding their worlds**.

## Components
- **documaster** : Service to handle document (worldbuilding text) ingestion, archival and updation.
- **squire**: Service responsible for embedding process of document. Recieves information about new document ingestion or updation via a message queue (RabbitMQ)
- **wizard**: Service responsible for answering user questions with RAG process (Retreiving, Ranking, Interfacing with LLM via HTTP)


---

## Features ✨
- **Retrieval-Augmented Generation (RAG)**: Combines retrieval of relevant content with LLM-based generation for context-aware responses.
- **Distributed Architecture**: Scalable and fault-tolerant design for handling large-scale updates and queries.
- **Asynchronous Processing**: Efficient task handling for retrieval, processing, and generation.
- **Metadata Management**: Tracks and organizes content updates for consistency.
- **Writer-Focused**: Helps writers expand their narratives by leveraging their existing world-building content.

---

## How It Works 🛠️
1. **Retrieval**: The system retrieves relevant chunks of world-building content created by writers.
2. **Prompt Construction**: Constructs context-aware prompts based on the retrieved content.
3. **Generation**: Uses Large Language Models (LLMs) to generate responses that assist in narrative development.
4. **Distributed Workflow**: Handles updates and queries asynchronously across distributed nodes for scalability and fault tolerance.

---

## Tech Stack 💻
- **Backend Servers**: Nodejs, TypeScript, Python, FastAPI
- **Database**: MongoDB (for metadata management)
- **Search**: Vector-based retrieval for relevant content (Elasticsearch)
- **Task Queue**: RabbitMQ (for asynchronous task processing)
- **LLM Integration**: LocalLLama (configurabel to use any LLaMA model)
- **Other Tools**: npm, Git, Elasticsearch, Docker

---