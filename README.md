# Document Liability Analysis Streamlit App

This Streamlit app allows users to upload various document types (PDF, DOC, DOCX, images, PPTX, XLSX) for liability analysis. The app uses OCR to extract text from the documents, summarizes the content using LLaMA 3.1 70B, and performs a liability analysis using OpenAI's model.

## Features

- File upload support for multiple document types
- OCR text extraction using Upstage API
- Text summarization using LLaMA 3.1 70B
- Liability analysis using OpenAI's model
- PDF report generation

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in `.env` file
4. Run the Streamlit app: `streamlit run app/main.py`

## Usage

1. Upload a supported document file
2. Wait for the analysis to complete
3. View the generated report
4. Optionally save the report as a PDF

## Contributing

Feel free to submit issues or pull requests to improve the app.