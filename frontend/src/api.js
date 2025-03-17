const BASE_URL = import.meta.env.VITE_API_URL;

// Query about the PDF
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

// Function to upload PDF from a URL
async function uploadPDFUrl(fileUrl) {
  const formData = new FormData();
  formData.append("file_url", fileUrl);

  const res = await fetch(`${BASE_URL}/api/upload-pdf-from-url/`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    return Promise.reject({ status: res.status, data: await res.json() });
  }

  return res.json(); // Return response as JSON
}

// Processing uploaded pdf function
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

// Upload PDF function
async function uploadPDF(file) {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch(`${BASE_URL}/api/upload-pdf/`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Failed to upload PDF");
    }

    return await response.json();
  } catch (error) {
    console.error("File upload error:", error);
    throw error;
  }
}

/**
 * Upload an HTML website URL for processing.
 * @param {string} url - The URL of the HTML website to process.
 * @returns {Promise<Object>} - The response from the server.
 */
async function uploadHtmlUrl(url) {
  const res = await fetch(`${BASE_URL}/api/process-html/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }), // Send the URL in the request body
  });

  if (!res.ok) {
    return Promise.reject({ status: res.status, data: await res.json() });
  }

  return res.json(); // Return the parsed JSON response
}

export default {
  processDocument,
  uploadPDF,
  queryRAG,
  uploadPDFUrl,
  uploadHtmlUrl,
};
