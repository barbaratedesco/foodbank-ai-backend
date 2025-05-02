from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uuid
import shutil
import os

app = FastAPI()

# Allow frontend (like Flutter) to access the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# This is where we store the detected food items
inventory = []

class Item(BaseModel):
    id: str
    name: str
    category: str
    confidence: float
    location: str

@app.post("/upload")
async def upload_photo(file: UploadFile = File(...)):
    image_id = str(uuid.uuid4())
    image_path = f"images/{image_id}.jpg"
    os.makedirs("images", exist_ok=True)

    # Save the uploaded image
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Simulate AI result (this would be replaced with real model output)
    simulated_items = [
        {"name": "Pasta", "category": "Dry Goods", "confidence": 0.94},
        {"name": "Canned Tomatoes", "category": "Canned Goods", "confidence": 0.91},
    ]

    # Add to inventory
    for item in simulated_items:
        inventory.append(Item(
            id=str(uuid.uuid4()),
            name=item["name"],
            category=item["category"],
            confidence=item["confidence"],
            location="Fort Worth Food Bank"
        ))

    return {"status": "success", "items_logged": simulated_items}

@app.get("/inventory", response_model=List[Item])
def get_inventory():
    return inventory
