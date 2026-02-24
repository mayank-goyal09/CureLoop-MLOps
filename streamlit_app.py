import streamlit as st
import requests
import time
import random

# ──────────────────────────────────────────────────────────
# CONSTANTS
# ──────────────────────────────────────────────────────────
API_BASE = "https://mayankg09-cureloop-mlops.hf.space"
API_PREDICT = f"{API_BASE}/predict"

# ──────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CureLoop · AI Medicine Advisor",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────
# SYMPTOM LIST (all 132 symptoms from the trained model)
# ──────────────────────────────────────────────────────────
ALL_SYMPTOMS = [
    "abdominal_pain", "abnormal_menstruation", "acidity", "acute_liver_failure",
    "altered_sensorium", "anxiety", "back_pain", "belly_pain", "blackheads",
    "bladder_discomfort", "blister", "blood_in_sputum", "bloody_stool",
    "blurred_and_distorted_vision", "breathlessness", "brittle_nails",
    "bruising", "burning_micturition", "chest_pain", "chills", "cold_hands_and_feets",
    "coma", "congestion", "constipation", "continuous_feel_of_urine",
    "continuous_sneezing", "cough", "cramps", "dark_urine", "dehydration",
    "depression", "diarrhoea", "dischromic_patches", "distention_of_abdomen",
    "dizziness", "drawing_of_gas", "drying_and_tingling_lips", "enlarged_thyroid",
    "excessive_hunger", "extra_marital_contacts", "family_history",
    "fast_heart_rate", "fatigue", "fluid_overload", "foul_smell_of_urine",
    "headache", "high_fever", "hip_joint_pain", "history_of_alcohol_consumption",
    "increased_appetite", "indigestion", "inflammatory_nails", "internal_itching",
    "irregular_sugar_level", "irritability", "irritation_in_anus",
    "itching", "joint_pain", "knee_pain", "lack_of_concentration",
    "lethargy", "loss_of_appetite", "loss_of_balance", "loss_of_smell",
    "malaise", "mild_fever", "mood_swings", "movement_stiffness",
    "mucoid_sputum", "muscle_pain", "muscle_wasting", "muscle_weakness",
    "nausea", "neck_pain", "nodal_skin_eruptions", "obesity",
    "pain_behind_the_eyes", "pain_during_bowel_movements", "pain_in_anal_region",
    "painful_walking", "palpitations", "passage_of_gases", "patches_in_throat",
    "phlegm", "polyuria", "prominent_veins_on_calf", "puffy_face_and_eyes",
    "pus_filled_pimples", "receiving_blood_transfusion",
    "receiving_unsterile_injections", "red_sore_around_nose",
    "red_spots_over_body", "redness_of_eyes", "restlessness", "runny_nose",
    "rusty_sputum", "scurring", "shivering", "silver_like_dusting",
    "sinus_pressure", "skin_peeling", "skin_rash", "slurred_speech",
    "small_dents_in_nails", "spinning_movements", "spotting_urination",
    "stiff_neck", "stomach_bleeding", "stomach_pain", "sunken_eyes",
    "sweating", "swelled_lymph_nodes", "swelling_joints",
    "swelling_of_stomach", "swollen_blood_vessels", "swollen_extremeties",
    "swollen_legs", "throat_irritation", "toxic_look_(typhos)",
    "ulcers_on_tongue", "unsteadiness", "visual_disturbances", "vomiting",
    "watering_from_eyes", "weakness_in_limbs", "weakness_of_one_body_side",
    "weight_gain", "weight_loss", "yellow_crust_ooze", "yellow_urine",
    "yellowing_of_eyes", "yellowish_skin",
]

# ──────────────────────────────────────────────────────────
# HELPER: prettify symptom names for display
# ──────────────────────────────────────────────────────────
def pretty(name: str) -> str:
    return name.replace("_", " ").title()

def ugly(name: str) -> str:
    return name.strip().lower().replace(" ", "_")

