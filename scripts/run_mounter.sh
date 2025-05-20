#!/bin/sh

# Show usage information
show_help() {
  echo "Usage: sh scripts/run_mounter.sh --env [ development | staging | production ]"
  echo ""
  echo "--env       Set environment context (development, staging, or production)"
  echo "--help, -h  Show this help message"
  echo ""
  echo "Example: sh scripts/run_mounter.sh --env development"
  exit 0
}

# Set project directories
PROJECT_DIR="$HOME/Project/CRON-AE-Automation"
ENV_DIR="$PROJECT_DIR/env"
MOUNT_DIR="$PROJECT_DIR/mount"

# Default empty
ENVIRONMENT=""

# Parse arguments
while [ "$#" -gt 0 ]; do
  case "$1" in
    --env)
      ENVIRONMENT="$2"
      shift 2
      ;;
    --help|-h)
      show_help
      ;;
    *)
      echo "Error: Invalid argument '$1'"
      show_help
      ;;
  esac
done

# Validate environment value
if [ -z "$ENVIRONMENT" ]; then
  echo "Error: Missing value for --env"
  show_help
fi

if [ "$ENVIRONMENT" != "development" ] && [ "$ENVIRONMENT" != "staging" ] && [ "$ENVIRONMENT" != "production" ]; then
  echo "Error: Invalid environment '$ENVIRONMENT'. Must be one of: development, staging, production."
  exit 1
fi

# Resolve environment file
ENV_FILE="$ENV_DIR/.env.$ENVIRONMENT"

# Load environment variables
if [ ! -f "$ENV_FILE" ]; then
  echo "Error: Environment file $ENV_FILE not found."
  exit 1
fi

export $(grep -v '^#' "$ENV_FILE" | xargs)

# Check required env vars
if [ -z "$NAS_USERNAME" ] || [ -z "$NAS_PASSWORD" ] || [ -z "$NAS_PATH" ]; then
  echo "Error: NAS_USERNAME, NAS_PASSWORD, or NAS_PATH is not set in $ENV_FILE."
  exit 1
fi

# Parse NAS_PATH: //192.168.100.104/Database_Asset_3/ae_auto_asset
NAS_IP=$(echo "$NAS_PATH" | cut -d'/' -f3)
SHARE_NAME=$(echo "$NAS_PATH" | cut -d'/' -f4)
SUB_PATH=$(echo "$NAS_PATH" | cut -d'/' -f5)

# Prepare mount destination
MOUNT_DEST="$MOUNT_DIR/$NAS_IP/$SHARE_NAME/$SUB_PATH"
mkdir -p "$MOUNT_DEST"

echo "Mounting $NAS_PATH to $MOUNT_DEST..."

sudo mount -t cifs "$NAS_PATH" "$MOUNT_DEST" -o username="$NAS_USERNAME",password="$NAS_PASSWORD",vers=3.0

# Verify mount
if mountpoint -q "$MOUNT_DEST"; then
  echo "Mounted successfully: $NAS_PATH -> $MOUNT_DEST"
else
  echo "Error: Failed to mount $NAS_PATH"
  exit 1
fi
