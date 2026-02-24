---
title: CureLoop MLOps
emoji: 💊
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

<div align="center">

# � CureLoop-MLOps

### *Automated Disease Prediction Pipeline*

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&duration=3000&pause=1000&color=36BCF7&center=true&vCenter=true&multiline=true&repeat=true&width=600&height=80&lines=Push+Code+%E2%86%92+Auto+Train+%E2%86%92+Test+%E2%86%92+Deploy;End-to-End+MLOps+in+Action+%F0%9F%9A%80" alt="Typing SVG" />

<br/>

![MLOps Pipeline](https://github.com/mayank-goyal09/CureLoop-MLOps/actions/workflows/main.yml/badge.svg)
[![Streamlit App](https://img.shields.io/badge/Streamlit-Try_App_Here-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://cureloop-mlops-projects.streamlit.app/)
[![API Status](https://img.shields.io/badge/🔴_Live_API-Online-brightgreen?style=for-the-badge&logo=fastapi&logoColor=white)](https://mayankg09-cureloop-mlops.hf.space/docs)
[![Hugging Face](https://img.shields.io/badge/🤗_Hugging_Face-Deployed-yellow?style=for-the-badge)](https://huggingface.co/spaces/mayankg09/cureLoop-mLOps)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://mayankg09-cureloop-mlops.hf.space/)
[![Python](https://img.shields.io/badge/Python-3.9-3776AB?style=for-the-badge&logo=python&logoColor=white)]()
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)]()

<br/>

> *"Transforming static notebooks into a living, breathing AI system."*

<br/>

### 🌐 [**👉 Try the AI App (Streamlit) →**](https://cureloop-mlops-projects.streamlit.app/)
### 🧑‍💻 [**👉 Explore the API (FastAPI) →**](https://mayankg09-cureloop-mlops.hf.space/docs)

</div>

---

## 🚀 Project Evolution

<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=16&duration=2000&pause=500&color=FF6B6B&center=true&vCenter=true&repeat=true&width=500&lines=From+Jupyter+Notebook...;...to+Production+ML+System+%F0%9F%8E%AF" alt="Evolution" />

</div>

This repository represents the **production-grade evolution** of my original [Medicine Recommendation System](https://github.com/mayank-goyal09/medicine-recommendation-system). 

| Feature | 🏛️ Original (Legacy) | ⚡ **CureLoop (This Repo)** |
| :--- | :---: | :---: |
| **Model Training** | 📓 Manual in Notebooks | 🤖 **Automated** on every push |
| **Deployment** | 💻 Local Only | ☁️ **[Live on HF Spaces](https://mayankg09-cureloop-mlops.hf.space/docs)** |
| **Interface** | 📝 CLI / Notebook | 🌐 **FastAPI REST API** |
| **Reliability** | ❌ No Tests | ✅ **Pytest Automated** |
| **Scalability** | 1️⃣ Single Machine | 🐳 **Docker (Runs Anywhere)** |
| **CI/CD** | ❌ None | ✅ **GitHub Actions** |

---

## 🛠️ The MLOps Pipeline

<div align="center">

```
╔══════════╗    ╔══════════╗    ╔══════════╗    ╔══════════╗    ╔══════════╗
║  📝 PUSH ║───▶║ 🧠 TRAIN ║───▶║ 🧪 TEST  ║───▶║ 🐳 BUILD ║───▶║ ☁️ DEPLOY ║
╚══════════╝    ╚══════════╝    ╚══════════╝    ╚══════════╝    ╚══════════╝
   GitHub          Model           Pytest          Docker         HF Spaces
   Actions        Retrain        Validation        Image          Auto-Sync
```

</div>

<details>
<summary>🔍 <b>Click to see detailed pipeline steps</b></summary>

<br/>

| Step | Action | Tool |
| :---: | :--- | :--- |
| 1️⃣ | Developer pushes code/data to GitHub | `git push` |
| 2️⃣ | GitHub Actions triggers the pipeline | `.github/workflows/main.yml` |
| 3️⃣ | Model is retrained on latest data | `python train.py` |
| 4️⃣ | Unit tests validate API & predictions | `pytest app/test_main.py` |
| 5️⃣ | Docker image is built for verification | `docker build` |
| 6️⃣ | Code synced to Hugging Face Spaces | `git push space main` |
| 7️⃣ | HF Spaces builds Docker & serves API | Automatic 🚀 |

</details>

---

## 🧪 Try It Now!

<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=18&duration=2500&pause=800&color=00D26A&center=true&vCenter=true&repeat=true&width=450&lines=The+API+is+LIVE!+Test+it+below+%F0%9F%91%87" alt="Live" />

</div>

### 🖥️ Interactive Docs (Recommended)
> Visit the **[Swagger UI](https://mayankg09-cureloop-mlops.hf.space/docs)** and click "Try it out" on the `/predict` endpoint!

### 💻 cURL Command
```bash
curl -X POST "https://mayankg09-cureloop-mlops.hf.space/predict" \
  -H "Content-Type: application/json" \
  -d '{"symptoms": ["itching", "skin_rash", "nodal_skin_eruptions"]}'
```

### 🐍 Python Example
```python
import requests

response = requests.post(
    "https://mayankg09-cureloop-mlops.hf.space/predict",
    json={"symptoms": ["itching", "skin_rash", "nodal_skin_eruptions"]}
)
print(response.json())
```

<details>
<summary>📋 <b>Click to see sample response</b></summary>

```json
{
  "predicted_disease": "Fungal infection",
  "recognized_symptoms": ["itching", "skin_rash", "nodal_skin_eruptions"],
  "ignored_symptoms": [],
  "description": "Fungal infection is a common skin condition caused by fungi.",
  "precautions": ["bath twice", "use detol or neem in bathing water", "keep infected area dry", "use clean cloths"],
  "medications": ["Antifungal Cream", "Fluconazole", "Terbinafine", "Clotrimazole", "Ketoconazole"],
  "diet": ["Antifungal Diet", "Probiotics", "Garlic", "Coconut oil", "Turmeric"]
}
```

</details>

---

## 📂 Project Structure

```
CureLoop-MLOps/
│
├── 🔄 .github/workflows/
│   └── main.yml            # CI/CD Pipeline (Train → Test → Deploy)
│
├── 🌐 app/
│   ├── main.py             # FastAPI Application & Endpoints  
│   └── test_main.py        # Automated API Tests
│
├── 📊 data/
│   ├── Training.csv        # Symptom-Disease Training Data (4920 rows)
│   ├── description.csv     # Disease Descriptions
│   ├── medications.csv     # Medication Recommendations
│   ├── precautions_df.csv  # Precautionary Measures
│   └── diets.csv           # Dietary Recommendations
│
├── 🧠 models/
│   ├── doctor_model.joblib # Trained Decision Tree Model
│   └── symptom_list.joblib # Feature Column Names
│
├── 🐳 Dockerfile           # Container Build Instructions
├── 🏋️ train.py              # Automated Training Script
├── 📦 requirements.txt     # Python Dependencies
└── 📖 README.md            # You are here!
```

---

## 💻 Tech Stack

<div align="center">

| Category | Technologies |
| :---: | :---: |
| **Machine Learning** | ![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white) ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white) ![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white) |
| **API Framework** | ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white) ![Uvicorn](https://img.shields.io/badge/Uvicorn-2F4F4F?style=flat-square&logoColor=white) |
| **DevOps** | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white) |
| **Cloud** | ![Hugging Face](https://img.shields.io/badge/🤗_Hugging_Face-FFD21E?style=flat-square) |

</div>

---

## 🔧 Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/mayank-goyal09/CureLoop-MLOps.git
cd CureLoop-MLOps

# 2. Install dependencies
pip install -r requirements.txt

# 3. Train the model
python train.py

# 4. Start the server
uvicorn app.main:app --reload

# 5. Open docs at http://localhost:8000/docs 🎉
```

---

## 🗺️ The Journey

```
📓 Jupyter Notebook          🔄 CureLoop-MLOps              🌐 Live API
   (Research Phase)     →       (Production Phase)      →     (Deployed!)
                                                        
   Manual training             Automated CI/CD              Anyone can use
   Local execution             Docker containers            REST API access
   No tests                    Full test suite              Cloud hosted
```

<div align="center">

[📓 Original Project](https://github.com/mayank-goyal09/medicine-recommendation-system) **→** [� This MLOps Repo](https://github.com/mayank-goyal09/CureLoop-MLOps) **→** [🌐 Live API](https://mayankg09-cureloop-mlops.hf.space/docs)

</div>

---

<div align="center">

### 📬 Connect with Me

[![Email](https://img.shields.io/badge/Email-itsmaygal09@gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:itsmaygal09@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Mayank_Goyal-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mayank-goyal-4b8756363/)
[![Portfolio](https://img.shields.io/badge/Portfolio-mayank--goyal09.github.io-000000?style=for-the-badge&logo=github&logoColor=white)](https://mayank-goyal09.github.io/)

<br/>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=14&duration=3000&pause=1000&color=888888&center=true&vCenter=true&repeat=true&width=400&lines=Made+with+%E2%9D%A4%EF%B8%8F+by+Mayank+Goyal;MLOps+Learning+Journey+%F0%9F%9A%80;Star+%E2%AD%90+if+you+found+this+useful!" alt="Footer" />

</div>
