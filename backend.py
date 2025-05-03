# backend.py

from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from pymongo import MongoClient
from datetime import datetime

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from typing import Optional

# Initialize FastAPI app
app = FastAPI()


# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Can restrict by frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




class User(BaseModel):
    student_id: str
    password: str

# Helper: hash and verify
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@app.post("/signup/")
async def signup(user: User):
    if user_collection.find_one({"student_id": user.student_id}):
        return JSONResponse(status_code=400, content={"message": "Student ID already exists"})

    hashed = hash_password(user.password)
    user_collection.insert_one({"student_id": user.student_id, "password": hashed})
    return {"message": "Account created successfully"}

@app.post("/login/")
async def login(user: User):
    db_user = user_collection.find_one({"student_id": user.student_id})
    if not db_user or not verify_password(user.password, db_user["password"]):
        return JSONResponse(status_code=401, content={"message": "Invalid credentials"})
    return {"message": "Login successful"}


# Load the fine-tuned LLaMA model and tokenizer
model_name = "./lora_mentor_model"  
tokenizer_name="./lora_mentor_model_tokenizer"

tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# MongoDB client and database setup
client = MongoClient("mongodb://localhost:27017/")
db = client["qa_database"]
collection = db["qa_sessions"]
user_collection = db["users"]

# Pydantic model for question input
class QuestionRequest(BaseModel):
    question: str
    student_id: str = None

# Function to generate an answer from the LLaMA model
def get_answer_llama(question: str) -> str:
    input_ids = tokenizer.encode(question, return_tensors='pt')
    output = model.generate(input_ids, max_new_tokens=100)  # You can adjust max_new_tokens
    return tokenizer.decode(output[0], skip_special_tokens=True)

# FastAPI route to handle question requests
@app.post("/ask_question/")
async def ask_question(request: QuestionRequest):
    question = request.question
    student_id = request.student_id

    if not student_id:
        return JSONResponse(status_code=400, content={"message": "Student ID is required."})

    # Check if student exists
    if not user_collection.find_one({"student_id": student_id}):
        return JSONResponse(status_code=404, content={"message": "Student ID not found."})

    # Get the answer from the model
    answer = get_answer_llama(question)

    # Log the interaction
    collection.insert_one({
        "student_id": student_id,  # correctly assigned
        "question": question,
        "answer": answer,
        "timestamp": datetime.now()
    })

    return {"answer": answer}
