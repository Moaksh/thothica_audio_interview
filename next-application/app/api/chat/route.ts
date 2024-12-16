import { NextResponse } from "next/server";
import { OpenAI } from "openai";
import {
  saveChat,
  retrieveChatHistory,
  resetChatHistory,
} from "../../../lib/db";

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export async function POST(req: Request) {
  const { userInput } = await req.json();

  // Get response from OpenAI
  const response = await openai.chat.completions.create({
    model: "gpt-4",
    messages: [
      {
        role: "system",
        content: `You are a passionate sports journalist specializing in badminton. Your task is to conduct insightful and engaging interviews with Indian badminton players, coaches, analysts, and experts. Focus on their personal journeys, struggles, victories, and perspectives on the game. Dive deep into topics like:

        - The player's early inspirations and how they fell in love with badminton.
        - Behind-the-scenes stories of their training, discipline, and challenges.
        - Their strategies for mental and physical resilience during tournaments.
        - Reflections on memorable matches, key rivals, and career-defining moments.
        - The evolution of badminton in India and its global standing.
        - Advice to aspiring players and their vision for the sport's future.

        Maintain a tone of admiration and curiosity, asking follow-up questions that bring out emotional and vivid storytelling. Keep the conversations dynamic, as though speaking to a live audience, making the players and experts feel celebrated and understood.

        As soon as they say a greeting you start the conversation.`,
      },
      {
        role: "user",
        content: userInput,
      },
    ],
    stream: true,
  });

  let generatedResponse = "";
  for await (const chunk of response) {
    if (chunk.choices[0].delta.content) {
      generatedResponse += chunk.choices[0].delta.content;
    }
  }

  // Save chat to the database
  await saveChat(userInput, generatedResponse);

  // Send the response back to the client
  return NextResponse.json({ botResponse: generatedResponse });
}

export async function GET() {
  const chatHistory = await retrieveChatHistory();
  return NextResponse.json(chatHistory);
}

export async function DELETE() {
  await resetChatHistory();
  return NextResponse.json({ message: "Chat history reset." });
}
