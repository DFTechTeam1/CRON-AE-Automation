#!/bin/sh

# Show usage information
show_help() {
  echo "Usage: sh scripts/run_mounter.sh [ --development | --staging | --production ]"
  echo ""
  echo "--development    Use .env.development"
  echo "--staging        Use .env.staging"
  echo "--production     Use .env.production"
  echo "--help           Show this help message"
  echo ""
  echo "Example: sh scripts/run_mounter.sh --development"
  exit 0
}

# Set project directories
PROJECT_DIR="$HOME/Project/CRON-AE-Automation"
ENV_DIR="$PROJECT_DIR/env"
MOUNT_DIR="$PROJECT_DIR/mount"

# Parse arguments
case "$1" in
  --development)
    ENV_FILE="$ENV_DIR/.env.development"
    ;;
  --staging)
    ENV_FILE="$ENV_DIR/.env.staging"
    ;;
  --production)
    ENV_FILE="$ENV_DIR/.env.production"
    ;;
  --help|-h)
    show_help
    ;;
  *)
    echo "Error: Invalid argument"
    show_help
    ;;
esac

# Load environment variables
if [ ! -f "$ENV_FILE" ]; then
  echo "Error: Environment file $ENV_FILE not found."
  exit 1
fi

export $(grep -v '^#' "$ENV_FILE" | xargs)

# Check required env vars
if [ -z "$NAS_USERNAME" ] || [ -z "$NAS_PASSWORD" ] || [ -z "$ROOT_PATH" ]; then
  echo "Error: NAS_USERNAME, NAS_PASSWORD, or ROOT_PATH is not set in $ENV_FILE."
  exit 1
fi

# Parse ROOT_PATH: //192.168.100.104/Database_Asset_3/ae_auto_asset
NAS_IP=$(echo "$ROOT_PATH" | cut -d'/' -f3)
SHARE_NAME=$(echo "$ROOT_PATH" | cut -d'/' -f4)
SUB_PATH=$(echo "$ROOT_PATH" | cut -d'/' -f5)

# Prepare mount destination
MOUNT_DEST="$MOUNT_DIR/$NAS_IP/$SHARE_NAME/$SUB_PATH"
mkdir -p "$MOUNT_DEST"

echo "Mounting $ROOT_PATH to $MOUNT_DEST..."

sudo mount -t cifs "$ROOT_PATH" "$MOUNT_DEST" -o username="$NAS_USERNAME",password="$NAS_PASSWORD",vers=3.0

# Verify mount
if mountpoint -q "$MOUNT_DEST"; then
  echo "Mounted successfully: $ROOT_PATH -> $MOUNT_DEST"
else
  echo "Error: Failed to mount $ROOT_PATH"
  exit 1
fi
