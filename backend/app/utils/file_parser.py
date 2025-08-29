import base64
import io
import logging
from typing import Optional
import pandas as pd
from PyPDF2 import PdfReader

logger = logging.getLogger(__name__)

def parse_csv_from_base64(base64_content: str) -> Optional[str]:
    """
    Parse base64-encoded CSV content and extract text.
    
    Args:
        base64_content: Base64-encoded CSV string
        
    Returns:
        Extracted text as string or None if parsing fails
    """
    try:
        # Decode base64 content
        csv_bytes = base64.b64decode(base64_content)
        csv_string = csv_bytes.decode('utf-8')
        
        # Read CSV using pandas
        df = pd.read_csv(io.StringIO(csv_string))
        
        # Convert DataFrame to text representation
        text_content = df.to_string(index=False)
        
        logger.info(f"Successfully parsed CSV with {len(df)} rows and {len(df.columns)} columns")
        return text_content
        
    except Exception as e:
        logger.error(f"Error parsing CSV: {str(e)}")
        return None

def parse_pdf_from_base64(base64_content: str) -> Optional[str]:
    """
    Parse base64-encoded PDF content and extract text.
    
    Args:
        base64_content: Base64-encoded PDF string
        
    Returns:
        Extracted text as string or None if parsing fails
    """
    try:
        # Decode base64 content
        pdf_bytes = base64.b64decode(base64_content)
        
        # Create PDF reader
        pdf_reader = PdfReader(io.BytesIO(pdf_bytes))
        
        # Extract text from all pages
        text_content = ""
        for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            if page_text:
                text_content += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
        
        logger.info(f"Successfully parsed PDF with {len(pdf_reader.pages)} pages")
        return text_content.strip()
        
    except Exception as e:
        logger.error(f"Error parsing PDF: {str(e)}")
        return None

def parse_file_content(file_content: str, file_type: str = None) -> Optional[str]:
    """
    Parse file content based on type or auto-detect.
    
    Args:
        file_content: Base64-encoded file content
        file_type: Optional file type hint ('csv' or 'pdf')
        
    Returns:
        Extracted text as string or None if parsing fails
    """
    if not file_content:
        return None
    
    # Try to auto-detect file type if not specified
    if not file_type:
        # Simple heuristic: check if content looks like CSV (contains commas and newlines)
        try:
            decoded = base64.b64decode(file_content).decode('utf-8')
            if ',' in decoded and '\n' in decoded:
                file_type = 'csv'
            else:
                file_type = 'pdf'
        except:
            file_type = 'pdf'  # Default to PDF if detection fails
    
    # Parse based on file type
    if file_type.lower() == 'csv':
        return parse_csv_from_base64(file_content)
    elif file_type.lower() == 'pdf':
        return parse_pdf_from_base64(file_content)
    else:
        logger.warning(f"Unsupported file type: {file_type}")
        return None
