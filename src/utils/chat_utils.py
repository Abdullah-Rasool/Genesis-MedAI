from src.models.gemini_client import MedAIclient

client = MedAIclient()

def chat_assistant(question:str):
    """
     Ask any general health-related questions (safe, non-diagnostic responses).
    """
     # Prompt for Gemini
    prompt = f"""
    You are a friendly health assistant AI.
    Answer the user's question safely.
    - Do NOT provide any medical diagnosis.
    - Give general, informative, and safe advice.
    User's question: {question}
    """
    try:
        result = client.ask_text(prompt)
        return result
    except Exception as e:
        return f"Error in chat assistance {str(e)}"
    
