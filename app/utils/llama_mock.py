import random
import uuid
from typing import List, Dict, Any

def mock_parse_document(content: bytes, filename: str, file_extension: str) -> Dict[str, Any]:
    """
    Mock LlamaCloud document parsing response
    Simulates parsing a document and returning chunks with metadata
    """
    
    # Generate mock document ID
    document_id = f"doc_{uuid.uuid4().hex[:8]}"
    
    # Mock contract text chunks based on file type and content
    if file_extension == '.pdf':
        chunks = generate_pdf_mock_chunks(filename)
    elif file_extension == '.docx':
        chunks = generate_docx_mock_chunks(filename)
    else:  # .txt
        chunks = generate_txt_mock_chunks(filename, content)
    
    return {
        "document_id": document_id,
        "chunks": chunks,
        "processing_time": random.uniform(1.2, 3.5),
        "total_pages": random.randint(5, 25),
        "word_count": random.randint(1000, 5000)
    }

def generate_pdf_mock_chunks(filename: str) -> List[Dict[str, Any]]:
    """Generate mock chunks for PDF files"""
    
    # Contract-specific text templates
    contract_chunks = [
        {
            "text": "This Master Service Agreement ('Agreement') is entered into on [DATE] between [PARTY A], a [STATE] corporation ('Company'), and [PARTY B], a [STATE] corporation ('Service Provider').",
            "page": 1,
            "section": "Introduction"
        },
        {
            "text": "Termination clause: Either party may terminate this Agreement with ninety (90) days' written notice to the other party. Upon termination, all obligations shall cease except for those that by their nature should survive termination.",
            "page": 2,
            "section": "Termination"
        },
        {
            "text": "Liability limitation: In no event shall either party's liability exceed the total amount paid under this Agreement in the twelve (12) months preceding the claim. This limitation applies to all claims, whether in contract, tort, or otherwise.",
            "page": 5,
            "section": "Liability"
        },
        {
            "text": "Payment terms: Service Provider shall invoice Company monthly for services rendered. Payment is due within thirty (30) days of invoice date. Late payments shall incur a service charge of 1.5% per month.",
            "page": 3,
            "section": "Payment"
        },
        {
            "text": "Confidentiality: Both parties acknowledge that they may have access to confidential information. Each party agrees to maintain the confidentiality of such information and not disclose it to third parties without written consent.",
            "page": 4,
            "section": "Confidentiality"
        },
        {
            "text": "Intellectual Property: All work product created by Service Provider under this Agreement shall be deemed work made for hire and shall be owned by Company. Service Provider assigns all rights, title, and interest to Company.",
            "page": 6,
            "section": "IP Rights"
        },
        {
            "text": "Force Majeure: Neither party shall be liable for any delay or failure to perform due to causes beyond its reasonable control, including but not limited to acts of God, war, terrorism, or government regulations.",
            "page": 7,
            "section": "Force Majeure"
        },
        {
            "text": "Governing Law: This Agreement shall be governed by and construed in accordance with the laws of [STATE], without regard to its conflict of laws principles. Any disputes shall be resolved in the courts of [STATE].",
            "page": 8,
            "section": "Governing Law"
        },
        {
            "text": "Amendment: This Agreement may only be amended by written agreement signed by both parties. No oral modifications shall be binding or enforceable.",
            "page": 8,
            "section": "Amendment"
        },
        {
            "text": "Severability: If any provision of this Agreement is held to be invalid or unenforceable, the remaining provisions shall continue in full force and effect.",
            "page": 9,
            "section": "Severability"
        }
    ]
    
    # Customize based on filename
    filename_lower = filename.lower()
    if 'nda' in filename_lower:
        contract_chunks = generate_nda_chunks()
    elif 'employment' in filename_lower:
        contract_chunks = generate_employment_chunks()
    elif 'license' in filename_lower:
        contract_chunks = generate_license_chunks()
    
    # Convert to required format
    chunks = []
    for i, chunk_data in enumerate(contract_chunks):
        chunks.append({
            "chunk_id": f"c{i+1}",
            "text": chunk_data["text"],
            "metadata": {
                "page": chunk_data["page"],
                "contract_name": filename,
                "section": chunk_data.get("section", "General"),
                "chunk_type": "contract_clause"
            }
        })
    
    return chunks

