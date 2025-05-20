# AE-Automation
CRON-AE-Automation

## Project Structures ##
```
├── job\             # Cron job execution scripts.
├── logs\            # Log files generated during execution.
├── scripts\         # Shell scripts for automation and orchestration.
├── services\        # Code for interacting with external services.
├── src\             # Core business logic and main application modules.
├── utils\           # Shared utility and helper functions.
├── pyproject.toml   # Project configuration and dependency declarations.
```

# Project Setup Instructions
This project was developed using WSL (Ubuntu 24.04.2 LTS on Windows 11) and Python v3.12.3. Before you begin, ensure you have UV installed as your Python package manager.

## Prerequisites

- **Python v3.12.3**
- **UV**

## Setup steps

1. **Initialize the project and install dependencies**
    ```
    sh scripts\setup.sh
    ```
2. **Run full data extraction**
    ```
    sh scripts\run_executor.sh --path job\insert.py --env <environment>
    ```
3. **Run data updater**
    ```
    sh scripts\run_executor.sh --path job\update.py --env <environment>
    ```

## Replace <environment> with one of:
- development
- staging
- production


# Project Features
- [x] Extracts all data for automated processing.
- [x] Updates all relevant data for automation workflows.


# Repo Owner? #
* Bastian Armananta
