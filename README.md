# Claude Playground

Experimental projects using Claude SDK for building AI agents and applications.

## Setup

1. Install Python 3.13
2. Create virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   copy .env.example .env  # Windows
   # cp .env.example .env  # Linux/Mac
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

## Projects

- **01-basic-chat**: Simple Claude chat interface
- **02-tool-use**: Claude with function calling
- **03-agentic-workflow**: Multi-step agent with tools
- **04-streaming-responses**: Real-time streaming responses

## Running a Project

```bash
cd projects/01-basic-chat
python main.py
```

## Documentation

See `docs/` folder for detailed guides and best practices.

## Quick Start

```bash
# Activate virtual environment
venv\Scripts\activate

# Run basic chat example
cd projects/01-basic-chat
python main.py
```
