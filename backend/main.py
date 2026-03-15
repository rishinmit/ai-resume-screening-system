from fastapi import FastAPI, UploadFile, Form
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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