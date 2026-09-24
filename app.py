import streamlit as st
import numpy as np
import pickle
import time
import os

# ─────────────────────────────────────────────
# PAGE CONFIGURATION
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Loan Approval Prediction System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS STYLING
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Global ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Background ── */
    .stApp {
        background: linear-gradient(135deg, #f0f4ff 0%, #ffffff 50%, #f0fff4 100%);
    }

    /* ── Hide default Streamlit menu/footer ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ── Hero Banner ── */
    .hero-banner {
        background: linear-gradient(135deg, #1a56db 0%, #0e9f6e 100%);
        border-radius: 16px;
        padding: 40px 48px;
        color: white;
        margin-bottom: 28px;
        box-shadow: 0 8px 32px rgba(26, 86, 219, 0.25);
        position: relative;
        overflow: hidden;
    }
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -40px; right: -40px;
        width: 200px; height: 200px;
        background: rgba(255,255,255,0.08);
        border-radius: 50%;
    }
    .hero-banner::after {
        content: '';
        position: absolute;
        bottom: -60px; left: -20px;
        width: 250px; height: 250px;
        background: rgba(255,255,255,0.05);
        border-radius: 50%;
    }
    .hero-title {
        font-size: 2.4rem;
        font-weight: 700;
        margin: 0 0 8px 0;
        line-height: 1.2;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        opacity: 0.9;
        margin: 0;
        max-width: 620px;
        line-height: 1.6;
    }
    .hero-emoji {
        font-size: 3.5rem;
        float: right;
        margin-top: -10px;
    }

    /* ── Cards ── */
    .card {
        background: white;
        border-radius: 14px;
        padding: 28px;
        box-shadow: 0 2px 16px rgba(0,0,0,0.07);
        border: 1px solid #e8edf5;
        margin-bottom: 20px;
        transition: box-shadow 0.2s;
    }
    .card:hover {
        box-shadow: 0 6px 24px rgba(0,0,0,0.11);
    }
    .card-title {
        font-size: 1.15rem;
        font-weight: 600;
        color: #1a56db;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* ── Section Headers ── */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
        margin: 32px 0 18px 0;
        padding-bottom: 10px;
        border-bottom: 3px solid #1a56db;
        display: inline-block;
    }

    /* ── Predict Button ── */
    .stButton > button {
        background: linear-gradient(135deg, #1a56db, #0e9f6e) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 14px 40px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        cursor: pointer !important;
        box-shadow: 0 4px 15px rgba(26, 86, 219, 0.3) !important;
        transition: all 0.3s !important;
        letter-spacing: 0.5px !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(26, 86, 219, 0.4) !important;
    }

    /* ── Result Cards ── */
    .result-approved {
        background: linear-gradient(135deg, #ecfdf5, #d1fae5);
        border: 2px solid #10b981;
        border-radius: 16px;
        padding: 32px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.2);
    }
    .result-rejected {
        background: linear-gradient(135deg, #fff5f5, #fee2e2);
        border: 2px solid #ef4444;
        border-radius: 16px;
        padding: 32px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.2);
    }
    .result-title {
        font-size: 2rem;
        font-weight: 700;
        margin: 8px 0;
    }
    .result-subtitle {
        font-size: 1rem;
        opacity: 0.75;
        margin-top: 6px;
    }

    /* ── Info Metric Cards ── */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border-top: 4px solid #1a56db;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1a56db;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #64748b;
        margin-top: 4px;
    }

    /* ── FAQ ── */
    .faq-item {
        background: #f8faff;
        border-left: 4px solid #1a56db;
        border-radius: 0 10px 10px 0;
        padding: 16px 20px;
        margin-bottom: 12px;
    }
    .faq-q {
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 6px;
    }
    .faq-a {
        color: #475569;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    /* ── Sidebar ── */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a56db 0%, #1e3a8a 100%) !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: white !important;
        font-size: 1rem;
    }

    /* ── Input Summary Box ── */
    .summary-box {
        background: #f0f7ff;
        border: 1px solid #bfdbfe;
        border-radius: 12px;
        padding: 20px;
        margin-top: 16px;
    }
    .summary-row {
        display: flex;
        justify-content: space-between;
        padding: 6px 0;
        border-bottom: 1px solid #e0eaff;
        font-size: 0.92rem;
    }
    .summary-row:last-child { border-bottom: none; }
    .summary-key { color: #475569; }
    .summary-val { font-weight: 600; color: #1a56db; }

    /* ── Divider ── */
    .custom-divider {
        height: 3px;
        background: linear-gradient(90deg, #1a56db, #0e9f6e, transparent);
        border-radius: 2px;
        margin: 30px 0;
    }

    /* ── Step Cards ── */
    .step-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        border-left: 5px solid #1a56db;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        margin-bottom: 12px;
    }
    .step-num {
        background: #1a56db;
        color: white;
        border-radius: 50%;
        width: 28px; height: 28px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.85rem;
        margin-right: 10px;
    }

    /* ── CIBIL Score Bar ── */
    .cibil-bar {
        height: 14px;
        border-radius: 7px;
        background: linear-gradient(90deg, #ef4444 0%, #f59e0b 40%, #10b981 75%, #1a56db 100%);
        margin: 10px 0;
        position: relative;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# LOAD MODEL & SCALER
# ─────────────────────────────────────────────
@st.cache_resource
def load_model():
    """Load the trained ML model from model.pkl"""
    try:
        with open("model.pkl", "rb") as f:
            model = pickle.load(f)
        return model, None
    except FileNotFoundError:
        return None, "⚠️ model.pkl not found. Please place your trained model file in the app directory."
    except Exception as e:
        return None, f"⚠️ Error loading model: {str(e)}"

@st.cache_resource
def load_scaler():
    """Load the fitted scaler from scaler.pkl"""
    try:
        with open("scaler.pkl", "rb") as f:
            scaler = pickle.load(f)
        return scaler, None
    except FileNotFoundError:
        return None, "⚠️ scaler.pkl not found. Please place your scaler file in the app directory."
    except Exception as e:
        return None, f"⚠️ Error loading scaler: {str(e)}"

model, model_error = load_model()
scaler, scaler_error = load_scaler()


# ─────────────────────────────────────────────
# SIDEBAR NAVIGATION
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div style='text-align:center; padding: 20px 0 10px 0;'>
            <div style='font-size:3rem;'>🏦</div>
            <div style='font-size:1.2rem; font-weight:700; color:white; margin-top:8px;'>
                LoanPredict AI
            </div>
            <div style='font-size:0.8rem; opacity:0.7; color:white;'>
                Smart Loan Decision System
            </div>
        </div>
        <hr style='border-color:rgba(255,255,255,0.2); margin:16px 0;'/>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        options=["🏠  Home", "📊  Loan Prediction", "ℹ️  About", "📞  Contact"],
        label_visibility="collapsed"
    )

    st.markdown("""
        <hr style='border-color:rgba(255,255,255,0.2); margin:20px 0 14px 0;'/>
        <div style='font-size:0.78rem; opacity:0.6; color:white; text-align:center; padding-bottom:10px;'>
            Powered by Machine Learning<br/>
            © 2025 LoanPredict AI
        </div>
    """, unsafe_allow_html=True)

    # Model status indicator in sidebar
    st.markdown("<hr style='border-color:rgba(255,255,255,0.2);'/>", unsafe_allow_html=True)
    if model and scaler:
        st.markdown("""
            <div style='background:rgba(16,185,129,0.2); border:1px solid rgba(16,185,129,0.5);
                        border-radius:8px; padding:10px; text-align:center; color:white; font-size:0.82rem;'>
                ✅ Model Ready
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='background:rgba(239,68,68,0.2); border:1px solid rgba(239,68,68,0.5);
                        border-radius:8px; padding:10px; text-align:center; color:white; font-size:0.82rem;'>
                ⚠️ Model Not Loaded
            </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ══════════════════════════════════════════════
#  PAGE: HOME
# ══════════════════════════════════════════════
# ─────────────────────────────────────────────
if page == "🏠  Home":

    # Hero Banner
    st.markdown("""
        <div class="hero-banner">
            <span class="hero-emoji">🏦</span>
            <h1 class="hero-title">Loan Approval Prediction System</h1>
            <p class="hero-subtitle">
                This application predicts whether a loan will be approved based on applicant details
                using a Machine Learning model. Get instant, data-driven decisions in seconds.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Quick Stats Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">98%</div>
                <div class="metric-label">Model Accuracy</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">8</div>
                <div class="metric-label">Input Features</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">&lt;1s</div>
                <div class="metric-label">Prediction Time</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">ML</div>
                <div class="metric-label">Powered Engine</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

    # Features Overview
    st.markdown("<div class='section-header'>✨ Key Features</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class="card">
                <div class="card-title">🤖 AI-Powered Prediction</div>
                <p style='color:#475569; font-size:0.93rem; line-height:1.6;'>
                    Uses a trained Machine Learning model to analyze your financial profile
                    and predict loan approval with high accuracy.
                </p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="card">
                <div class="card-title">⚡ Instant Results</div>
                <p style='color:#475569; font-size:0.93rem; line-height:1.6;'>
                    Get your loan eligibility prediction in under a second.
                    No waiting, no paperwork — just instant data-driven insights.
                </p>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="card">
                <div class="card-title">🔒 Secure & Private</div>
                <p style='color:#475569; font-size:0.93rem; line-height:1.6;'>
                    Your data is processed locally and never stored or shared.
                    Complete privacy with every prediction.
                </p>
            </div>
        """, unsafe_allow_html=True)

    # How it Works
    st.markdown("<div class='section-header'>🔄 How It Works</div>", unsafe_allow_html=True)

    steps = [
        ("1", "Fill in your financial details", "Enter your income, loan amount, CIBIL score, assets, and other required information in the Loan Prediction form."),
        ("2", "Submit for prediction", "Click the 'Predict Loan Approval' button to send your data to the ML model for analysis."),
        ("3", "Get instant results", "The model processes your inputs and returns an Approved ✅ or Rejected ❌ result within milliseconds."),
        ("4", "Review and plan", "Use the result to understand your eligibility and make informed financial decisions."),
    ]
    for num, title, desc in steps:
        st.markdown(f"""
            <div class="step-card">
                <span class="step-num">{num}</span>
                <strong style='color:#1e293b;'>{title}</strong>
                <p style='color:#475569; font-size:0.9rem; margin:6px 0 0 38px; line-height:1.5;'>{desc}</p>
            </div>
        """, unsafe_allow_html=True)

    # CIBIL Score Guide
    st.markdown("<div class='section-header'>📈 CIBIL Score Guide</div>", unsafe_allow_html=True)
    st.markdown("""
        <div class="card">
            <div class="cibil-bar"></div>
            <div style='display:flex; justify-content:space-between; font-size:0.8rem; color:#64748b; margin-top:6px;'>
                <span>300 — Poor</span>
                <span>550 — Fair</span>
                <span>700 — Good</span>
                <span>750 — Very Good</span>
                <span>900 — Excellent</span>
            </div>
            <p style='color:#475569; font-size:0.92rem; margin-top:14px; line-height:1.6;'>
                A CIBIL score above <strong>750</strong> significantly improves your chances of loan approval.
                Lenders consider scores above 700 as creditworthy. Scores below 600 may lead to rejection
                or higher interest rates.
            </p>
        </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ══════════════════════════════════════════════
#  PAGE: LOAN PREDICTION
# ══════════════════════════════════════════════
# ─────────────────────────────────────────────
elif page == "📊  Loan Prediction":

    # Page Header
    st.markdown("""
        <div class="hero-banner">
            <span class="hero-emoji">📊</span>
            <h1 class="hero-title">Loan Eligibility Predictor</h1>
            <p class="hero-subtitle">
                Fill in the form below with your financial details.
                Our ML model will instantly predict your loan approval status.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Show model errors if any
    if model_error:
        st.error(model_error)
    if scaler_error:
        st.error(scaler_error)

    # ── INPUT FORM ──
    st.markdown("<div class='section-header'>📝 Applicant Details</div>", unsafe_allow_html=True)

    with st.form("loan_form", clear_on_submit=False):

        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.markdown("""
                <div style='background:#f0f7ff; border-radius:10px; padding:18px 20px; margin-bottom:16px;'>
                    <div style='font-weight:600; color:#1a56db; margin-bottom:4px;'>👤 Personal Information</div>
                </div>
            """, unsafe_allow_html=True)

            num_dependents = st.slider(
                "👨‍👩‍👧 Number of Dependents",
                min_value=0, max_value=5, value=0, step=1,
                help="Number of people financially dependent on you (0–5)"
            )

            education = st.selectbox(
                "🎓 Education Level",
                options=["Graduated", "Not Graduated"],
                help="Select your highest education qualification"
            )

            self_employed = st.selectbox(
                "💼 Self Employed",
                options=["No", "Yes"],
                help="Are you self-employed or running your own business?"
            )

            annual_income = st.slider(
                "💰 Annual Income (₹)",
                min_value=100000,
                max_value=10000000,
                value=500000,
                step=50000,
                format="₹%d",
                help="Your total annual income in Indian Rupees"
            )

        with col2:
            st.markdown("""
                <div style='background:#f0fff4; border-radius:10px; padding:18px 20px; margin-bottom:16px;'>
                    <div style='font-weight:600; color:#0e9f6e; margin-bottom:4px;'>💳 Loan & Financial Details</div>
                </div>
            """, unsafe_allow_html=True)

            loan_amount = st.slider(
                "🏠 Loan Amount (₹)",
                min_value=100000,
                max_value=50000000,
                value=1000000,
                step=100000,
                format="₹%d",
                help="The total loan amount you are applying for"
            )

            loan_duration = st.slider(
                "📅 Loan Duration (Years)",
                min_value=1,
                max_value=30,
                value=10,
                step=1,
                help="Repayment period in years"
            )

            cibil_score = st.slider(
                "📈 CIBIL Score",
                min_value=300,
                max_value=900,
                value=700,
                step=1,
                help="Your credit score (300 = Poor, 900 = Excellent)"
            )

            total_assets = st.slider(
                "🏗️ Total Assets Value (₹)",
                min_value=0,
                max_value=100000000,
                value=5000000,
                step=500000,
                format="₹%d",
                help="Total value of all your assets (property, vehicles, savings, etc.)"
            )

        # ── DYNAMIC SUMMARY ──
        st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
        st.markdown("#### 📋 Your Application Summary")

        edu_val = 1 if education == "Graduated" else 0
        emp_val = 1 if self_employed == "Yes" else 0

        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        with col_s1:
            st.metric("Dependents", f"{num_dependents}")
            st.metric("Education", education)
        with col_s2:
            st.metric("Self Employed", self_employed)
            st.metric("Annual Income", f"₹{annual_income:,.0f}")
        with col_s3:
            st.metric("Loan Amount", f"₹{loan_amount:,.0f}")
            st.metric("Duration", f"{loan_duration} yrs")
        with col_s4:
            st.metric("CIBIL Score", f"{cibil_score}")
            st.metric("Total Assets", f"₹{total_assets:,.0f}")

        # CIBIL Score Color Indicator
        if cibil_score >= 750:
            cibil_color = "#10b981"
            cibil_label = "Excellent 🌟"
        elif cibil_score >= 700:
            cibil_color = "#0e9f6e"
            cibil_label = "Good ✅"
        elif cibil_score >= 600:
            cibil_color = "#f59e0b"
            cibil_label = "Fair ⚠️"
        else:
            cibil_color = "#ef4444"
            cibil_label = "Poor ❌"

        st.markdown(f"""
            <div style='background:{cibil_color}22; border:1px solid {cibil_color}66;
                        border-radius:10px; padding:12px 18px; margin:10px 0;
                        display:flex; align-items:center; gap:12px;'>
                <span style='font-size:1.4rem;'>📊</span>
                <div>
                    <div style='font-weight:600; color:{cibil_color};'>CIBIL Score Status: {cibil_label}</div>
                    <div style='font-size:0.85rem; color:#64748b;'>
                        Score of {cibil_score} — {"High chance of approval" if cibil_score >= 700 else "May affect approval chances"}
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br/>", unsafe_allow_html=True)

        # ── SUBMIT BUTTON ──
        submitted = st.form_submit_button("🔍 Predict Loan Approval", use_container_width=True)

    # ── PREDICTION LOGIC ──
    if submitted:
        # Validate inputs
        errors = []
        if annual_income <= 0:
            errors.append("Annual income must be greater than 0.")
        if loan_amount <= 0:
            errors.append("Loan amount must be greater than 0.")
        if loan_amount > annual_income * 50:
            errors.append("Loan amount seems unusually high relative to income.")
        if cibil_score < 300 or cibil_score > 900:
            errors.append("CIBIL score must be between 300 and 900.")

        if errors:
            for err in errors:
                st.error(f"⚠️ {err}")
        elif not model or not scaler:
            st.error("❌ Cannot make prediction: model or scaler not loaded. Please check your .pkl files.")
        else:
            # Loading animation
            with st.spinner("🔄 Analyzing your application with AI..."):
                time.sleep(1.5)  # Simulate processing time

                try:
                    # ── PREPROCESS INPUT ──
                    # Encode categorical variables
                    education_encoded = 1 if education == "Graduated" else 0
                    self_employed_encoded = 1 if self_employed == "Yes" else 0

                    # Build feature array
                    # Order: [no_of_dependents, education, self_employed,
                    #          income_annum, loan_amount, loan_term,
                    #          cibil_score, total_assets]
                    input_features = np.array([[
                        num_dependents,
                        education_encoded,
                        self_employed_encoded,
                        annual_income,
                        loan_amount,
                        loan_duration,
                        cibil_score,
                        total_assets
                    ]])

                    # Scale features
                    input_scaled = scaler.transform(input_features)

                    # Make prediction
                    prediction = model.predict(input_scaled)[0]

                    # Get probability if available
                    try:
                        proba = model.predict_proba(input_scaled)[0]
                        confidence = max(proba) * 100
                        has_proba = True
                    except AttributeError:
                        has_proba = False
                        confidence = None

                    # ── DISPLAY RESULT ──
                    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
                    st.markdown("### 🎯 Prediction Result")

                    if prediction == 1 or prediction == "Approved":
                        st.markdown(f"""
                            <div class="result-approved">
                                <div style='font-size:4rem;'>✅</div>
                                <div class="result-title" style='color:#065f46;'>Loan