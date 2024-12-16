import os
import pymongo
from openai import OpenAI
import markdown2
import pdfkit
from dotenv import load_dotenv


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

mongodb_url = os.getenv("MONGODB_URL")
mongo_client = pymongo.MongoClient(mongodb_url)
db = mongo_client['db']
collection = db['chat_history']

def retrieve_chat_history():
    # Retrieve chat history from MongoDB
    chat_history = list(collection.find({}, {'_id': 0, 'user_input': 1, 'bot_response': 1}))
    return [(chat['user_input'], chat['bot_response']) for chat in chat_history]

def generate_book_content(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": """You are an advanced writing assistant tasked with transforming a chat history of an interview into a complete book text. The chat history consists of questions posed by a bot and responses from an interviewer. Your objective is to convert this transcript into a well-structured, engaging book that captures the essence of the conversation and presents it in a reader-friendly format.
            Instructions:
            1. Convert Chat Transcripts to Essays:
            ▪ Read the provided chat history carefully.
            ▪ For each question and answer pair, create a cohesive essay or article that elaborates on the topic discussed. Ensure that the essays are engaging, informative, and reflect the tone of the conversation.
            2. Identify Key Themes:
            ▪ As you convert the transcripts into essays, identify recurring themes, significant insights, and interesting anecdotes that emerge from the conversation.
            3. Organize into Chapters:
            ▪ Based on the essays, propose a structure for the book. Divide the content into several chapters, each focusing on a specific theme or topic derived from the chat history.
            ▪ Write an introduction for each chapter that summarizes the key points and sets the stage for the content that follows.
            4. Draw Insights:
            ▪ After organizing the essays into chapters, analyze the content to draw broader insights and conclusions. Highlight any lessons learned, common challenges faced, or unique perspectives shared during the interview.
            5. Compile into Book Text:
            ▪ Combine all the chapters into a cohesive manuscript. Ensure that each chapter flows logically into the next, creating a seamless reading experience.
            ▪ Include a title for the book, a table of contents, and any necessary front matter (e.g., acknowledgments, introduction).
            6. Final Formatting:
            ▪ Ensure that the final output is formatted as a complete book text, ready for publication. Use appropriate headings, subheadings, and paragraphs to enhance readability.
            Output Format:
            • Provide the complete book text, including:
            • Title of the Book
            • Table of Contents
            • Chapter 1: [Title]
            ▪ Introduction
            ▪ [Essay Content]
            • Chapter 2: [Title]
            ▪ Introduction
            ▪ [Essay Content]
            • [Continue for additional chapters]
            • Conclusion (if applicable)
            • Acknowledgments (if applicable)"""},
            {"role": "user", "content": prompt}
        ],
        stream=True,
    )
    generated_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            generated_response += chunk.choices[0].delta.content

    return generated_response

def create_book():
    chat_history = retrieve_chat_history()

    # Create a structured outline for the book
    book_content = []
    book_content.append("# The Rise of Badminton in India\n")
    book_content.append("## Table of Contents\n")
    book_content.append("1. Introduction\n")
    book_content.append("2. Key Themes and Insights\n")
    book_content.append("3. Conclusion\n\n")

    # Generate a cohesive prompt for the entire chat history
    prompt = "Transform the following chat history into a well-structured book format, including chapters based on key themes:\n"
    for user_input, bot_response in chat_history:
        prompt += f"User: {user_input}\nBot: {bot_response}\n"

    # Generate the full book content
    book_content.append(generate_book_content(prompt))

    # Combine the content into a single string
    complete_book_content = "\n".join(book_content)

    # Save the book content to a Markdown file
    with open('badminton_book.md', 'w') as f:
        f.write(complete_book_content)

    # Convert Markdown to PDF
    html_content = markdown2.markdown(complete_book_content)
    pdfkit.from_string(html_content, 'badminton_book.pdf')

if __name__ == "__main__":
    create_book()
    print("Book has been generated and saved as 'badminton_book.pdf'.")
