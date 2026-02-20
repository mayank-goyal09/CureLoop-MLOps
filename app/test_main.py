from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_home():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "System Online", "message": "Ready for diagnosis!"}

def test_predict_valid_symptoms():
    """Test prediction with valid symptoms."""
    # Using common symptoms from the dataset
    payload = {
        "symptoms": ["itching", "skin_rash", "nodal_skin_eruptions"]
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    # Check if response structure is correct
    assert "predicted_disease" in data
    assert "description" in data
    assert "precautions" in data
    assert "medications" in data
    assert "diet" in data
    
    # Based on the notebook, these symptoms -> Fungal infection
    assert data["predicted_disease"] == "Fungal infection"

def test_predict_partial_invalid_symptoms():
    """Test prediction with mix of valid and invalid symptoms."""
    payload = {
        "symptoms": ["itching", "invalid_symptom_xyz"]
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert "itching" in data["recognized_symptoms"]
    assert "invalid_symptom_xyz" in data["ignored_symptoms"]

def test_predict_no_valid_symptoms():
    """Test error when no valid symptoms are provided."""
    payload = {
        "symptoms": ["invalid_one", "invalid_two"]
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "No valid symptoms provided."
