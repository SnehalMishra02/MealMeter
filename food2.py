import os
from dotenv import load_dotenv
from io import BytesIO

# Load environment variables from .env file
load_dotenv()

import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file, mime_type):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.read()

        image_parts = [
            {
                "mime_type": mime_type,  # Use the provided MIME type
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    

import openai

openai.api_key = 'sk-proj-ByESQHjhUDwTjTQP5RftT3BlbkFJH56H90bCtZ8rDVz5rEYs'

def generate(input):


    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=input,
        max_tokens=50
    )


    return response.choices[0].text.strip()
