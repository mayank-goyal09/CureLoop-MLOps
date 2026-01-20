from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import logging

app = FastAPI(title="Medicine Recommendation System 🩺")

logging.basicConfig(level=logging.INFO)

# --- 1. Load Everything ---

# Load model
model = joblib.load("models/doctor_model.joblib")

# Load symptom list (usually stored as a list)
loaded_symptoms = joblib.load("models/symptom_list.joblib")

# Ensure it's a dictionary: symptom -> index
if isinstance(loaded_symptoms, list):
    symptoms_dict = {symptom: idx for idx, symptom in enumerate(loaded_symptoms)}
elif isinstance(loaded_symptoms, dict):
    symptoms_dict = loaded_symptoms
else:
    raise RuntimeError("symptom_list.joblib must be a list or a dict")

# Load datasets
description = pd.read_csv("data/description.csv")
precautions = pd.read_csv("data/precautions_df.csv")
medications = pd.read_csv("data/medications.csv")
diets = pd.read_csv("data/diets.csv")

# --- 2. Input Schema ---

class SymptomInput(BaseModel):
    symptoms: list[str]

# --- 3. Helper Function ---

def get_recommendations(predicted_disease):

    desc_row = description[description['Disease'] == predicted_disease]
    desc = desc_row['Description'].values[0] if not desc_row.empty else "No description available."

    pre_row = precautions[precautions['Disease'] == predicted_disease]
    if not pre_row.empty:
        pre = pre_row.iloc[:, 1:].values.flatten().tolist()
        pre = [p for p in pre if str(p).lower() != 'nan']
    else:
        pre = []

    med_row = medications[medications['Disease'] == predicted_disease]
    med = med_row['Medication'].values.tolist() if not med_row.empty else []

    die_row = diets[diets['Disease'] == predicted_disease]
    die = die_row['Diet'].values.tolist() if not die_row.empty else []

    return {
        "description": desc,
        "precautions": pre,
        "medications": med,
        "diet": die
    }

# --- 4. Predict Endpoint ---

@app.post("/predict")
def predict(input_data: SymptomInput):
    try:
        input_vector = np.zeros(len(symptoms_dict))

        found = []
        ignored = []

        for s in input_data.symptoms:
            cleaned_symptom = s.strip().lower().replace(" ", "_")

            if cleaned_symptom in symptoms_dict:
                idx = symptoms_dict[cleaned_symptom]
                input_vector[idx] = 1
                found.append(cleaned_symptom)
            else:
                ignored.append(cleaned_symptom)
                logging.warning(f"Symptom not found: {cleaned_symptom}")

        if input_vector.sum() == 0:
            raise HTTPException(
                status_code=400,
                detail="No valid symptoms provided."
            )

        prediction = model.predict(input_vector.reshape(1, -1))[0]
        details = get_recommendations(prediction)

        return {
            "predicted_disease": prediction,
            "recognized_symptoms": found,
            "ignored_symptoms": ignored,
            **details
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- 5. Health Check ---

@app.get("/")
def home():
    return {"status": "System Online", "message": "Ready for diagnosis!"}
