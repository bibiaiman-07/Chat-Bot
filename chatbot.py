import nltk
import random
from nltk.chat.util import Chat, reflections
from textblob import TextBlob  # For spelling correction

# Define chatbot pairs
pairs = [
    # Greetings
    (r"hi|hello|hey|hii|heyy", ["Hello! How can I help you today?", "Hi there! How are you feeling?"]),
    (r"good morning|good afternoon|good evening", ["Good day to you! How are you feeling?"]),
    (r"how are you?", ["I'm doing well, thank you! How about you?"]),
    
    # Asking about Bot
    (r"what is your name?|who are you?", ["I'm your mental health support bot. You can call me Bot!"]),
    (r"what can you do?", ["I'm here to listen and support you. Feel free to talk to me."]),
    (r"are you a human?", ["No, I am a bot, but I'm here to help you as much as I can."]),
    
    # Emotions - Happy
    (r"i'm happy|i feel happy|i'm excited|i feel great", ["That's wonderful to hear! What made you happy today?", "Awesome! Keep spreading positivity!"]),
    (r"i'm feeling good|i feel fantastic", ["I'm so glad you're feeling fantastic! Keep the positivity going!"]),
    
    # Emotions - Sad
    (r"i'm sad|i feel sad|i'm upset", ["I'm sorry you're feeling this way. Do you want to talk about it?", "Sadness is hard. I'm here to listen if you want to share."]),
    (r"i'm crying|i feel like crying", ["It's okay to cry sometimes. I'm here for you."]),
    (r"i feel so empty|i feel numb", ["I'm really sorry you're feeling this way. It's okay to feel this way sometimes, but you're not alone."]),
    
    # Emotions - Stress / Anxiety
    (r"i'm stressed|i feel stressed|i'm anxious|i have anxiety", ["I'm sorry to hear you're feeling stressed. Want to talk about what's bothering you?", "Anxiety can feel overwhelming. I'm here with you."]),
    (r"i have exam stress|i'm nervous about exams", ["Exams can be stressful, but you've got this! Have you tried deep breathing?"]),
    (r"i can't stop worrying", ["Worrying can be exhausting. Have you considered some relaxation techniques like meditation?"]),
    
    # Emotions - Anger
    (r"i'm angry|i feel angry|i'm frustrated", ["Anger is a natural feeling. Want to tell me what happened?", "It's okay to feel angry. I'm here to listen without judgment."]),
    (r"i feel rage|i feel furious", ["It must be tough to feel this way. Would you like to talk about what's making you feel this way?"]),
    
    # Emotions - Depression / Hopelessness
    (r"i'm depressed|i feel depressed|i'm sad|i feel hopeless", ["I'm really sorry you're feeling this way. You're not alone.", "Please reach out to someone you trust. I'm here to listen too."]),
    (r"i feel like giving up|i want to end it all|i'm thinking of suicide|i want to die", [
        "I'm so sorry you're feeling this way. Please talk to someone you trust or a mental health professional immediately. You matter.",
        "It sounds really tough. Please remember, you don't have to face this alone. Reach out to someone right now."
    ]),
    
    # Loneliness
    (r"i'm lonely|i feel lonely", ["Loneliness can feel heavy. I'm here to chat with you anytime."]),
    (r"nobody cares about me|i feel unloved", ["You are important. Sometimes we feel invisible, but your feelings matter."]),
    (r"i have no friends", ["It’s tough to feel like that, but I'm here to listen. You're not alone."]),
    
    # Coping & Advice
    (r"how can i feel better?", ["Sometimes, talking can help. Would you like to share what's on your mind?", "Taking deep breaths or going for a walk can help. Want to try that?"]),
    (r"what should i do?", ["Start with something small. Take a deep breath, and let's talk about what's bothering you."]),
    (r"how do i relax?", ["You can try deep breathing or meditation. Have you ever tried mindfulness?"]),
    (r"how to manage stress?", ["Managing stress can start with small steps like taking breaks, talking, or doing something creative."]),
    
    # Self-Worth & Empowerment
    (r"i feel worthless", ["You are important. Your feelings matter, and you're worthy of love and care."]),
    (r"i don't like myself", ["I understand how hard that can be. It's important to remind yourself that you're enough."]),
    (r"i feel like i can't do anything right", ["It's normal to feel this way sometimes, but you're doing your best. That matters."]),
    
    # Positive Affirmations
    (r"i'm not good enough", ["You are good enough, just as you are. Don't let negative thoughts define you."]),
    (r"i am strong", ["Yes, you are! You've faced challenges before, and you'll keep moving forward."]),
    (r"i can do this", ["That's the spirit! Keep going, you are capable."]),
    
    # Gratitude
    (r"thank you|thanks", ["You're welcome! I'm always here to listen.", "I'm glad I could help!"]),
    (r"i'm grateful", ["Gratitude is beautiful. What are you grateful for?"]),
    (r"thank you for listening", ["It’s my pleasure! You are heard."]),
    
    # Asking for Support
    (r"i need help|can you help me?", ["I'm here to listen and support you. What’s going on?", "Tell me more, and I’ll do my best to help."]),
    (r"can you help me with my problems?", ["I can listen to you, and together we can explore solutions. What’s bothering you?"]),
    
    # Seeking Professional Help
    (r"should i see a therapist?", ["It could be helpful to talk to a professional if you're struggling. You're not alone in this."]),
    (r"should i talk to someone about this?", ["Yes, it's always good to talk to someone. Whether a friend, family, or professional."]),
    
    # Empathy & Support
    (r"i need someone to talk to", ["I'm here for you. Tell me what’s going on."]),
    (r"i don't know who to talk to", ["You can talk to me. I'm here to listen anytime."]),
    (r"no one understands me", ["I may not understand everything, but I can listen. Your feelings are valid."]),
    
    # Family & Relationships
    (r"my family doesn't understand me", ["I'm sorry you're feeling misunderstood. It's tough when family doesn't understand."]),
    (r"my partner is distant", ["Relationships can be difficult. It might help to talk openly with your partner."]),
    (r"i feel disconnected from my friends", ["Friendships can go through rough patches, but it’s never too late to reach out."]),
    
    # Grief & Loss
    (r"i lost someone|i'm grieving", ["I'm so sorry for your loss. Grief is a heavy emotion. I'm here to listen."]),
    (r"i can't stop crying|i feel like i can't go on", ["It's okay to grieve. Take it one day at a time, and reach out if you need help."]),
    
    # Personal Reflection
    (r"i don't know who i am", ["It’s okay to feel uncertain. Sometimes, reflecting on your values and passions helps."]),
    (r"i feel like i've lost myself", ["I hear you. Personal growth and change can be tough, but you are still discovering who you are."]),
    
    # General fallback
    (r"(.*)", ["Can you tell me more about that?", "I'm here to listen. Please continue.", "Would you like to share more?"])
]


# Correct spelling using TextBlob
def correct_spelling(text):
    blob = TextBlob(text)
    return str(blob.correct())

# Create chatbot
chat = Chat(pairs, reflections)

# 🔥 This function will be called by your Flask app
# chatbot.py

# chatbot.py

def get_bot_response(user_input):
    corrected_input = correct_spelling(user_input)
    response = None

    try:
        response = chat.respond(corrected_input)
    except Exception as e:
        print("Error in responding:", e)
        response = None

    if not response:
        response = random.choice([
            "I'm not sure what you mean, could you rephrase?",
            "Tell me more about that."
        ])

    return response

   


