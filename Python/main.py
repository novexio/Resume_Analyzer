from fastapi import FastAPI
import pandas as pd 
from fastapi.middleware.cors import CORSMiddleware
import joblib 
from pydantic import BaseModel
from fastapi import UploadFile, File
from PyPDF2 import PdfReader 

app = FastAPI()

model = joblib.load("resume_model.pkl")     
vectorizer = joblib.load("vectorizer.pkl")

app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173",
                        "http://127.0.0.1:5173"],
        allow_credentials= True,
        allow_methods=["*"],
        allow_headers=["*"],
)

class ResumeData(BaseModel):
    text: str


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    # File Type check
    if file.content_type != "application/pdf":
        return {"error" : "Invalid file type. Please upload a PDF file."}
    
    reader = PdfReader(file.file)
    text = ""


    for page in reader.pages:
        text += page.extract_text() or ""
    
    text_lower = text.lower()

    vec = vectorizer.transform([text])
    prediction = model.predict(vec)[0]

    # Confidence score
    probability = model.predict_proba(vec)[0]
    confidence = max(probability)

    # Detected skills

    skills_list = [
    "python", "sql", "excel", "powerbi",
    "machine learning", "deep learning",
    "react", "javascript", "html", "css",
    "django", "fastapi", "nodejs"
    ]

    detected_skills = []

    for skill in skills_list:
        if skill in text_lower:
            detected_skills.append(" " + skill)

    # Suggested roles based on detected skills
    suggestions = []

    if "github" not in text_lower:
        suggestions.append("Add GitHub profile to showcase your projects. ")
    
    if "project" not in text_lower:
        suggestions.append("Include a project section")
    
    if len(detected_skills) < 3:
        suggestions.append("Consider adding more skills to your resume. ")
    
    if "sql" not in text_lower and "excel" not in text_lower:
        suggestions.append("Mention tools like SQL or Excel. ")

    return {
        "prediction_Role": prediction,
        "Confidence": f"{round(confidence * 100)}%",
        "Detected_Skills": detected_skills if detected_skills else "No specific skills detected",
        "Suggestions": suggestions if suggestions else "Your resume looks good!"
    }