# Setup Guide

## Prerequisites

- Python 3.13
- Anthropic API key ([get one here](https://console.anthropic.com/))

## Installation Steps

1. **Clone the repository**
   ```bash
   cd claude-playground
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   copy .env.example .env
   ```
   
   Edit `.env` and add your API key:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

5. **Test installation**
   ```bash
   cd projects/01-basic-chat
   python main.py
   ```

## Troubleshooting

- **ImportError**: Make sure virtual environment is activated
- **API Key Error**: Check that `.env` file exists and has valid key
- **Module not found**: Run `pip install -r requirements.txt`