def generate_nda_chunks() -> List[Dict[str, Any]]:
    """Generate NDA-specific chunks"""
    return [
        {
            "text": "Non-Disclosure Agreement: This Agreement is to protect confidential information that may be disclosed between the parties in connection with potential business relationships.",
            "page": 1,
            "section": "Purpose"
        },
        {
            "text": "Definition of Confidential Information: Confidential Information includes all non-public, proprietary information, technical data, trade secrets, know-how, research, product plans, products, services, customers, customer lists, markets, software, developments, inventions, processes, formulas, technology, designs, drawings, engineering, hardware configuration information, marketing, finances, or other business information.",
            "page": 1,
            "section": "Definitions"
        },
        {
            "text": "Obligations: The receiving party agrees to hold and maintain the Confidential Information in strict confidence and not to disclose such information to any third parties without prior written consent.",
            "page": 2,
            "section": "Obligations"
        },
        {
            "text": "Term: This Agreement shall remain in effect for a period of five (5) years from the date of execution, unless terminated earlier by mutual written consent.",
            "page": 2,
            "section": "Term"
        }
    ]

def generate_employment_chunks() -> List[Dict[str, Any]]:
    """Generate employment contract chunks"""
    return [
        {
            "text": "Employment Agreement: This Agreement sets forth the terms and conditions of employment between the Company and Employee for the position of [TITLE].",
            "page": 1,
            "section": "Employment"
        },
        {
            "text": "Compensation: Employee shall receive an annual salary of $[AMOUNT], payable in accordance with Company's standard payroll practices. Employee may also be eligible for performance bonuses at Company's discretion.",
            "page": 2,
            "section": "Compensation"
        },
        {
            "text": "Benefits: Employee shall be entitled to participate in Company's benefit plans, including health insurance, retirement plans, and paid time off, subject to the terms of such plans.",
            "page": 2,
            "section": "Benefits"
        },
        {
            "text": "Termination: Either party may terminate this employment relationship at any time, with or without cause, upon two (2) weeks' written notice.",
            "page": 3,
            "section": "Termination"
        }
    ]

def generate_license_chunks() -> List[Dict[str, Any]]:
    """Generate software license chunks"""
    return [
        {
            "text": "Software License Agreement: This Agreement grants Licensee a non-exclusive, non-transferable license to use the Software subject to the terms and conditions herein.",
            "page": 1,
            "section": "License Grant"
        },
        {
            "text": "Restrictions: Licensee may not copy, modify, distribute, sell, or lease any part of the Software. Reverse engineering is strictly prohibited.",
            "page": 1,
            "section": "Restrictions"
        },
        {
            "text": "Support and Maintenance: Licensor shall provide technical support and software updates for a period of one (1) year from the effective date.",
            "page": 2,
            "section": "Support"
        },
        {
            "text": "License Fee: Licensee agrees to pay the license fee of $[AMOUNT] annually. Failure to pay may result in license termination.",
            "page": 2,
            "section": "Fees"
        }
    ]

def generate_docx_mock_chunks(filename: str) -> List[Dict[str, Any]]:
    """Generate mock chunks for DOCX files"""
    # Similar to PDF but with different formatting
    return generate_pdf_mock_chunks(filename)

def generate_txt_mock_chunks(filename: str, content: bytes) -> List[Dict[str, Any]]:
    """Generate mock chunks for TXT files"""
    try:
        # Try to decode the content
        text_content = content.decode('utf-8')
        
        # Split into chunks (simple approach)
        words = text_content.split()
        chunk_size = 100  # words per chunk
        
        chunks = []
        for i in range(0, len(words), chunk_size):
            chunk_text = ' '.join(words[i:i+chunk_size])
            chunks.append({
                "chunk_id": f"c{i//chunk_size + 1}",
                "text": chunk_text,
                "metadata": {
                    "page": (i // chunk_size) + 1,
                    "contract_name": filename,
                    "section": "Content",
                    "chunk_type": "text_content"
                }
            })
        
        return chunks if chunks else generate_pdf_mock_chunks(filename)
        
    except UnicodeDecodeError:
        # Fallback to mock chunks if can't decode
        return generate_pdf_mock_chunks(filename)
