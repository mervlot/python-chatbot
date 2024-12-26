import nltk
from nltk.chat.util import Chat, reflections
import json
import mysql.connector

# Download necessary NLTK data
nltk.download('punkt')

# MySQL Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="yourusername",
        password="yourpassword",
        database="yourdatabase"
    )

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
    response = chatbot.respond(input_text)
    
    # Example of database interaction
    with get_db_connection() as connection:
        cursor = connection.cursor()
        # Insert the user's message into the database
        add_message = "INSERT INTO chat_log (user_input, ai_response) VALUES (%s, %s)"
        cursor.execute(add_message, (input_text, response))
        connection.commit()
        cursor.close()
    
    return response

if __name__ == "__main__":
    # Read from stdin for integration with Node.js
    input_data = sys.stdin.read()
    input_json = json.loads(input_data)
    user_input = input_json.get('message', '')

    response = get_response(user_input)

    # Write to stdout for Node.js to read
    sys.stdout.write(json.dumps({"response": response}))
    sys.stdout.flush()