import asyncio
import json
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.utils.retrieval import PROMPT_TEMPLATE, generate_response, initialize_llm, retrieve_documents
from app.utils.global_vars import global_state, GlobalState
from app.utils.logging_config import get_logger
from app.model.query_request import QueryRequest

logger = get_logger()
router = APIRouter()

# Dependency function
def get_global_state():
    return global_state

@router.post("/query/")
async def query_rag(request: QueryRequest, state: GlobalState = Depends(get_global_state)):
    """
    SSE Streaming Endpoint for RAG pipeline.
    """
    query = request.query
    top_k = request.top_k
    logger.info(f"Query: {query}, Top K: {top_k}")

    dbnn = state.get_vector_db()
    all_documents = state.all_documents

    async def event_generator():
        if not dbnn:
            logger.error("Vector database not initialized")
            yield "data: {\"error\": \"Vector database not initialized\"}\n\n"
            return

        try:
            # Step 1: Retrieve documents
            retrieved_results = retrieve_documents(dbnn, all_documents, query, top_k)
            if not retrieved_results:
                logger.warning("No relevant documents found.")
                yield "data: {\"response\": \"No relevant documents found.\"}\n\n"
                return

            # Step 2: Initialize LLM
            llm = initialize_llm()

            # Step 3: Generate response
            response_content = generate_response(llm, PROMPT_TEMPLATE, retrieved_results, query)

            # Step 4: Stream response content chunk by chunk
            chunk_size = 100
            for i in range(0, len(response_content), chunk_size):
                chunk = response_content[i: i + chunk_size]
                formatted_chunk = json.dumps({"response": chunk})
                yield f"data: {formatted_chunk}\n\n"
                await asyncio.sleep(0.05)  # Simulate streaming delay

            # Step 5: Stream metadata at the end
            metadata = {}
            yield f"data: {json.dumps({'metadata': metadata})}\n\n"

        except Exception as e:
            logger.error(f"Unexpected error in RAG pipeline: {e}")
            yield f"data: {json.dumps({'error': 'Internal server error'})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
