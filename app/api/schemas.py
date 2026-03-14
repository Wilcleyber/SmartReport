from pydantic import BaseModel
from typing import Dict, Any, Optional

class AnalysisResponse(BaseModel):
    status: str
    fileId: str
    fileName: str
    analysisSummary: str
    dataMetrics: Dict[str, Any]  # Ex: {"media_producao": 1500.5, "total": 5000}
    chartBase64: str
    pdfUrl: Optional[str] = None

class ErrorResponse(BaseModel):
    status: str
    detail: str