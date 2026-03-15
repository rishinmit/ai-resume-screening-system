# LIVE DEMO:- 
# AI Resume Screening System

An AI-powered Resume Screening System that automatically ranks candidate resumes based on their similarity with a Job Description (JD). The system uses semantic embeddings and skill matching to help recruiters quickly identify the most suitable candidates.

## 🚀 Features

* Upload **Job Description (JD)** and multiple **candidate resumes**
* Automatic **resume ranking using AI**
* **Semantic similarity matching** using Sentence-BERT
* **Skill extraction and matching**
* Visual display of:

  * Top candidate
  * Resume ranking
  * Matched and missing skills
  * Score bars and statistics
* Download/view uploaded resumes directly from the interface

---

## 🧠 Machine Learning Model

The system uses **Sentence-BERT (all-MiniLM-L6-v2)** to convert text into semantic embeddings.

Ranking is calculated using:

```
Final Score = (0.7 × Semantic Similarity) + (0.3 × Skill Match)
```

### Technologies Used

* **Sentence Transformers**
* **Cosine Similarity**
* **Skill Matching Algorithm**

---

## 🏗️ Project Architecture

```
Frontend (Vercel)
        │
        ▼
Backend API (FastAPI on Render)
        │
        ▼
Sentence-BERT Embedding Model
        │
        ▼
Resume Ranking Results
```

---

## 📂 Project Structure

```
ai-resume-screening-system
│
├── backend
│   ├── main.py
│   ├── ats_model.py
│   ├── utils.py
│   ├── requirements.txt
│
├── frontend
│   ├── index.html
│   ├── script.js
│   ├── style.css
│
└── README.md
```

---

## ⚙️ How It Works

1. User uploads a **Job Description**
2. User uploads multiple **candidate resumes**
3. Text is extracted from resumes (PDF/DOCX)
4. Sentence-BERT converts text into embeddings
5. Cosine similarity is calculated between JD and resumes
6. Skill matching score is calculated
7. Final ranking is generated and displayed

---

## 🖥️ Live Demo

Frontend:

```
https://ai-resume-screening-system-1lb2vx2mu.vercel.app
```

Backend API:

```
https://ai-resume-screening-system.onrender.com
```

---

## 🛠️ Installation (Local Setup)

Clone the repository:

```
git clone https://github.com/rishinmit/ai-resume-screening-system.git
cd ai-resume-screening-system
```

### Backend Setup

```
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend will run at:

```
http://localhost:8000
```

### Frontend

Simply open:

```
frontend/index.html
```

in your browser.

---

## 📊 Example Workflow

1. Upload a **Software Engineer Job Description**
2. Upload multiple candidate resumes
3. Click **Analyze Resumes**
4. System automatically ranks candidates and highlights:

   * Best candidate
   * Skill gaps
   * Matching skills

---

## 👨‍💻 Authors

**Rishi Raj**
USN: 1NT22IS137

**Sajid Raza**
USN: 1NT22IS144

Department of Information Science and Engineering
NMIT, Yelahanka

Project completed as part of the **In-house Internship Program** under the guidance of:

**Dr. Deepak Raj**
Associate Professor
Department of Information Science and Engineering

---

## 📜 License

This project is developed for academic and educational purposes.
