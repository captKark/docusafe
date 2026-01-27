import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. Load the secrets
load_dotenv()

# 2. Setup the Client
# We use the standard OpenAI client, but point it to Groq's servers
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

def test_ai_connection():
    """
    A simple test to see if the brain is working.
    """
    print("🤖 Contacting the AI Module...")
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", # High performance, open source model
            messages=[
                {"role": "system", "content": "You are a helpful backend assistant."},
                {"role": "user", "content": "Say 'Hello Docusafe Developer' and nothing else."}
            ]
        )
        
        # Extract the message
        response = completion.choices[0].message.content
        print(f"✅ Success! AI Responded: {response}")
        return True
        
    except Exception as e:
        print(f"❌ Error connecting to AI: {e}")
        return False

# This allows us to run this file directly to test it
if __name__ == "__main__":
    test_ai_connection()