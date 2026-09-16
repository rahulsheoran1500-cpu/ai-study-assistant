"""PDF SERVICE - PDF processing and text extraction"""

import PyPDF2
import logging

logger = logging.getLogger(__name__)

class PDFService:
    """Service for PDF processing"""
    
    @staticmethod
    def extract_text_from_pdf(file_path, max_pages=None):
        """Extract text from PDF file
        
        Args:
            file_path: Path to PDF file
            max_pages: Maximum pages to extract (None = all)
        
        Returns:
            str: Extracted text
        """
        try:
            text = ""
            with open(file_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                total_pages = len(reader.pages)
                
                # Limit pages if specified
                pages_to_read = min(total_pages, max_pages) if max_pages else total_pages
                
                for page_num in range(pages_to_read):
                    page = reader.pages[page_num]
                    text += page.extract_text() + "\n"
            
            if not text.strip():
                return None
            
            return text.strip()
        
        except Exception as e:
            logger.error(f"PDF extraction error: {str(e)}")
            return None
    
    @staticmethod
    def get_pdf_info(file_path):
        """Get PDF file information
        
        Returns:
            dict: PDF metadata
        """
        try:
            with open(file_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                return {
                    'pages': len(reader.pages),
                    'title': reader.metadata.title if reader.metadata else 'Unknown'
                }
        except Exception as e:
            logger.error(f"Error getting PDF info: {str(e)}")
            return {'pages': 0, 'title': 'Unknown'}
