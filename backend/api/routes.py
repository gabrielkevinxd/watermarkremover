import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from services.pdf_service import remove_watermark, cleanup_file
from core.config import settings

router = APIRouter()

@router.post("/remove-watermark")
async def api_remove_watermark(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="PDF file to process")
):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    content = await file.read()
    if len(content) > 50 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size limit is 50MB.")

    task_id = str(uuid.uuid4())[:8]
    input_path = settings.UPLOAD_DIR / f"{task_id}_input.pdf"
    output_path = settings.OUTPUT_DIR / f"{task_id}_cleaned.pdf"

    with open(input_path, "wb") as f:
        f.write(content)

    try:
        result = remove_watermark(str(input_path), str(output_path))
        background_tasks.add_task(cleanup_file, str(input_path))
        
        return {
            "success": True,
            "task_id": task_id,
            "filename": f"cleaned_{file.filename}",
            "pages_processed": result["pages_processed"],
            "download_url": f"/api/download/{task_id}"
        }
    except Exception as e:
        cleanup_file(str(input_path))
        cleanup_file(str(output_path))
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@router.get("/download/{task_id}")
async def download_file(task_id: str, background_tasks: BackgroundTasks):
    output_path = settings.OUTPUT_DIR / f"{task_id}_cleaned.pdf"
    
    if not output_path.exists():
        raise HTTPException(status_code=404, detail="File not found or has expired.")
    
    # Delay cleanup for a subsequent job or another task normally, but here let's just use background task
    background_tasks.add_task(cleanup_file, str(output_path))
    
    return FileResponse(
        path=str(output_path),
        filename=f"cleaned_{task_id}.pdf",
        media_type="application/pdf"
    )
