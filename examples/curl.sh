#!/bin/sh
# Image, then video from that image, then poll until done. Needs curl and jq.
set -e
: "${SPICYAPI_KEY:?export SPICYAPI_KEY first}"
API=https://api.spicyapi.com/v1
auth="Authorization: Bearer $SPICYAPI_KEY"

image_url=$(curl -sf "$API/images/generations" -H "$auth" -H "Content-Type: application/json" \
  -d '{"model": "spicy-image-1", "prompt": "a woman on a beach at golden hour, photorealistic", "size": "832*1216", "n": 1}' \
  | jq -r '.data[0].url')
echo "image: $image_url"

task=$(curl -sf "$API/videos/generations" -H "$auth" -H "Content-Type: application/json" \
  -d "{\"model\": \"spicy-motion-2\", \"prompt\": \"slow build, steady rhythm\", \"image_url\": \"$image_url\", \"resolution\": \"720P\", \"duration\": 5}" \
  | jq -r '.id')
echo "task: $task"

while :; do
  res=$(curl -sf "$API/videos/tasks/$task" -H "$auth")
  status=$(echo "$res" | jq -r '.status')
  echo "status: $status"
  case "$status" in
    succeeded) echo "$res" | jq -r '.output.video_url'; break ;;
    failed) echo "$res" | jq -r '.error'; exit 1 ;;
  esac
  sleep 12
done
