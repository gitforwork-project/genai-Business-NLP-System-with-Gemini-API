import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeminiConfig:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Configure the API
        genai.configure(api_key=self.api_key)
        
        # Initialize models
        self.generative_model = genai.GenerativeModel('gemini-2.0-flash')
        self.embeddings_model = "models/text-embedding-004"
    
    def get_generative_model(self):
        return self.generative_model
    
    def get_embeddings_model(self):
        return self.embeddings_model

# Test the configuration
if __name__ == "__main__":
    try:
        config = GeminiConfig()
        print("✅ Gemini API configured successfully!")
        
        # Test with a simple prompt
        model = config.get_generative_model()
        response = model.generate_content("Say hello in a professional business tone.")
        print(f"Test response: {response.text}")
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
