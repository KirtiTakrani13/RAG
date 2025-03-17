# Retrieval Augmented Generation (RAG) Application

## Repository Cloning

Clone this repository:

```bash
git clone https://github.com/KirtiTakrani13/RAG.git
```

## Backend Environment Setup

Create a `.env` file in the `backend_llm` directory:

```bash
cd backend_llm
touch .env
```

Fill in your environment variables:

```env
OPENAI_API_KEY=your_openai_api_key
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token
```

### Obtaining API Keys:

- **OpenAI API Key**: Obtain your key from [OpenAI Platform](https://platform.openai.com/api-keys).
- **Hugging Face API Token**: Obtain your token from [Hugging Face](https://huggingface.co/settings/tokens).

> **Note**: Shyftlabs team members have been provided these API keys via email. Feel free to use those or your own OpenAI API Key.

## Frontend Environment Setup

Navigate to the frontend directory and create an `.env` file if your frontend requires environment variables:

```bash
cd ..
cd frontend
touch .env
```
Fill in your environment variables for frontend:

```env
VITE_API_URL='http://localhost:8000'
```

Update your frontend environment variables accordingly.

## Requirements

- Docker
- Docker Compose

Recommended:
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

## Building and Running the Project (With Docker)

Refer to the image below for the folder structure:

![Folder Structure](https://github.com/user-attachments/assets/53d2c9e7-0bf7-4351-85cf-be883b250596)

### Steps to Build and Run

Run the following commands from the project root directory:
Make sure you are in the project root directory before running the following commands.  
(In my case, the root directory was `kproject`.)  

```bash
docker-compose build
docker-compose up 
```

Access the frontend at: [http://localhost:3000](http://localhost:3000)

Access the backend at: [http://localhost:8000](http://localhost:8000)

----

## Steps to Build and Run (Without Docker)

If you prefer to run the project without Docker, follow these steps:

1. Ensure you have all required dependencies installed (Node.js, Python, etc.).

2. Navigate to the frontend directory and start the frontend:

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. Open a new terminal, navigate to the backend_llm directory, and create a virtual environment (if not already created):

   ```bash
   cd backend_llm
   python -m venv venv  # Create a virtual environment
   source venv/bin/activate  # Activate the virtual environment (Linux/macOS)
   # OR
   venv\Scripts\activate  # Activate the virtual environment (Windows)
   ```

4. Install the backend dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. If you encounter any dependency errors, try resolving them by:

   - Searching for solutions online (e.g., using Google or Stack Overflow).
   - Contacting the repository maintainer if the issue persists.

6. Start the backend:

   ```bash
   uvicorn app.main:app --reload
   ```

Now, you can access the frontend at [http://localhost:3000](http://localhost:3000)  
and the backend at [http://localhost:8000](http://localhost:8000).

----

## Project Features

- **Backend:**
  - FastAPI webserver.
  - Supports document uploads:
    - Local PDF files.
    - Direct PDF URL (downloads automatically).
    - HTML webpage support (e.g., [CERN HTML Example](https://info.cern.ch/hypertext/README.html)).

- **Frontend:**
  - React-based application.
  - Supports uploading local PDF documents.
  - Supports entering PDF URLs directly (auto-downloads).
  - Supports HTML webpages processing (e.g., [https://info.cern.ch/hypertext/README.html](https://info.cern.ch/hypertext/README.html)).

- **Search:** Semantic and keyword search capabilities.
- **Streaming:** Real-time streaming of the final output to the user.

### Demo Video

Watch the demo video to see the application in action:




https://github.com/user-attachments/assets/f74dffea-7266-4f36-897d-0d6b411728a4


## Assignment Requirements Status

✅ Webserver via FastAPI  
✅ Streaming support  
✅ Semantic & keyword search  
✅ PDF and HTML document upload endpoints  
✅ Frontend User Interface

## Bonus Optimizations

✅ Enhanced quality of output
✅ Reduced latency and optimized performance

## Contact & Support

For questions or issues, please open an issue in this repository or contact the maintainer directly.
email: kirtitakrani40@gmail.com 

