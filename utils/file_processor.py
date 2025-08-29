"""
File processing utilities for handling resume uploads
"""
from typing import Tuple, Optional
import docx2txt
# Note: google-genai is imported lazily inside the PDF branch to avoid import errors at module load time

def process_uploaded_file(uploaded_file, api_key: Optional[str] = None) -> Tuple[Optional[str], str]:
    """
    Process an uploaded file and extract text content
    
    Args:
        uploaded_file: Streamlit file uploader object
        api_key: Optional Gemini API key (used for PDF extraction via google-genai)
        
    Returns:
        Tuple of (processed_text, status_message)
    """
    if uploaded_file is None:
        return None, "No file uploaded"
    
    try:
        if uploaded_file.type == "application/pdf":
            # Use Gemini (google-genai) to extract plain text from the uploaded PDF
            try:
                from google import genai  # type: ignore
                from google.genai import types  # type: ignore
            except ImportError:
                return None, (
                    "Error processing file: google-genai is not installed or conflicts with a 'google' package. "
                    "Please uninstall the legacy 'google' package and install requirements."
                )

            if not api_key:
                return None, "Error processing file: API key is required to process PDF files"

            client = genai.Client(api_key=api_key)
            pdf_bytes = uploaded_file.getvalue()

            prompt = (
                "Extract the plain text content from this resume PDF. "
                "Return only the extracted text without any additional commentary."
            )

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Part.from_bytes(
                        data=pdf_bytes,
                        mime_type="application/pdf",
                    ),
                    prompt,
                ],
            )

            extracted_text = getattr(response, "text", "") or ""
            if not extracted_text.strip():
                return None, "Error processing file: Could not extract text from PDF"
            return extracted_text, "Successfully extracted text from your resume!"
            
        elif uploaded_file.type == "text/plain":
            # For text files
            return uploaded_file.getvalue().decode("utf-8"), "Successfully extracted text from your resume!"
            
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            # For DOCX files
            return docx2txt.process(uploaded_file), "Successfully extracted text from your DOCX file!"
            
        else:
            return None, f"Unsupported file type: {uploaded_file.type}"
            
    except Exception as e:
        return None, f"Error processing file: {str(e)}"
