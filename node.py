import nltk
from nltk.chat.util import Chat, reflections
import sys
import json

# Download necessary NLTK data (make sure to run this once or preload the data)
nltk.download('punkt')

# Define patterns and responses
patterns = [
    (r'hello|hi|hey', ['Hello!', 'Hi there!', 'Hey!']),
    (r'how are you', ['I am good, thanks for asking.', 'Doing well, how about you?']),
    (r'what can you do', ['I can help with simple questions or just chat with you!']),
    (r'quit', ['Goodbye! Come back soon!'])
]

# Create the chatbot
chatbot = Chat(patterns, reflections)

# Function to get chatbot response from stdin
def get_response(input_text):
    return chatbot.respond(input_text)

if __name__ == "__main__":
    # Read from stdin for integration with Node.js
    input_data = sys.stdin.read()
    input_json = json.loads(input_data)
    user_input = input_json.get('message', '')

    response = get_response(user_input)

    # Write to stdout for Node.js to read
    sys.stdout.write(json.dumps({"response": response}))
    sys.stdout.flush()