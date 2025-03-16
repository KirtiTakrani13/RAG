import { useState } from "react";
import { useImmer } from "use-immer";
import api from "@/api";
import { parseSSEStream } from "@/utils";
import ChatMessages from "@/components/ChatMessages";
import ChatInput from "@/components/ChatInput";

function Chatbot() {
  const [messages, setMessages] = useImmer([]);
  const [newMessage, setNewMessage] = useState("");

  const isLoading = messages.length && messages[messages.length - 1].loading;

  async function submitNewMessage() {
    const trimmedMessage = newMessage.trim();
    if (!trimmedMessage || isLoading) return;

    setMessages((draft) => [
      ...draft,
      { role: "user", content: trimmedMessage },
      { role: "assistant", content: "", loading: true },
    ]);
    setNewMessage("");

    //

    try {
      // Request streaming response from API
      const stream = await api.queryRAG(trimmedMessage, 3);

      // Process the stream in real-time
      for await (const textChunk of parseSSEStream(stream)) {
        try {
          // Parse the JSON chunk
          const data = JSON.parse(textChunk);

          if (data.response) {
            // Append the response chunk to the assistant's message
            setMessages((draft) => {
              draft[draft.length - 1].content += data.response;
            });
          }

          if (data.metadata) {
            // Handle metadata (if needed)
            console.log("Metadata:", data.metadata);
          }
        } catch (err) {
          console.error("Error parsing JSON chunk:", err);
        }
      }

      // Mark completion
      setMessages((draft) => {
        draft[draft.length - 1].loading = false;
      });
    } catch (err) {
      console.error("Error:", err);
      setMessages((draft) => {
        draft[draft.length - 1].loading = false;
        draft[draft.length - 1].content = "Error fetching response.";
      });
    }
  }

  return (
    <div className="relative grow flex flex-col gap-6 pt-6">
      {messages.length === 0 && (
        <div className="mt-3 font-urbanist text-primary-blue text-xl font-light space-y-2">
          <p>👋 Welcome!</p>
          <p>I am powered by the latest technology.</p>
          <p>Ask me anything about the uploaded pdf.</p>
        </div>
      )}
      <ChatMessages messages={messages} isLoading={isLoading} />
      <ChatInput
        newMessage={newMessage}
        isLoading={isLoading}
        setNewMessage={setNewMessage}
        submitNewMessage={submitNewMessage}
      />
    </div>
  );
}

export default Chatbot;
