import nltk
from nltk.chat.util import Chat, reflections
import json

# Download necessary NLTK data (make sure to run this once or preload the data)
#nltk.download('punkt')

# Define patterns and responses
patterns = [
    (r'hello|hi|hey', ['Hello!', 'Hi there!', 'Hey!']),
    (r'who made you', ['I was made by MervAI by Oguunmuyiwa Muhammad']),
    (r'how are you', ['I am good, thanks for asking.', 'Doing well, how about you?']),
    (r'what can you do', ['I can help with simple questions or just chat with you!']),
    (r'quit', ['Goodbye! Come back soon!'])
]

# Create the chatbot
chatbot = Chat(patterns, reflections)

# Function to get chatbot response
def get_response(input_text):
    return chatbot.respond(input_text)

if __name__ == "__main__":
    print("Merva: Hello! I'm here to help. Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        response = get_response(user_input)
        print("Merva:", response)