#!/bin/bash

MODULE_NAME=$1
MODULE_TYPE=$2  # strategy, intel, risk, etc.

if [ -z "$MODULE_NAME" ] || [ -z "$MODULE_TYPE" ]; then
  echo "❌ Usage: ./curl_loader.sh <module_name> <folder>"
  echo "Example: ./curl_loader.sh options_ai strategy"
  exit 1
fi

DEST="../$MODULE_TYPE/${MODULE_NAME}.py"
URL="https://raw.githubusercontent.com/patelp320/superbot-trading-core/main/$MODULE_TYPE/${MODULE_NAME}.py"

echo "📦 Downloading $MODULE_NAME → $DEST"
curl -s -o "$DEST" "$URL"

if [ $? -eq 0 ]; then
  echo "✅ $MODULE_NAME loaded into $MODULE_TYPE/"
else
  echo "❌ Download failed"
fi

