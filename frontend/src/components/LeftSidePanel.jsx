import { useState } from "react";
import { FaFilePdf } from "react-icons/fa"; // Import a PDF file icon from react-icons
import api from "@/api"; // Import API functions

function LeftSidePanel() {
  const [file, setFile] = useState(null);
  const [isUrlMode, setIsUrlMode] = useState(false);
  const [url, setUrl] = useState("");
  const [processing, setProcessing] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [isHtmlMode, setIsHtmlMode] = useState(false); // New state for HTML mode
  const [htmlUrl, setHtmlUrl] = useState(""); // New state for HTML URL

  // Handle file selection and upload
  const handleFileUpload = async (event) => {
    const uploadedFile = event.target.files[0];
    if (!uploadedFile || uploadedFile.type !== "application/pdf") {
      alert("Please upload a valid PDF file.");
      return;
    }

    // Sanitize filename: remove spaces and disallowed characters
    let fileName = uploadedFile.name.replace(/\s+/g, ""); // Remove spaces
    fileName = fileName.replace(/[^a-zA-Z0-9_.-]/g, ""); // Keep only safe characters

    // Ensure it starts with a lowercase letter
    if (!/^[a-z]/.test(fileName)) {
      fileName = "a" + fileName; // Prepend 'a' if it doesn't start with lowercase
    }

    // Create a new File object with the modified name
    const modifiedFile = new File([uploadedFile], fileName, {
      type: uploadedFile.type,
    });

    setFile(modifiedFile);
    await uploadFile(modifiedFile);
  };

  // Upload file via API
  const uploadFile = async (selectedFile) => {
    if (!selectedFile) return;

    setUploading(true);
    try {
      const response = await api.uploadPDF(selectedFile);

      if (response?.filename) {
        alert(`Upload Successful: ${response.filename}`);
      } else {
        throw new Error("Unexpected response from server.");
      }
    } catch (error) {
      console.error("Upload error:", error);
      alert("Failed to upload PDF.");
    } finally {
      setUploading(false);
    }
  };

  // Handle URL input change
  const handleUrlChange = (event) => {
    setUrl(event.target.value);
  };

  const handleUrlSubmit = async () => {
    // Basic URL validation
    try {
      new URL(url); // This will throw an error if the URL is invalid
    } catch (error) {
      console.error("Error: ", error);
      alert("Please enter a valid URL.");
      return;
    }

    if (!url) {
      alert("Please enter a valid URL.");
      return;
    }

    setUploading(true);
    try {
      const response = await api.uploadPDFUrl(url);
      if (response?.filename) {
        alert(
          `PDF Name : ${response.filename} \nStatus : ${response.status} in DB`
        );
      } else {
        throw new Error("Unexpected response from server.");
      }
    } catch (error) {
      console.error("Error downloading PDF:", error);
      alert("Failed to download PDF from URL.");
    } finally {
      setUploading(false);
    }
  };

  // Handle HTML URL input change
  const handleHtmlUrlChange = (event) => {
    setHtmlUrl(event.target.value);
  };

  // Handle HTML URL submission
  const handleHtmlUrlSubmit = async () => {
    // Basic URL validation
    try {
      new URL(htmlUrl); // This will throw an error if the URL is invalid
    } catch (error) {
      console.error("Error: ", error);
      alert("Please enter a valid HTML website URL.");
      return;
    }

    if (!htmlUrl) {
      alert("Please enter a valid HTML website URL.");
      return;
    }

    setUploading(true);
    try {
      // Call the API to process the HTML website URL
      const response = await api.uploadHtmlUrl(htmlUrl);

      // Check if the response contains the expected message
      if (response?.message) {
        alert(`Success: ${response.message}`);
      } else {
        throw new Error("Unexpected response from server.");
      }
    } catch (error) {
      console.error("Error processing HTML website:", error);

      // Display a user-friendly error message
      if (error.status === 400) {
        alert("Invalid URL provided. It must start with http:// or https://");
      } else if (error.status === 500) {
        alert("Failed to process the HTML website. Please try again later.");
      } else {
        alert("Failed to process HTML website.");
      }
    } finally {
      setUploading(false);
    }
  };

  // Process document function
  const handleProcess = async () => {
    setProcessing(true);
    try {
      console.log("Processing started...");
      const data = await api.processDocument(); // Use function directly
      console.log("Processing finished:", data);
      alert(data.message);
    } catch (error) {
      console.error("Error in processing:", error);
      alert("Error processing documents.");
    } finally {
      setProcessing(false);
    }
  };

  // Format file size in a human-readable way
  const formatFileSize = (sizeInBytes) => {
    if (sizeInBytes < 1024) return `${sizeInBytes} B`;
    if (sizeInBytes < 1024 * 1024)
      return `${(sizeInBytes / 1024).toFixed(2)} KB`;
    return `${(sizeInBytes / (1024 * 1024)).toFixed(2)} MB`;
  };

  return (
    <div className="w-1/4 bg-gray-50 p-6 border-r border-gray-200">
      {/* Welcome Message */}
      <div className="mt-6 font-urbanist text-primary-blue text-xl font-light space-y-2">
        <p>Please Upload File or Enter URL!</p>
      </div>

      {/* Toggle Checkbox for PDF URL */}
      <div className="mt-4 flex items-center space-x-2">
        <input
          type="checkbox"
          id="toggle-mode"
          checked={isUrlMode}
          onChange={() => {
            setIsUrlMode(!isUrlMode);
            setIsHtmlMode(false); // Ensure HTML mode is off when PDF URL mode is toggled
          }}
          className="w-4 h-4"
        />
        <label htmlFor="toggle-mode" className="text-sm text-gray-700">
          Enter PDF URL instead of uploading a file
        </label>
      </div>

      {/* Toggle Checkbox for HTML URL */}
      <div className="mt-4 flex items-center space-x-2">
        <input
          type="checkbox"
          id="toggle-html-mode"
          checked={isHtmlMode}
          onChange={() => {
            setIsHtmlMode(!isHtmlMode);
            setIsUrlMode(false); // Ensure PDF URL mode is off when HTML mode is toggled
          }}
          className="w-4 h-4"
        />
        <label htmlFor="toggle-html-mode" className="text-sm text-gray-700">
          Enter HTML Website URL
        </label>
      </div>

      {/* Conditional Rendering Based on Checkbox State */}
      {isUrlMode ? (
        // PDF URL Input Mode
        <div className="mt-4">
          <input
            type="url"
            placeholder="Enter PDF URL"
            value={url}
            onChange={handleUrlChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-blue"
          />
          <button
            onClick={handleUrlSubmit}
            className="mt-2 w-full bg-primary-blue text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors"
          >
            Submit PDF URL
          </button>
        </div>
      ) : isHtmlMode ? (
        // HTML URL Input Mode
        <div className="mt-4">
          <input
            type="url"
            placeholder="Enter HTML Website URL"
            value={htmlUrl}
            onChange={handleHtmlUrlChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-blue"
          />
          <button
            onClick={handleHtmlUrlSubmit}
            className="mt-2 w-full bg-primary-blue text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors"
          >
            Submit HTML Website URL
          </button>
        </div>
      ) : (
        // File Upload Mode
        <>
          <label className="mt-4 cursor-pointer bg-primary-blue text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors block text-center">
            Upload PDF
            <input
              type="file"
              accept="application/pdf"
              className="hidden"
              onChange={handleFileUpload}
            />
          </label>

          {/* File Display */}
          {file && (
            <div className="mt-4 flex items-center space-x-3 p-3 bg-white rounded-lg shadow-sm">
              {/* File Icon */}
              <div className="text-red-600">
                <FaFilePdf className="w-8 h-8" />
              </div>

              {/* File Details */}
              <div>
                <p className="text-sm font-medium text-gray-900">{file.name}</p>
                <p className="text-xs text-gray-500">
                  {formatFileSize(file.size)}
                </p>
              </div>
            </div>
          )}
          {uploading && (
            <p className="text-sm text-gray-500 mt-2">Uploading...</p>
          )}
        </>
      )}

      {/* Hide Process button when HTML mode is active */}
      {!isHtmlMode && (
        <button
          onClick={handleProcess}
          className="mt-4 w-full bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
          disabled={processing}
        >
          {processing ? "Processing..." : "Process"}
        </button>
      )}
    </div>
  );
}

export default LeftSidePanel;
