export async function onRequest(context) {
  return new Response("Not Found", {
    status: 404,
    headers: {
      "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
      "Content-Type": "text/plain"
    }
  });
}
