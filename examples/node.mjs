// Image, then video, then poll. Node 18+, no dependencies.
// export SPICYAPI_KEY=sk-spicy-... && node examples/node.mjs
const KEY = process.env.SPICYAPI_KEY;
if (!KEY) throw new Error("export SPICYAPI_KEY first");
const API = "https://api.spicyapi.com/v1";

async function call(path, body) {
  const res = await fetch(API + path, {
    method: body ? "POST" : "GET",
    headers: { Authorization: `Bearer ${KEY}`, "Content-Type": "application/json" },
    body: body && JSON.stringify(body),
  });
  const json = await res.json();
  if (!res.ok) throw new Error(`${res.status} ${json.error?.message ?? ""}`);
  return json;
}

const img = await call("/images/generations", {
  model: "spicy-image-1",
  prompt: "a woman on a beach at golden hour, photorealistic",
  size: "832*1216",
  n: 1,
});
const imageUrl = img.data[0].url;
console.log("image:", imageUrl, "cost:", img.cost_usd);

let task = await call("/videos/generations", {
  model: "spicy-motion-2",
  prompt: "slow build, steady rhythm",
  image_url: imageUrl,
  resolution: "720P",
  duration: 5,
});

while (task.status !== "succeeded" && task.status !== "failed") {
  await new Promise((r) => setTimeout(r, 12000));
  task = await call(`/videos/tasks/${task.id}`);
  console.log("status:", task.status);
}
if (task.status === "failed") throw new Error(task.error);
console.log("video:", task.output.video_url);
