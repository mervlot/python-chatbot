import sounddevice as sd
import speech_recognition as sr
import mysql.connector
from nltk.tokenize import word_tokenize
import nltk

# Download necessary NLTK data for offline use
# nltk.download('punkt')

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'mervlot',
    'password': 'Oluwaseyi999',
    'database': 'merv',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}

# Connect to MySQL database
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    print("Database connection established.")
except mysql.connector.Error as err:
    print(f"Error connecting to database: {err}")
    exit()

# Create table if it doesn't exist
try:
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS learned_phrases (
        phrase VARCHAR(255) NOT NULL,
        response TEXT NOT NULL,
        PRIMARY KEY (phrase)
    )
    ''')
    conn.commit()
    print("Table 'learned_phrases' created or already exists.")
except mysql.connector.Error as err:
    print(f"Error creating table: {err}")
    exit()

# Initialize recognizer
recognizer = sr.Recognizer()
print("Speech recognition setup complete.")

# Function to record audio using sounddevice
def listen():
    print("Say something!")
    # Record 5 seconds of audio at 44100 Hz sample rate
    audio_data = sd.rec(int(5 * 44100), samplerate=44100, channels=1, dtype='int16')
    sd.wait()  # Wait until the recording is finished
    try:
        # Convert numpy array to AudioData object for recognizer
        audio = sr.AudioData(audio_data.tobytes(), 44100, 2)
        print("Processing audio...")
        text = recognizer.recognize_sphinx(audio)
        print(f"Recognized speech: {text}")
        return text
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Sphinx error; {e}")
        return None

def learn_response(phrase, response):
    # Insert or update the learned phrase in the database
    try:
        insert_query = "INSERT INTO learned_phrases (phrase, response) VALUES (%s, %s) ON DUPLICATE KEY UPDATE response = %s"
        cursor.execute(insert_query, (phrase, response, response))
        conn.commit()
        print(f"Learned '{phrase}' with response '{response}'.")
    except mysql.connector.Error as err:
        print(f"Error learning response: {err}")

def respond(phrase):
    # Check if we have a learned response for this phrase
    try:
        cursor.execute("SELECT response FROM learned_phrases WHERE phrase = %s", (phrase,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return "I'm not sure how to respond to that."
    except mysql.connector.Error as err:
        print(f"Error responding: {err}")
        return "I encountered an error while responding."

while True:
    text = listen()
    if text:
        print(f"You said: {text}")
        
        # Tokenize the text to deal with basic phrases
        tokens = word_tokenize(text)
        if tokens and tokens[0].lower() == 'learn':
            # If the user wants to teach the AI something new
            if len(tokens) > 2:
                phrase_to_learn = ' '.join(tokens[1:-1])  # Phrase to learn
                response = tokens[-1]  # Response to the phrase
                learn_response(phrase_to_learn, response)
            else:
                print("Please provide a phrase and its response to learn.")
        else:
            # Check if we have learned this phrase before
            response = respond(text)
            print(f"AI responds: {response}")

    if input("Press 'q' to quit, any other key to continue: ").lower() == 'q':
        break

# Close database connection
cursor.close()
conn.close()
print("Database connection closed.")