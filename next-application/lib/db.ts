import { MongoClient } from "mongodb";
import { ChatHistory } from "../types";

const uri = process.env.MONGODB_URI as string; // MongoDB connection string
const client = new MongoClient(uri);
const dbName = "db";

// Initialize the MongoDB client
let db: any;

export async function connectToDatabase() {
  if (!db) {
    await client.connect();
    db = client.db(dbName);
  }
  return db;
}

export async function initDb() {
  await connectToDatabase();
}

export async function saveChat(userInput: string, botResponse: string) {
  const database = await connectToDatabase();
  const collection = database.collection<ChatHistory>("chat_history");
  await collection.insertOne({
    user_input: userInput,
    bot_response: botResponse,
  });
}

export async function retrieveChatHistory(): Promise<ChatHistory[]> {
  const database = await connectToDatabase();
  const collection = database.collection<ChatHistory>("chat_history");
  return await collection.find({}).toArray();
}

export async function resetChatHistory() {
  const database = await connectToDatabase();
  const collection = database.collection<ChatHistory>("chat_history");
  await collection.deleteMany({});
}
