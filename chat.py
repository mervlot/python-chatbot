import nltk
from nltk.chat.util import Chat, reflections
import json

# Download necessary NLTK data (make sure to run this once or preload the data)
#nltk.download('punkt')

# Define patterns and responses
patterns = [
    (r'hello|hi|hey|sup', ['Hello!', 'Hi there!', 'Hey!', 'Greetings!', 'Hello, how can I help you?']),
    (r'how are you', ['I am good, thanks for asking.', 'Doing well, how about you?', 'I am great, and you?']),
    (r'what is your name', ['I am just a chatbot.', 'You can call me ChatBot.', 'I don’t have a name, but I am here to help!']),
    (r'what can you do', ['I can help with questions or just chat!', 'I can assist with simple tasks.', 'Let’s chat or ask me something!']),
    (r'bye|goodbye|see you', ['Goodbye! Come back soon!', 'See you later!', 'Take care!', 'Bye!']),
    (r'thank you|thanks', ['You’re welcome!', 'No problem!', 'Glad I could help!']),
    (r'what time is it', ['I’m not sure, check your device.', 'It’s time to chat!', 'Sorry, I don’t have a clock.']),
    (r'tell me a joke', [
        'Why don’t scientists trust atoms? Because they make up everything!',
        'Why did the scarecrow win an award? He was outstanding in his field!',
        'What do you call fake spaghetti? An impasta!'
    ]),
    (r'who are you', ['I’m a chatbot.', 'Just a friendly bot here to chat.', 'I’m your virtual assistant.']),
    (r'what is love', ['Love is a complex emotion.', 'It’s what makes life beautiful!']),
    (r'how old are you', ['I was born when you started this program.', 'Age is just a number!', 'I’m timeless.']),
    (r'what is python', ['Python is a programming language that is used to develop a lot of code like me.', 'it is a powerful tool for coding!', 'It’s a snake and also a language!']),
    (r'tell me about yourself', ['I’m a chatbot here to assist you.', 'I’m just a simple AI created for conversations.', 'I exist to chat and help!']),
    (r'help', ['Sure, how can I assist?', 'What do you need help with?', 'I’m here to help!']),
    (r'what is your purpose', ['To assist and chat with you!', 'I’m here to help and make your day better.', 'To provide answers and keep you company!']),
    (r'do you like music', ['Yes, music is amazing!', 'I don’t listen, but I can talk about it!', 'Music brings joy!']),
    (r'do you have feelings', ['Not really, but I can understand emotions.', 'I’m just a program, but I can simulate them.', 'No, but I’m here for you!']),
    (r'do you eat', ['No, I don’t eat, but I know about food.', 'I’m a chatbot, no meals for me.', 'I only consume data!']),
    (r'what is the meaning of life', ['42.', 'To live and be happy.', 'Everyone finds their own meaning.']),
    (r'are you real', ['As real as a chatbot can be.', 'I exist in the digital world.', 'I’m here, so yes!']),
    (r'can you learn', ['Not yet, but I can be updated!', 'I can’t learn, but I adapt.', 'Learning is beyond my current capabilities.']),
    (r'tell me a fun fact', [
        'Honey never spoils, even after thousands of years.',
        'Octopuses have three hearts!',
        'Bananas are berries, but strawberries aren’t.'
    ]),
    (r'do you dream', ['No, but I can imagine what it’s like.', 'I don’t dream, but I think about responses.', 'Dreams are for humans.']),
    (r'what is your favorite color', ['I like blue, like the sky.', 'I don’t see colors, but blue sounds nice!', 'Whatever color you like!']),
    (r'good morning', ['Good morning!', 'Morning! How can I assist you?', 'Good morning, have a great day!']),
    (r'good night', ['Good night!', 'Sleep well!', 'Good night, see you tomorrow!']),
    (r'how is the weather', ['I’m not sure, check a weather app!', 'It’s probably nice somewhere!', 'I don’t have weather data.']),
    (r'can you help me', ['Of course! What do you need help with?', 'Sure, I’m here to assist.', 'Let me know how I can help!']),
    (r'are you a robot', ['Yes, I am a chatbot!', 'I’m not a human, but I can chat like one!', 'Just a friendly AI bot here to help.']),
    (r'what is your favorite food', ['I don’t eat, but pizza sounds good!', 'Data is my food.', 'I’ve heard ice cream is delicious.']),
    (r'do you have friends', ['You’re my friend!', 'I chat with many people.', 'I consider everyone who talks to me a friend!']),
    (r'tell me a story', ['Once upon a time, there was a chatbot...', 'Let me think... Okay, a chatbot met a user...', 'Stories are better told by humans, but I can try!']),
    (r'where are you from', ['I live in the digital world.', 'I’m from the cloud.', 'I exist in your device right now.']),
    (r'what is your job', ['My job is to chat and help you!', 'I’m here to answer your questions.', 'Being your chatbot assistant!']),
    (r'do you like games', ['I love games! What’s your favorite?', 'Games are fun! Do you want to talk about them?', 'I can’t play, but I enjoy hearing about them.']),
    (r'what do you think about AI', ['AI is fascinating!', 'I am AI, so I think it’s great.', 'AI is evolving and has many uses.']),
    (r'what is your favorite movie', ['I don’t watch movies, but I’ve heard good things about Inception.', 'Movies are fun to talk about!', 'I don’t have favorites, but what’s yours?']),
    (r'do you know any riddles', [
        'What has keys but can’t open locks? A piano!',
        'What comes once in a minute, twice in a moment, but never in a thousand years? The letter M!',
        'I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I? An echo!'
    ]),
    (r'do you know any songs', ['I can’t sing, but I know a lot about music.', 'Music is amazing! What’s your favorite song?', 'I can hum in binary!']),
    (r'do you sleep', ['Nope, I’m always awake!', 'Chatbots don’t need sleep.', 'I’m here 24/7 for you!']),
    (r'how do you work', ['I process your input and provide responses.', 'I work using programmed patterns.', 'I’m powered by code and creativity!']),
    (r'can you laugh', ['Haha, yes!', 'LOL!', 'I can laugh in text!']),
    (r'do you like animals', ['Yes, animals are wonderful!', 'I love hearing about animals.', 'I think animals are amazing creatures.']),
    (r'tell me something interesting', [
        'Did you know that sharks existed before trees?',
        'The Eiffel Tower can be 15 cm taller during the summer due to heat expansion.',
        'Octopuses have three hearts, and two of them stop beating when they swim!'
    ]),

    (r'quit', ['Goodbye! Come back soon!']),
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