# ──────────────────────────────────────────────────────────
# INJECT CUSTOM CSS & ANIMATED BACKGROUND
# ──────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ─── Google Fonts ────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ─── Root variables ─────────────────────────────── */
:root {
    --bg-primary: #0a0e1a;
    --bg-secondary: #111827;
    --bg-card: rgba(17, 24, 39, 0.85);
    --bg-card-hover: rgba(20, 30, 55, 0.95);
    --accent-teal: #00d4aa;
    --accent-teal-glow: rgba(0, 212, 170, 0.3);
    --accent-blue: #3b82f6;
    --accent-emerald: #10b981;
    --accent-purple: #8b5cf6;
    --accent-rose: #f43f5e;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --border-color: rgba(0, 212, 170, 0.15);
    --glass-bg: rgba(15, 23, 42, 0.6);
    --glass-border: rgba(255,255,255,0.08);
}

/* ─── Animated BG: medical glow ──────────────────── */
.stApp {
    background: var(--bg-primary) !important;
    overflow-x: hidden;
}

.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    z-index: 0;
    pointer-events: none;
    background:
        radial-gradient(ellipse 600px 600px at 15% 20%, rgba(0,212,170,0.10) 0%, transparent 70%),
        radial-gradient(ellipse 500px 500px at 80% 70%, rgba(59,130,246,0.08) 0%, transparent 70%),
        radial-gradient(ellipse 400px 400px at 50% 50%, rgba(139,92,246,0.06) 0%, transparent 70%);
    animation: bgPulse 8s ease-in-out infinite alternate;
}

@keyframes bgPulse {
    0%   { opacity: 0.7; transform: scale(1); }
    100% { opacity: 1;   transform: scale(1.05); }
}

/* ─── Scrollbar ──────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--accent-teal); border-radius: 10px; }

/* ─── Main container ─────────────────────────────── */
.block-container {
    max-width: 1200px !important;
    padding: 2rem 2rem 4rem 2rem !important;
}

/* ─── Override ALL default text ──────────────────── */
html, body, .stApp, .stApp * {
    font-family: 'Inter', sans-serif !important;
    color: var(--text-primary);
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
}

/* ─── Sidebar ────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1321 0%, #111827 100%) !important;
    border-right: 1px solid var(--border-color) !important;
}

section[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1rem !important;
}

/* ─── Multiselect (symptom picker) ───────────────── */
div[data-baseweb="select"] {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
}

div[data-baseweb="select"]:focus-within {
    border-color: var(--accent-teal) !important;
    box-shadow: 0 0 0 2px var(--accent-teal-glow) !important;
}

div[data-baseweb="tag"] {
    background: linear-gradient(135deg, rgba(0,212,170,0.2), rgba(59,130,246,0.2)) !important;
    border: 1px solid var(--accent-teal) !important;
    border-radius: 20px !important;
    color: var(--accent-teal) !important;
}

/* ─── Buttons ────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #00d4aa 0%, #00b89c 50%, #009e85 100%) !important;
    color: #0a0e1a !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.85rem 2.5rem !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    letter-spacing: 0.5px;
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1) !important;
    box-shadow: 0 4px 20px rgba(0,212,170,0.3) !important;
    text-transform: uppercase;
}

.stButton > button:hover {
    transform: translateY(-2px) scale(1.03) !important;
    box-shadow: 0 8px 30px rgba(0,212,170,0.5) !important;
}

.stButton > button:active {
    transform: translateY(0) scale(0.98) !important;
}

/* ─── Metric Cards ───────────────────────────────── */
div[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 16px !important;
    padding: 1.2rem 1.5rem !important;
    backdrop-filter: blur(12px) !important;
    transition: all 0.3s ease !important;
}

div[data-testid="stMetric"]:hover {
    border-color: var(--accent-teal) !important;
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(0,212,170,0.15) !important;
}

div[data-testid="stMetric"] label {
    color: var(--text-secondary) !important;
}

div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
    color: var(--accent-teal) !important;
    font-weight: 700 !important;
}

/* ─── Expander ───────────────────────────────────── */
details {
    background: var(--bg-card) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(10px) !important;
    transition: all 0.3s ease !important;
}

details:hover {
    border-color: var(--accent-teal) !important;
}

details summary {
    font-weight: 600 !important;
}

