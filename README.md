# ID Extractor

This project uses advanced machine learning techniques, specifically GPT-4 with vision capabilities, to extract and structure information from various types of ID cards.

## Features

- Extracts text from ID card images using GPT-4 vision model
- Structures the extracted information into a JSON format
- Supports various types of ID cards (currently optimized for Ghanaian IDs, but extensible to others)
- Provides both raw extracted text and structured information

## Installation

1. Clone this repository: 
   git clone https://github.com/patrickattankurugu/id-extractor.git
2. Navigate to the project directory:
    cd id-extractor
3. Install the required packages:
   pip install -r requirements.txt
4. Set up your OpenAI API key in a `.env` file:
   OPENAI_API_KEY=your_api_key_here

## Usage

1. Place your ID card image in the `images` folder.

2. Run the script:
   python task1_advanced_extraction.py

3. The extracted information will be printed to the console and saved in `id_extraction_result.json`.

## Customization

While the current implementation is optimized for Ghanaian ID cards, the system is designed to be flexible. To adapt it for other types of ID cards:

1. Modify the `structure_extracted_text` function in `task1_advanced_extraction.py` to include fields relevant to the new ID card type.
2. Update the system message in the `extract_text_from_image` function if specific instructions are needed for the new card type.



