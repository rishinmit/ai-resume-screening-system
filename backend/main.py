from fastapi import FastAPI, UploadFile, Form
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil
import os

from ats_model import ResumeATS
from utils import extract_text

app = FastAPI()

# ats = None

# @app.on_event("startup")
# def load_model():
#     global ats
#     ats = ResumeATS()
ats = None

def get_model():
    global ats
    if ats is None:
        ats = ResumeATS()
    return ats
# app.mount("/files", StaticFiles(directory="temp"), name="files")
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-resume-screening-system-mzw913dsb.vercel.app",
        "http://localhost:5501",
        "http://127.0.0.1:5501",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
ats = None


@app.post("/rank-resumes")
async def rank_resumes(jd: UploadFile, resumes: list[UploadFile], top_n: int = Form(0)):

    os.makedirs("temp", exist_ok=True)

    jd_path = f"temp/{jd.filename}"

    with open(jd_path, "wb") as buffer:
        shutil.copyfileobj(jd.file, buffer)

    jd_text = extract_text(jd_path)

    resume_texts = []
    resume_names = []

    for resume in resumes:

        path = f"temp/{resume.filename}"

        with open(path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)

        text = extract_text(path)

        resume_texts.append(text)
        resume_names.append(resume.filename)

    # ranking = ats.rank_resumes(jd_text, resume_texts)
    model = get_model()
    ranking = model.rank_resumes(jd_text, resume_texts)

    # FLATTEN RESULTS

    flat = []

    for group in ranking:
        for c in group["candidates"]:
            flat.append(c)

    flat = sorted(flat, key=lambda x: x["score"], reverse=True)

    if top_n > 0:
        flat = flat[:top_n]

    return {
        "ranking": flat,
        "resumes": resume_names
    }

from fastapi.responses import FileResponse

@app.get("/")
def home():
    return FileResponse("../frontend/index.html")


@app.get("/files/{filename}")
def get_uploaded_file(filename: str):
    safe_name = os.path.basename(filename)
    file_path = os.path.join("temp", safe_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path, media_type="application/pdf")


@app.get("/download/{filename}")
def download_uploaded_file(filename: str):
    safe_name = os.path.basename(filename)
    file_path = os.path.join("temp", safe_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename=safe_name,
        headers={"Content-Disposition": f'attachment; filename="{safe_name}"'},
    )