/* ─── Tabs ───────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: var(--bg-secondary) !important;
    border-radius: 14px !important;
    padding: 6px !important;
    border: 1px solid var(--glass-border) !important;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    padding: 10px 20px !important;
    font-weight: 600 !important;
    color: var(--text-secondary) !important;
    transition: all 0.3s ease !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(0,212,170,0.2), rgba(59,130,246,0.15)) !important;
    color: var(--accent-teal) !important;
    border-bottom: none !important;
}

/* ─── Custom card class ──────────────────────────── */
.cure-card {
    background: var(--bg-card);
    border: 1px solid var(--glass-border);
    border-radius: 20px;
    padding: 2rem;
    backdrop-filter: blur(12px);
    transition: all 0.4s cubic-bezier(0.4,0,0.2,1);
    position: relative;
    overflow: hidden;
}

.cure-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 3px;
    background: linear-gradient(90deg, var(--accent-teal), var(--accent-blue), var(--accent-purple));
}

.cure-card:hover {
    border-color: var(--accent-teal);
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(0,212,170,0.12);
}

/* ─── Hero Title ─────────────────────────────────── */
.hero-title {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #00d4aa 0%, #3b82f6 50%, #8b5cf6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1px;
    line-height: 1.15;
    margin-bottom: 0.3rem;
    animation: fadeInUp 1s ease-out;
}

.hero-subtitle {
    font-size: 1.1rem;
    color: var(--text-secondary);
    font-weight: 400;
    margin-bottom: 2rem;
    animation: fadeInUp 1s ease-out 0.2s both;
}

.hero-badge {
    display: inline-block;
    background: rgba(0,212,170,0.1);
    border: 1px solid rgba(0,212,170,0.25);
    border-radius: 50px;
    padding: 6px 18px;
    font-size: 0.8rem;
    color: #00d4aa;
    font-weight: 600;
    letter-spacing: 1px;
    margin-bottom: 1rem;
    animation: fadeInUp 0.8s ease-out;
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ─── Section Headers ────────────────────────────── */
.section-header {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 2rem 0 1rem 0;
    display: flex;
    align-items: center;
    gap: 10px;
}

/* ─── Pill Badges ────────────────────────────────── */
.pill {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 600;
    margin: 4px;
    transition: all 0.3s ease;
}

.pill-teal {
    background: rgba(0,212,170,0.12);
    border: 1px solid rgba(0,212,170,0.3);
    color: #00d4aa;
}

.pill-blue {
    background: rgba(59,130,246,0.12);
    border: 1px solid rgba(59,130,246,0.3);
    color: #60a5fa;
}

.pill-purple {
    background: rgba(139,92,246,0.12);
    border: 1px solid rgba(139,92,246,0.3);
    color: #a78bfa;
}

.pill-rose {
    background: rgba(244,63,94,0.12);
    border: 1px solid rgba(244,63,94,0.3);
    color: #fb7185;
}

.pill-emerald {
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.3);
    color: #34d399;
}

/* ─── Info List ──────────────────────────────────── */
.info-item {
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    padding: 12px 18px;
    margin: 8px 0;
    display: flex;
    align-items: center;
    gap: 12px;
    transition: all 0.3s ease;
}

.info-item:hover {
    background: rgba(0,212,170,0.06);
    border-color: rgba(0,212,170,0.2);
    transform: translateX(6px);
}

/* ─── Diagnosis Result Card ──────────────────────── */
.diagnosis-result {
    background: linear-gradient(135deg, rgba(0,212,170,0.08), rgba(59,130,246,0.06));
    border: 1px solid rgba(0,212,170,0.25);
    border-radius: 24px;
    padding: 2.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    animation: resultAppear 0.6s cubic-bezier(0.4,0,0.2,1);
}

.diagnosis-result::after {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: conic-gradient(from 0deg, transparent, rgba(0,212,170,0.05), transparent, rgba(59,130,246,0.05), transparent);
    animation: rotate 10s linear infinite;
}

@keyframes rotate {
    to { transform: rotate(360deg); }
}

@keyframes resultAppear {
    from { opacity: 0; transform: scale(0.9); }
    to   { opacity: 1; transform: scale(1); }
}

