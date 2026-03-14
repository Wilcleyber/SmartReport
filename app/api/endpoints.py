import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

# Importações dos serviços
from app.api.schemas import AnalysisResponse
from app.services.data_engine import DataEngine
from app.utils.sanitizer import Sanitizer
from app.services.ai_analyst import AIAnalyst
from app.services.visualizer import Visualizer

router = APIRouter()
ai_analyst = AIAnalyst()
UPLOAD_DIR = "uploads"

@router.post("/upload", response_model=AnalysisResponse)
async def upload_and_process(file: UploadFile = File(...)):
    extension = os.path.splitext(file.filename)[1].lower()
    if extension not in ['.csv', '.xlsx']:
        raise HTTPException(status_code=400, detail="Formato inválido.")

    try:
        content = await file.read()
        
        # Orquestração do processamento
        df_original, metrics, tech_summary = await DataEngine.process_file(content, extension)
        df_sanitized = Sanitizer.mask_data(df_original)
        analysis_summary = await ai_analyst.generate_analysis(tech_summary)
        chart_b64 = Visualizer.generate_chart_base64(metrics)
        
        operation_id = str(uuid.uuid4())
        pdf_filename = f"report_{operation_id}.pdf"
        pdf_path = os.path.join(UPLOAD_DIR, pdf_filename)
        
        Visualizer.generate_pdf(analysis_summary, chart_b64, file.filename, pdf_path)

        return {
            "status": "success",
            "fileId": operation_id,
            "fileName": file.filename,
            "analysisSummary": analysis_summary,
            "dataMetrics": metrics,
            "chartBase64": f"data:image/png;base64,{chart_b64}",
            "pdfUrl": pdf_filename
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")
    finally:
        await file.close()

@router.get("/download/{file_name}")
async def download_pdf(file_name: str):
    file_path = os.path.join(UPLOAD_DIR, file_name)
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=file_name, media_type='application/pdf')
    raise HTTPException(status_code=404, detail="Arquivo não encontrado.")