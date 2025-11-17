from src.models.gemini_client import MedAIclient

client = MedAIclient()

def transcribe_audio(audio_path:str):
    """
    Converts audio into text using Gemini.
    """
    
    prompt = """
    You are a transcription assistant. 
        Convert the following medical conversation audio into clean text.
        Do NOT add your own words. Just transcribe exactly.
    """
    
    try:
        result = client.analyze_audio(audio_path,prompt)
        return result
    except Exception as e:
        return f"Error facing during audio transcription {str(e)}"
    
def generate_notes(raw_text:str):
    """
    Convert raw conversation text into structured, safe, non-diagnostic notes.
    """
    prompt = f"""
    Convert the following conversation into structured medical visit notes.
        IMPORTANT:
        - Do NOT diagnose.
        - Do NOT prescribe medicines.
        - Only summarize what the conversation already contains.

        Conversation:
        {raw_text}

        Return this format:
        - Patient Concerns
        - Doctor Suggestions (non-diagnostic)
        - Follow-up Reminders
        """
    try:
        result = client.ask_text(prompt)
        return result
    except Exception as e:
        return f"Error Generating Notes{str(e)}"
    
    