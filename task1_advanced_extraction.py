import os
import base64
import json
from PIL import Image
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# Load environment variables
load_dotenv()

# Initialize the GPT-4 Vision model for image analysis
vision_model = ChatOpenAI(model="gpt-4o", max_tokens=1024)

# Initialize the latest GPT-4 model for text structuring
text_model = ChatOpenAI(model="gpt-4-1106-preview", max_tokens=1024)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def extract_text_from_image(image_path):
    base64_image = encode_image(image_path)
    
    messages = [
        SystemMessage(content="You are an expert in extracting text from images of ID cards. Your task is to accurately read and extract all text visible on the ID card."),
        HumanMessage(
            content=[
                {"type": "text", "text": "Please extract all text from this ID card image. Be as accurate and detailed as possible."},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        )
    ]
    
    response = vision_model.invoke(messages)
    return response.content

def structure_extracted_text(extracted_text):
    messages = [
        SystemMessage(content="You are an expert in structuring information from ID cards. Your task is to organize the extracted text into a structured format."),
        HumanMessage(content=f"Here's the extracted text from an ID card: \n\n{extracted_text}\n\nPlease structure this information into a JSON format. Include fields such as 'full_name', 'date_of_birth', 'id_number', 'gender', 'issue_date', 'expiry_date', 'card_type', and any other relevant fields you can identify. If a field is not present, use 'Not found' as the value. Ensure that your response is valid JSON."),
    ]
    
    response = text_model.invoke(messages)
    
    # Try to extract JSON from the response
    try:
        # First, attempt to parse the entire response as JSON
        return json.loads(response.content)
    except json.JSONDecodeError:
        # If that fails, try to find and extract a JSON object from the text
        content = response.content
        json_start = content.find('{')
        json_end = content.rfind('}') + 1
        if json_start != -1 and json_end != -1:
            try:
                return json.loads(content[json_start:json_end])
            except json.JSONDecodeError:
                pass
        
        # If JSON extraction fails, return a structured error message
        return {
            "error": "Failed to parse JSON from model response",
            "raw_response": content
        }


def process_id_card(image_path):
    extracted_text = extract_text_from_image(image_path)
    structured_info = structure_extracted_text(extracted_text)
    
    result = {
        "full_text": extracted_text,
        "structured_information": structured_info
    }
    
    return json.dumps(result, indent=2)

if __name__ == "__main__":
    image_path = "images/id.jpeg"  # Make sure this path is correct
    result = process_id_card(image_path)
    print(result)
    
    with open("id_extraction_result.json", "w") as f:
        f.write(result)