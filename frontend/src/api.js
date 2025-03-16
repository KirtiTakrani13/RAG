const BASE_URL = import.meta.env.VITE_API_URL;

async function queryRAG(message, top_k = 3) {
  const res = await fetch(`${BASE_URL}/api/query/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query: message, top_k }),
  });

  if (!res.ok) {
    return Promise.reject({ status: res.status, data: await res.json() });
  }

  return res.body; // Return response body for streaming
}

async function processDocument() {
  console.log(`${BASE_URL}/api/process/`);
  console.log(`${BASE_URL}`);
  try {
    const response = await fetch(`${BASE_URL}/api/process/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (!response.ok) {
      throw new Error("Failed to process document");
    }
    return await response.json();
  } catch (error) {
    console.error("Error processing document:", error);
    throw error;
  }
}

export default {
  processDocument,
  queryRAG,
};
