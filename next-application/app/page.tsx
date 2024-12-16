"use client";
import { useEffect, useState } from "react";
import { ChatHistory } from "../types";

export default function Home() {
  const [userInput, setUserInput] = useState<string>("");
  const [chatHistory, setChatHistory] = useState<ChatHistory[]>([]);

  useEffect(() => {
    fetchChatHistory();
  }, []);

  const fetchChatHistory = async () => {
    const response = await fetch("/api/chat");
    const data: ChatHistory[] = await response.json();
    setChatHistory(data);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ userInput }),
    });
    const data = await response.json();
    setChatHistory([
      ...chatHistory,
      { user_input: userInput, bot_response: data.botResponse },
    ]);
    setUserInput("");
  };

  const handleReset = async () => {
    await fetch("/api/chat", {
      method: "DELETE",
    });
    setChatHistory([]);
  };

  return (
    <div className="container p-6 flex flex-col bg-gray-100 relative min-w-full max-h-dvh">
      <div className="flex flex-col space-y-1.5 pb-6">
        <h2 className="font-semibold text-lg tracking-tight">
          Badminton Player Interview Chatbot
        </h2>
        <p className="text-sm text-[#6b7280] leading-3">Powered by thothica</p>
      </div>
      <div className="bg-white p-6 rounded-lg shadow-2xl overflow-auto border border-[#e5e7eb] w-full flex flex-col h-dvh">
        <div
          className="overflow-auto pr-4 max-h-[400px] flex-1" // Set a max height for scrolling
          style={{ minWidth: "100%", display: "table" }}
        >
          <ul>
            {chatHistory.map((chat, index) => (
              <li key={index}>
                <strong>You:</strong> {chat.user_input} <br />
                <strong>Bot:</strong> {chat.bot_response}
              </li>
            ))}
          </ul>
        </div>
      </div>
      <form onSubmit={handleSubmit}>
        <div className="flex items-center pt-2">
          <div className="flex items-center justify-center w-full space-x-2">
            <input
              type="text"
              value={userInput}
              className="border rounded-md p-2 w-full"
              onChange={(e) => setUserInput(e.target.value)}
              placeholder="Type your question..."
            />
            <button
              className="inline-flex items-center justify-center rounded-md text-sm font-medium text-[#f9fafb] disabled:pointer-events-none disabled:opacity-50 bg-black hover:bg-[#111827E6] h-10 px-4 py-2"
              type="submit"
            >
              Send
            </button>
          </div>
        </div>
      </form>
      <button
        className="inline-flex items-center justify-center rounded-md text-sm font-medium text-[#f9fafb] disabled:pointer-events-none disabled:opacity-50 bg-black hover:bg-[#111827E6] h-10 px-4 py-2"
        onClick={handleReset}
      >
        Reset Chat History
      </button>
    </div>
  );
}