.disease-name {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 2.2rem;
    font-weight: 800;
    color: #00d4aa;
    position: relative;
    z-index: 1;
    text-shadow: 0 0 40px rgba(0,212,170,0.3);
}

/* ─── Floating DNA particles ─────────────────────── */
.dna-container {
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}

.dna-particle {
    position: absolute;
    border-radius: 50%;
    opacity: 0.15;
    animation: float linear infinite;
}

@keyframes float {
    0%   { transform: translateY(100vh) rotate(0deg); opacity: 0; }
    10%  { opacity: 0.15; }
    90%  { opacity: 0.15; }
    100% { transform: translateY(-10vh) rotate(720deg); opacity: 0; }
}

/* ─── Heartbeat line ─────────────────────────────── */
.heartbeat-line {
    width: 100%;
    height: 60px;
    overflow: hidden;
    position: relative;
    margin: 1rem 0;
}

.heartbeat-line svg {
    position: absolute;
    animation: heartbeatScroll 3s linear infinite;
}

@keyframes heartbeatScroll {
    from { transform: translateX(0); }
    to   { transform: translateX(-50%); }
}

/* ─── Disclaimer ─────────────────────────────────── */
.disclaimer {
    background: rgba(244,63,94,0.08);
    border: 1px solid rgba(244,63,94,0.2);
    border-radius: 14px;
    padding: 1rem 1.5rem;
    margin-top: 2rem;
    font-size: 0.85rem;
    color: #fb7185;
}

/* ─── Stat grid ──────────────────────────────────── */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin: 1.5rem 0;
}

.stat-box {
    background: var(--bg-card);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.3s ease;
}

.stat-box:hover {
    border-color: var(--accent-teal);
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(0,212,170,0.1);
}

.stat-number {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #00d4aa, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.stat-label {
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin-top: 4px;
}

/* ─── API Badge ──────────────────────────────────── */
.api-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 50px;
    padding: 5px 14px;
    font-size: 0.75rem;
    font-weight: 600;
    color: #34d399;
}

.api-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #34d399;
    animation: blink 1.5s ease-in-out infinite;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* ─── hide streamlit defaults ────────────────────── */
#MainMenu { visibility: hidden; }
header { visibility: hidden; }
footer { visibility: hidden; }

/* ─── Progress shimmer ───────────────────────────── */
.shimmer {
    background: linear-gradient(90deg, var(--bg-card) 25%, rgba(0,212,170,0.08) 50%, var(--bg-card) 75%);
    background-size: 200% 100%;
    animation: shimmer 2s ease-in-out infinite;
    border-radius: 12px;
    height: 20px;
    margin: 8px 0;
}

@keyframes shimmer {
    from { background-position: 200% 0; }
    to   { background-position: -200% 0; }
}

</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
# FLOATING PARTICLES (DNA-like)
# ──────────────────────────────────────────────────────────
particles_html = '<div class="dna-container">'
colors = ["#00d4aa", "#3b82f6", "#8b5cf6", "#10b981", "#f43f5e"]
for i in range(30):
    size = random.randint(3, 8)
    left = random.randint(0, 100)
    dur = random.randint(15, 40)
    delay = random.randint(0, 20)
    c = colors[i % len(colors)]
    particles_html += (
        f'<div class="dna-particle" style="'
        f'width:{size}px;height:{size}px;'
        f'left:{left}%;'
        f'background:{c};'
        f'animation-duration:{dur}s;'
        f'animation-delay:{delay}s;'
        f'box-shadow:0 0 {size*3}px {c};'
        f'"></div>'
    )
