"""
InsightPulse AI - Neural Document Engine v1.0
=====================================================================
Forensic extraction of PDF, DOCX, and CSV files into structured, 
LLM-ready text with spatial and temporal alignment.
"""
import io
import pandas as pd
from typing import Dict, Any, List
try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

def extract_text_from_pdf(byte_content: bytes) -> str:
    """Extract and align text from PDF for forensic analysis."""
    if not PdfReader:
        return "Error: pypdf library not installed."
    
    reader = PdfReader(io.BytesIO(byte_content))
    full_text = []
    for i, page in enumerate(reader.pages):
        full_text.append(f"--- PAGE {i+1} ---\n{page.extract_text()}")
    
    return "\n".join(full_text)

def tabular_to_structured_text(df: pd.DataFrame) -> str:
    """Convert CSV/DataFrame to a highly aligned text format for LLMs."""
    # We create a specific 'Forensic Text' representation
    lines = []
    lines.append(f"DATASET STRUCTURE: {df.shape[0]} rows x {df.shape[1]} columns")
    lines.append("-" * 40)
    
    # Header alignment
    headers = " | ".join(df.columns)
    lines.append(headers)
    lines.append("-" * len(headers))
    
    # Sample rows with alignment
    for idx, row in df.head(50).iterrows():
        row_str = " | ".join([str(val) for val in row.values])
        lines.append(f"ROW {idx}: {row_str}")
        
    return "\n".join(lines)

def chunk_text(text: str, chunk_size: int = 4000, overlap: int = 500) -> List[str]:
    """Smart chunking for long documents to fit LLM context windows."""
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i : i + chunk_size])
    return chunks

def process_business_file(byte_content: bytes, filename: str) -> Dict[str, Any]:
    """Universal entry point for forensic document ingestion."""
    ext = filename.split(".")[-1].lower()
    
    result = {
        "filename": filename,
        "content_type": ext,
        "structured_text": "",
        "metadata": {}
    }
    
    if ext == "pdf":
        result["structured_text"] = extract_text_from_pdf(byte_content)
    elif ext in ["csv", "xlsx", "xls"]:
        try:
            if ext == "csv":
                df = pd.read_csv(io.BytesIO(byte_content))
            else:
                df = pd.read_excel(io.BytesIO(byte_content))
            result["structured_text"] = tabular_to_structured_text(df)
            result["metadata"]["rows"] = len(df)
            result["metadata"]["columns"] = list(df.columns)
        except Exception as e:
            result["structured_text"] = f"Extraction failed: {str(e)}"
    
    return result
