"""Images and chat through the OpenAI SDK, video over plain HTTP.

pip install openai requests
export SPICYAPI_KEY=sk-spicy-...
"""
import os
import time

import requests
from openai import OpenAI

KEY = os.environ["SPICYAPI_KEY"]
API = "https://api.spicyapi.com/v1"
client = OpenAI(api_key=KEY, base_url=API)

img = client.images.generate(
    model="spicy-image-1",
    prompt="a woman on a beach at golden hour, photorealistic",
    size="1024*1024",
    n=1,
)
image_url = img.data[0].url
print("image:", image_url)

# Video is not an OpenAI endpoint, so call it directly.
headers = {"Authorization": f"Bearer {KEY}"}
task = requests.post(
    f"{API}/videos/generations",
    headers=headers,
    json={
        "model": "spicy-motion-2",
        "prompt": "slow build, steady rhythm",
        "image_url": image_url,
        "resolution": "720P",
        "duration": 5,
    },
    timeout=60,
)
task.raise_for_status()
task_id = task.json()["id"]

while True:
    res = requests.get(f"{API}/videos/tasks/{task_id}", headers=headers, timeout=60).json()
    print("status:", res["status"])
    if res["status"] == "succeeded":
        print("video:", res["output"]["video_url"])
        break
    if res["status"] == "failed":
        raise SystemExit(res["error"])
    time.sleep(12)

stream = client.chat.completions.create(
    model="spicy-chat-1",
    messages=[{"role": "user", "content": "hey"}],
    stream=True,
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="", flush=True)
print()
