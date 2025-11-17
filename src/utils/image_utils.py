from src.models.gemini_client import MedAIclient

client = MedAIclient()

def read_prescription(image_path:str):
    """
    Extract Text from prescription image using gemini
    Cleans handwriting and return structured info.
    """
    prompt = """
      You are an AI assistant that extracts ONLY the readable information from
    handwritten or printed medical prescriptions.
    
    Return the output in a clean structured format:
    - Patient Name (if visible)
    - Medicines List
    - Dosage Instructions
    - Additional Notes
    
    Do NOT provide any diagnosis. Only extract text.
    """
    
    try:
        result = client.analyze_image(image_path,prompt)
        return result
    except Exception as e:
        return f"Error in reading prescription{str(e)}"