particles_html += '</div>'
st.markdown(particles_html, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
# HEARTBEAT LINE SVG
# ──────────────────────────────────────────────────────────
heartbeat_svg = """
<div class="heartbeat-line">
  <svg width="2000" height="60" viewBox="0 0 2000 60">
    <polyline fill="none" stroke="rgba(0,212,170,0.25)" stroke-width="2"
      points="0,30 80,30 100,30 110,10 120,50 130,20 140,40 150,30 200,30
              280,30 300,30 310,10 320,50 330,20 340,40 350,30 400,30
              480,30 500,30 510,10 520,50 530,20 540,40 550,30 600,30
              680,30 700,30 710,10 720,50 730,20 740,40 750,30 800,30
              880,30 900,30 910,10 920,50 930,20 940,40 950,30 1000,30
              1080,30 1100,30 1110,10 1120,50 1130,20 1140,40 1150,30 1200,30
              1280,30 1300,30 1310,10 1320,50 1330,20 1340,40 1350,30 1400,30
              1480,30 1500,30 1510,10 1520,50 1530,20 1540,40 1550,30 1600,30
              1680,30 1700,30 1710,10 1720,50 1730,20 1740,40 1750,30 1800,30
              1880,30 1900,30 1910,10 1920,50 1930,20 1940,40 1950,30 2000,30"/>
  </svg>
</div>
"""

# ──────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; margin-bottom:1.5rem;">
        <div style="font-size:3.5rem; margin-bottom:0.5rem;">🧬</div>
        <div style="font-family:'Space Grotesk',sans-serif; font-size:1.6rem; font-weight:800;
                    background:linear-gradient(135deg,#00d4aa,#3b82f6);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text;">
            CureLoop
        </div>
        <div style="color:#64748b; font-size:0.85rem; margin-top:2px;">
            AI-Powered Medicine Advisor
        </div>
        <div style="margin-top:10px;">
            <span class="api-badge">
                <span class="api-dot"></span>
                API Connected · HuggingFace
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(heartbeat_svg, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin:1rem 0;">
        <div class="stat-grid">
            <div class="stat-box">
                <div class="stat-number">41</div>
                <div class="stat-label">Diseases</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">132</div>
                <div class="stat-label">Symptoms</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">98%</div>
                <div class="stat-label">Accuracy</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div style="font-weight:600; font-size:0.95rem; margin-bottom:0.5rem; color:#94a3b8;">
        🔬 How It Works
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-item">
        <span style="font-size:1.3rem;">1️⃣</span>
        <span style="font-size:0.85rem; color:#94a3b8;">Select your symptoms from the dropdown</span>
    </div>
    <div class="info-item">
        <span style="font-size:1.3rem;">2️⃣</span>
        <span style="font-size:0.85rem; color:#94a3b8;">Click <b style="color:#00d4aa">Diagnose</b> to query the API</span>
    </div>
    <div class="info-item">
        <span style="font-size:1.3rem;">3️⃣</span>
        <span style="font-size:0.85rem; color:#94a3b8;">Get disease prediction + full care plan</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown(f"""
    <div style="font-size:0.8rem; color:#475569; margin-bottom:0.5rem;">
        <b style="color:#94a3b8;">🔗 API Endpoint</b><br>
        <a href="{API_BASE}/docs" target="_blank" 
           style="color:#00d4aa; text-decoration:none; word-break:break-all;">
            {API_BASE}/docs
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer">
        ⚠️ <b>Disclaimer</b>: This is an AI tool for educational purposes. 
        Always consult a qualified healthcare professional for medical advice.
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────
# MAIN CONTENT
# ──────────────────────────────────────────────────────────

# --- Hero ---
st.markdown("""
<div style="text-align:center; margin-bottom:1rem; position:relative; z-index:1;">
    <div class="hero-badge">🚀 POWERED BY FASTAPI + HUGGING FACE SPACES</div>
    <div class="hero-title">🩺 CureLoop</div>
    <div class="hero-subtitle">
        Intelligent Symptom Analysis · Disease Prediction · Personalised Care Plans
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(heartbeat_svg, unsafe_allow_html=True)

# --- Symptom input card ---
st.markdown('<div class="cure-card" style="position:relative; z-index:1;">', unsafe_allow_html=True)
st.markdown("""
<div class="section-header">
    <span style="font-size:1.5rem;">🔍</span>
    Symptom Analysis Panel
</div>
<p style="color:var(--text-secondary); font-size:0.9rem; margin-bottom:1rem;">
    Start typing or browse the list to select your symptoms. You can select multiple symptoms for more accurate diagnosis.
</p>
""", unsafe_allow_html=True)

# Prettified symptom list for display
display_symptoms = sorted([pretty(s) for s in ALL_SYMPTOMS])

selected = st.multiselect(
    "Select your symptoms",
    options=display_symptoms,
    placeholder="🔎 Type to search symptoms…",
    label_visibility="collapsed",
)

col_btn, col_info = st.columns([1, 2])
with col_btn:
    diagnose_clicked = st.button("🧬 Diagnose Now", use_container_width=True)
with col_info:
    if selected:
        st.markdown(
            f'<div style="padding:12px; color:#94a3b8; font-size:0.9rem;">'
            f'<span style="color:#00d4aa; font-weight:700;">{len(selected)}</span> symptom(s) selected'
            f'</div>',
            unsafe_allow_html=True,
        )

st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
# RESULTS
# ──────────────────────────────────────────────────────────
if diagnose_clicked:
    if not selected:
        st.warning("⚠️ Please select at least one symptom before diagnosing.")
    else:
        # Animated progress
        progress_placeholder = st.empty()
        with progress_placeholder.container():
            st.markdown("""
            <div style="text-align:center; padding:2rem; position:relative; z-index:1;">
                <div style="font-size:2.5rem; animation: pulse 1s ease-in-out infinite alternate;">🧬</div>
                <div style="color:#94a3b8; margin-top:0.8rem; font-size:0.95rem;">
                    Sending symptoms to CureLoop API…
                </div>
                <div class="shimmer" style="max-width:300px; margin:1rem auto;"></div>
                <div style="color:#475569; font-size:0.75rem; margin-top:0.5rem;">
                    Connecting to HuggingFace Spaces backend
                </div>
            </div>
            <style>
                @keyframes pulse { from {transform:scale(1)} to {transform:scale(1.2)} }
            </style>
            """, unsafe_allow_html=True)

        # ─── Call the FastAPI backend ────────────────
        raw_symptoms = [ugly(s) for s in selected]
        try:
            response = requests.post(
                API_PREDICT,
                json={"symptoms": raw_symptoms},
                timeout=30,
            )
            progress_placeholder.empty()

            if response.status_code == 200:
                data = response.json()

                disease = data.get("predicted_disease", "Unknown")
                desc = data.get("description", "No description available.")
                found = data.get("recognized_symptoms", [])
                ignored = data.get("ignored_symptoms", [])
                precautions = data.get("precautions", [])
                meds = data.get("medications", [])
                diets = data.get("diet", [])

                # ─── Disease Result Card ─────────────────────
                st.markdown(f"""
                <div class="diagnosis-result" style="position:relative; z-index:1;">
                    <div style="position:relative; z-index:1;">
                        <div style="font-size:0.9rem; text-transform:uppercase; letter-spacing:2px;
                                    color:#64748b; font-weight:600; margin-bottom:0.5rem;">
                            AI Diagnosis Result
                        </div>
                        <div class="disease-name">{disease}</div>
                        <div style="color:#94a3b8; font-size:0.95rem; margin-top:1rem; max-width:700px;
                                    margin-left:auto; margin-right:auto; line-height:1.7;">
                            {desc}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # ─── Recognized / Ignored pills ──────────────
                if found:
                    pills_html = '<div style="margin-bottom:0.5rem;"><span style="color:#94a3b8; font-size:0.85rem; font-weight:600;">✅ Recognized: </span>'
                    for f_sym in found:
                        pills_html += f'<span class="pill pill-teal">{pretty(f_sym)}</span>'
                    pills_html += '</div>'
                    st.markdown(pills_html, unsafe_allow_html=True)

                if ignored:
                    pills_html = '<div style="margin-bottom:1rem;"><span style="color:#94a3b8; font-size:0.85rem; font-weight:600;">⚠️ Unrecognized: </span>'
                    for ig in ignored:
                        pills_html += f'<span class="pill pill-rose">{pretty(ig)}</span>'
                    pills_html += '</div>'
                    st.markdown(pills_html, unsafe_allow_html=True)

                st.markdown(heartbeat_svg, unsafe_allow_html=True)

                # ─── Tabs for Details ────────────────────────
                tab_prec, tab_med, tab_diet = st.tabs([
                    "🛡️ Precautions",
                    "💊 Medications",
                    "🥗 Diet Plan",
                ])

                with tab_prec:
                    st.markdown('<div class="section-header"><span>🛡️</span> Recommended Precautions</div>', unsafe_allow_html=True)
                    if precautions:
                        for i, p in enumerate(precautions, 1):
                            st.markdown(f"""
                            <div class="info-item">
                                <span style="background:linear-gradient(135deg,#00d4aa,#3b82f6);
                                             -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                                             font-weight:800; font-size:1.1rem; min-width:24px;">{i}</span>
                                <span style="color:#cbd5e1;">{p}</span>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("No specific precautions found for this condition.")

                with tab_med:
                    st.markdown('<div class="section-header"><span>💊</span> Suggested Medications</div>', unsafe_allow_html=True)
                    if meds:
                        pills_html = '<div style="display:flex; flex-wrap:wrap; gap:6px;">'
                        for m in meds:
                            m_clean = str(m).strip("[]'\" ")
                            for med_item in m_clean.split(","):
                                med_item = med_item.strip().strip("'\" ")
                                if med_item:
                                    pills_html += f'<span class="pill pill-blue">💊 {med_item}</span>'
                        pills_html += '</div>'
                        st.markdown(pills_html, unsafe_allow_html=True)
                    else:
                        st.info("No specific medications found for this condition.")

                    st.markdown("""
                    <div class="disclaimer" style="margin-top:1.5rem;">
                        ⚠️ <b>Important</b>: Never self-medicate. Consult a licensed physician before taking any medication.
                    </div>
                    """, unsafe_allow_html=True)

                with tab_diet:
                    st.markdown('<div class="section-header"><span>🥗</span> Recommended Diet</div>', unsafe_allow_html=True)
                    if diets:
                        for d in diets:
                            d_clean = str(d).strip("[]'\" ")
                            items = [x.strip().strip("'\" ") for x in d_clean.split(",")]
                            for item in items:
                                if item:
                                    st.markdown(f"""
                                    <div class="info-item">
                                        <span style="font-size:1.2rem;">🥬</span>
                                        <span style="color:#cbd5e1;">{item}</span>
                                    </div>
                                    """, unsafe_allow_html=True)
                    else:
                        st.info("No specific diet recommendations found.")

                # ─── Summary Metrics ─────────────────────────
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div class="section-header"><span>📊</span> Diagnosis Summary</div>', unsafe_allow_html=True)

                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Disease", disease)
                m2.metric("Precautions", len(precautions))
                m3.metric("Medications", len(meds))
                m4.metric("Diet Items", len(diets))

            elif response.status_code == 400:
                progress_placeholder.empty()
                detail = response.json().get("detail", "Invalid symptoms.")
                st.error(f"❌ API Error: {detail}")
            else:
                progress_placeholder.empty()
                st.error(f"❌ API returned status {response.status_code}. Please try again.")

        except requests.exceptions.Timeout:
            progress_placeholder.empty()
            st.error("⏱️ The API is taking too long to respond. The HuggingFace Space may be waking up — please try again in 30 seconds.")
        except requests.exceptions.ConnectionError:
            progress_placeholder.empty()
            st.error("🔌 Cannot connect to the API. The HuggingFace Space may be sleeping. Please wait a minute and try again.")
        except Exception as e:
            progress_placeholder.empty()
            st.error(f"❌ Unexpected error: {str(e)}")


# ──────────────────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align:center; padding:2rem; border-top:1px solid rgba(255,255,255,0.06);
            position:relative; z-index:1;">
    <div style="font-family:'Space Grotesk',sans-serif; font-size:1.1rem; font-weight:700;
                background:linear-gradient(135deg,#00d4aa,#3b82f6);
                -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                background-clip:text; margin-bottom:0.3rem;">
        CureLoop · MLOps Pipeline
    </div>
    <div style="color:#475569; font-size:0.8rem;">
        Decision Tree Classifier · scikit-learn · FastAPI · Streamlit<br>
        <a href="{API_BASE}/docs" target="_blank" style="color:#00d4aa; text-decoration:none;">
            📡 API Documentation
        </a>
        &nbsp;·&nbsp; Built with 💚 for better healthcare access
    </div>
</div>
""", unsafe_allow_html=True)
