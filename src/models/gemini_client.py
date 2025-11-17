
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()


class MedAIclient:
        def __init__(self):
            gemini_api_key = os.getenv("GEMINI_API_KEY")
            if not gemini_api_key:
                raise ValueError("GEMINI_API_KEY is missing in your environment variables")
            self.client = genai.Client(api_key=gemini_api_key)
            self.model = "gemini-2.0-flash"
        
        # for text 
        def ask_text(self, text:str) -> str:
            response = self.client.models.generate_content(model=self.model, contents=text)
            return response.text
        
        # for image + text
        def analyze_image(self, image_path:str,task_prompt:str) -> str:
            with open(image_path, "rb") as img:
                response = self.client.models.generate_content(
                    model=self.model, 
                    contents=[types.Part.from_bytes(data = img.read(), mime_type = "image/png"), task_prompt])
                return response.text
        
        # audio + text
        def analyze_audio(self, audio_path:str,task_prompt:str) -> str:
            with open(audio_path, "rb") as audio:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=[types.Part.from_bytes(data=audio.read(), mime_type = "audio/wav"), task_prompt]
                )
                return response.text
            
        # video + text
        def analyze_video(self, video_path:str,task_prompt:str) -> str:
            with open(video_path, "rb") as video:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=[types.Part.from_bytes(data = video.read(), mime_type = "video/mp4"), task_prompt]
                )
                return response.text 