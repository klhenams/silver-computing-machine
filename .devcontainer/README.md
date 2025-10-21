# Dev Container Setup

This project includes a complete dev container setup for VS Code that provides a consistent development environment.

## Features

- **Python 3.11** with all project dependencies pre-installed
- **PostgreSQL** with pgvector extension for vector operations
- **Pre-commit hooks** for code quality enforcement
- **VS Code extensions** for Python development, debugging, and formatting
- **Debugging configurations** for FastAPI and pytest
- **Code formatting** with Black and import sorting with isort
- **Linting** with Flake8 and type checking with MyPy

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started) installed and running
- [VS Code](https://code.visualstudio.com/) with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Setup

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <your-repo-url>
   cd silver-computing-machine
   ```

2. **Open in Dev Container**:
   - Open the project in VS Code
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "Dev Containers: Reopen in Container"
   - Select the option and wait for the container to build

3. **Environment Setup**:
   - Copy `.env.example` to `.env` and configure your environment variables
   - Add your Hugging Face API key to the `.env` file

### What's Included

- **Development dependencies**: pytest, black, isort, flake8, mypy, pre-commit
- **Database**: PostgreSQL with pgvector extension running on port 5432
- **API**: FastAPI application accessible on port 8000
- **Code quality tools**: Pre-commit hooks automatically installed

### Available Commands

Once inside the dev container, you can use:

```bash
# Install development dependencies (done automatically)
pip install -e .[dev]

# Run the FastAPI application
uvicorn src.support_system.main:app --host 0.0.0.0 --port 8000 --reload

# Run tests
pytest tests/ -v

# Format code
black src/
isort src/

# Run linting
flake8 src/
mypy src/

# Run pre-commit hooks manually
pre-commit run --all-files
```

### Debugging

Three debug configurations are available:
- **Python: FastAPI** - Debug the FastAPI application
- **Python: Current File** - Debug the currently open Python file
- **Python: Pytest** - Debug tests with pytest

### Database Access

The PostgreSQL database is accessible at:
- **Host**: `postgres` (from within containers) or `localhost` (from host)
- **Port**: `5432`
- **Database**: `support_system`
- **Username**: `postgres`
- **Password**: `password`

### Port Forwarding

The dev container automatically forwards:
- Port **8000** for the FastAPI application
- Port **5432** for PostgreSQL database access

### Troubleshooting

1. **Container won't start**: Ensure Docker is running and you have sufficient disk space
2. **Port conflicts**: Make sure ports 8000 and 5432 aren't already in use on your host
3. **Permission issues**: The dev container runs as user `vscode` with UID 1000
4. **Dependencies not found**: Try rebuilding the container with "Dev Containers: Rebuild Container"

### File Watching

The dev container mounts your source code with the `cached` consistency for better performance on macOS and Windows while maintaining file watching capabilities for hot reload.
