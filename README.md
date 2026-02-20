# 🔄 CureLoop-MLOps: Automated Disease Prediction Pipeline

> **"Transforming static notebooks into a living, breathing AI system."**

## 🚀 Project Evolution
This repository represents the **production-grade evolution** of my original [Medicine Recommendation project](https://github.com/mayank-goyal09/medicine-recommendation-system). 

| Feature | 🏛️ Original (Legacy) | ⚡ **CureLoop (New)** |
| :--- | :--- | :--- |
| **Model Training** | Manual Execution in Notebooks | **Automated** on every code push via GitHub Actions |
| **Deployment** | Local Only | **Cloud Native** (Docker + Render) |
| **Interface** | CLI / Notebook Output | **FastAPI REST Endpoints** |
| **Reliability** | No Tests | **Automated Unit Tests** (Pytest) |
| **Scalability** | Single Machine | **Containerized** (Runs anywhere) |

---

## 🛠️ The MLOps Pipeline
This project implements a complete **CI/CD pipeline** for Machine Learning:
1.  **Code Push**: Developer pushes new code or data.
2.  **Linting**: GitHub Actions checks for syntax errors.
3.  **Auto-Training**: The system automatically retrains the model on the latest data.
4.  **Testing**: Unit tests validate the API and model accuracy.
5.  **Deployment**: On success, the app is automatically deployed to the cloud.

## 📂 Project Structure
```bash
CureLoop-MLOps/
├── .github/workflows/ # CI/CD Configurations
├── app/               # FastAPI Application Source
├── data/              # Medical Datasets
├── models/            # Serialized Models (.joblib)
├── tests/             # Pytest Suites
├── Dockerfile         # Container Instructions
└── train.py           # Automated Training Script
```

## 💻 Tech Stack
*   **Core**: Python 3.9
*   **ML**: Scikit-Learn, Pandas, NumPy
*   **API**: FastAPI, Uvicorn
*   **Ops**: Docker, GitHub Actions, Hugging Face Spaces 🤗

## 🚀 Deployment (Free Alternative)
This project is configured to deploy automatically to **Hugging Face Spaces** (Docker).

### Prerequisite Setup:
1.  Create a **New Space** on Hugging Face (Visual: Public, SDK: Docker).
2.  Get your **HF Access Token** (Write permission) from Settings -> Access Tokens.
3.  Add Secrets to this GitHub Repo (Settings -> Secrets and variables -> Actions):
    *   `HF_TOKEN`: Your Hugging Face token (starts with `hf_...`).
    *   `HF_USERNAME`: Your Hugging Face username (e.g., `mayank-goyal09`).
    *   `HF_SPACE_NAME`: The name of the Space you created (e.g., `medicine-api`).

## 🔧 How to Run Locally
1.  **Clone the Repo**
    ```bash
    git clone https://github.com/your-username/CureLoop-MLOps.git
    cd CureLoop-MLOps
    ```
2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the Training Script**
    ```bash
    python train.py
    ```
4.  **Start the Server**
    ```bash
    uvicorn app.main:app --reload
    ```
