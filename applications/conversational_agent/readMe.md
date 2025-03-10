# Conversational Agent

## Application Structure
```
conversational_agent/
├── agent.py          # Conversational agent implementation
├── cli.py           # Command-line interface
├── web_app.py       # Web interface with FastAPI
├── static/          # Static files for web interface
│   └── index.html   # Web user interface
├── prompts.py       # Predefined prompts definition
├── requirements.txt # Project dependencies
└── .env            # Environment variables configuration
```

## Installation and Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure `.env` file:
```
OPENAI_API_KEY=your_openai_api_key
```

## Usage

### Web Interface (Recommended)
1. Start the server:
```bash
python web_app.py
```
2. Open a browser and navigate to `http://localhost:8000`

### CLI Interface
```bash
python cli.py [options]
```

Available options:
- `--session <session_name>` : Session identifier (default: default_user)
- `--prompt-type <type>` : Predefined prompt type (teacher, french, coder, writer)
- `--system-prompt <prompt>` : Custom system prompt
- `--db-path <path>` : Path to database file

Example:
```bash
python cli.py --session user1 --prompt-type teacher
```

## Main Features

### Web Interface
- Multiple session management
- System prompt visualization and modification
- Conversation history
- Predefined prompts selection
- Responsive and intuitive interface
- Visual feedback system messages

### Key Components
1. **Conversational Agent** (`agent.py`)
   - Language model management (OpenAI)
   - Conversation memory management
   - System prompt processing
   - User session management

2. **Web Interface** (`web_app.py` + `static/index.html`)
   - REST API with FastAPI
   - Modern UI with Tailwind CSS
   - Asynchronous request handling
   - Advanced feature modals

3. **CLI Interface** (`cli.py`)
   - Interactive commands
   - Command-line argument support
   - Session management
   - Administrative commands

### Memory Management
- Persistent conversation storage
- Session-based history
- Custom system prompts management
- Multiple simultaneous user support

## Available CLI Commands
- `quit` : Exit application
- `history` : Display conversation history
- `prompt` : Display current system prompt
- `set_prompt` : Set new system prompt
- `use_prompt <type>` : Use predefined prompt
- `list_prompts` : Display available predefined prompts
- `reset` : Reset conversation
- `list_sessions` : List all available sessions
- `switch_session <session_id>` : Switch to another session
- `help` : Display help message

## Development Notes
- Application uses FastAPI for REST API
- Web interface uses Tailwind CSS for styling
- Sessions are persistent using SQLite
- Full UTF-8 character support
- Error handling and confirmation messages
