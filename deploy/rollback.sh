#!/bin/bash
set -e

TAG=${1:?Usage: ./deploy/rollback.sh <image-tag>}
HOST=${EC2_HOST:?EC2_HOST is not set}
KEY=${EC2_SSH_KEY_PATH:?EC2_SSH_KEY_PATH is not set}

echo "Rolling back to: $TAG"

ssh -i "$KEY" ubuntu@"$HOST" \
  "cd ~/app-django && API_TAG=$TAG docker compose pull && API_TAG=$TAG docker compose up -d"

echo "Verifying..."
sleep 5
curl -f "http://$HOST:8000/api/health/" && echo "Rollback successful."
