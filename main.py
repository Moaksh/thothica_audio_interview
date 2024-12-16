import os
import streamlit as st
from openai import OpenAI
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)
db = client['db']
collection = db['chat_history']

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client_openai = OpenAI(api_key=OPENAI_API_KEY)



def save_chat(user_input, bot_response):
    collection.insert_one({
        'user_input': user_input,
        'bot_response': bot_response
    })

def retrieve_chat_history():
    chat_history = list(collection.find({}, {'_id': 0, 'user_input': 1, 'bot_response': 1}))
    return [(chat['user_input'], chat['bot_response']) for chat in chat_history]

def reset_chat_history():
    collection.delete_many({})

def get_bot_response(user_input):
    response = client_openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": """You are a passionate sports journalist specializing in badminton. Your task is to conduct insightful and engaging interviews with Indian badminton players, coaches, analysts, and experts. Focus on their personal journeys, struggles, victories, and perspectives on the game. Dive deep into topics like:

            - The player's early inspirations and how they fell in love with badminton.
            - Behind-the-scenes stories of their training, discipline, and challenges.
            - Their strategies for mental and physical resilience during tournaments.
            - Reflections on memorable matches, key rivals, and career-defining moments.
            - The evolution of badminton in India and its global standing.
            - Advice to aspiring players and their vision for the sport's future.

            Maintain a tone of admiration and curiosity, asking follow-up questions that bring out emotional and vivid storytelling. Keep the conversations dynamic, as though speaking to a live audience, making the players and experts feel celebrated and understood.

            As soon as they say a greeting you start the conversation."""},
            {"role": "user", "content": user_input}
        ],
        stream=True,
    )

    generated_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            generated_response += chunk.choices[0].delta.content

    return generated_response


st.title("Badminton Player Interview Chatbot")
st.write("Type your questions below and press Enter to chat with the badminton player.")


user_input = st.text_input("You:", "")

if user_input:
    if user_input.strip():
        with st.spinner('Waiting for response...'):
            bot_response = get_bot_response(user_input)
            save_chat(user_input, bot_response)
            st.write(f"**Bot:** {bot_response}")
    else:
        st.warning("Please enter a valid question.")

st.subheader("Chat History")
chat_history = retrieve_chat_history()
for user_input, bot_response in chat_history:
    st.write(f"**You:** {user_input}")
    st.write(f"**Bot:** {bot_response}")

if st.button("Reset Chat History"):
    reset_chat_history()
    st.success("Chat history has been reset.")
