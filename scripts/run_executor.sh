#!/bin/bash

show_help() {
    echo "Usage: sh scripts/run_executor.sh [ --path <filepath> ] | [ --env <environment> ] | [ --help ]"
    echo ""
    echo "--path        Path to the Python script to execute"
    echo "--env         Set environment context (development, staging, or production)"
    echo "--help, -h    Show this help message"
    echo ""
    echo "Example: sh scripts/run_executor.sh --path /path/to/script.py --env development"
    exit 0
}

PROJECT_DIR="$HOME/Project/CRON-AE-Automation"
ENV_FILE=""
TARGET_SCRIPT=""

# Parse arguments
while [ "$#" -gt 0 ]; do
    case "$1" in
        --path)
            TARGET_SCRIPT="$2"
            shift 2
            ;;
        --env)
            case "$2" in
                development)
                    ENV_FILE="$PROJECT_DIR/env/.env.development"
                    echo "Using development environment configuration"
                    ;;
                staging)
                    ENV_FILE="$PROJECT_DIR/env/.env.staging"
                    echo "Using staging environment configuration"
                    ;;
                production)
                    ENV_FILE="$PROJECT_DIR/env/.env.production"
                    echo "Using production environment configuration"
                    ;;
                *)
                    echo "Error: Invalid environment '$2'"
                    show_help
                    ;;
            esac
            shift 2
            ;;
        --help|-h)
            show_help
            ;;
        *)
            echo "Error: Unknown option '$1'"
            show_help
            ;;
    esac
done

# Validate required arguments
if [ -z "$TARGET_SCRIPT" ] || [ -z "$ENV_FILE" ]; then
    echo "Error: Both --path and --env are required."
    show_help
fi

# Validate file exists
if [ ! -f "$TARGET_SCRIPT" ]; then
    echo "Error: The specified file does not exist: $TARGET_SCRIPT"
    exit 1
fi

# Activate virtual environment based on OS
echo "Checking OS Environment."
if grep -qEi "(Microsoft|WSL)" /proc/version &>/dev/null; then
    echo "WSL detected."
    . "$PROJECT_DIR/.venv/bin/activate"
else
    case "$OSTYPE" in
        linux*|darwin*)
            echo "Unix-based OS detected."
            source "$PROJECT_DIR/.venv/bin/activate"
            ;;
        *)
            echo "Unsupported OS."
            exit 1
            ;;
    esac
fi
echo "Virtual environment activated."

# Load environment variables
if [ -f "$ENV_FILE" ]; then
    echo "Loading environment variables from $ENV_FILE"
    export $(grep -v '^#' "$ENV_FILE" | xargs)
else
    echo "Error: Env file not found: $ENV_FILE"
    exit 1
fi

# Run the target script
echo "Running script: $TARGET_SCRIPT"
python3 "$TARGET_SCRIPT"

if [ $? -ne 0 ]; then
    echo "Error: Failed to run script: $TARGET_SCRIPT"
    exit 1
fi
