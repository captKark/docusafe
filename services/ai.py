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

def summarize_document(text: str) -> str:
    """
    Uses the AI to generate a summary of the given document content.
    """
    print("🤖 Generating document summary...")

    # Call the AI to summarize
    try:
        # we asssume that the conten must be long, so we ask for a concise summary
        chat_completion=client.chat.completions.create(
            messages=[
                {
                    "role":"system",
                    "content": "You are an expert document summarizer. Provide concise and clear summaries. Summarize the following text in 2-3 concise sentences."
                },
                {
                    "role":"user",
                    "content":text,
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content or "Summary could not be generated."
    except Exception as e:
        print(f"❌ Error generating summary: {e}")
        return "Summary could not be generated."