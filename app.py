import streamlit as st
import pandas as pd
import plotly.express as px
import time
from datetime import datetime

st.set_page_config(
    page_title="AI Guardian | Parent Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS MODERNE AVEC ANIMATIONS
st.markdown("""
<style>
    /* Police moderne */
    @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,100..900;1,100..900&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Animation fade in */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Hero section avec dégradé animé */
    .hero {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% 200%;
        animation: gradient 3s ease infinite;
        padding: 2.5rem;
        border-radius: 1.5rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 20px 35px -10px rgba(0,0,0,0.2);
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Cartes modernes */
    .card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        transition: all 0.3s ease;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 25px -12px rgb(0 0 0 / 0.2);
    }
    
    /* Badge privacy */
    .privacy-badge {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 2rem;
        font-size: 0.875rem;
        font-weight: 600;
        text-align: center;
        display: inline-block;
        box-shadow: 0 4px 10px rgba(16,185,129,0.3);
    }
    
    /* Score card */
    .score-card {
        background: white;
        border-radius: 1rem;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-radius: 1rem;
        margin-top: 2rem;
        color: #94a3b8;
    }
    
    /* Upload zone stylisée */
    .upload-zone {
        border: 2px dashed #c7d2fe;
        border-radius: 1rem;
        padding: 2rem;
        text-align: center;
        background: #f8fafc;
        transition: all 0.3s ease;
    }
    
    .upload-zone:hover {
        border-color: #667eea;
        background: #eff6ff;
    }
</style>
""", unsafe_allow_html=True)

# HERO SECTION
st.markdown("""
<div class="hero fade-in">
    <h1 style="color: white; margin: 0; font-size: 3rem;">🛡️ AI Guardian</h1>
    <p style="color: #f1f5f9; margin: 0.5rem 0 0 0; font-size: 1.2rem;">Protection des enfants sans espionnage</p>
    <p style="color: #c7d2fe; margin: 1rem 0 0 0; font-size: 0.9rem;">🤖 IA éthique · 🔒 Respect de la vie privée · ⚡ Alertes en temps réel</p>
</div>
""", unsafe_allow_html=True)

# UPLOAD ZONE
st.markdown('<div class="fade-in">', unsafe_allow_html=True)
st.markdown("### 📂 Importer une conversation")

with st.container():
    uploaded_file = st.file_uploader(
        "Téléchargez un fichier .txt",
        type=["txt"],
        help="Exportez une conversation depuis WhatsApp, Messenger ou Discord"
    )
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    conversation = uploaded_file.read().decode("utf-8")
    
    with st.expander("🔒 Aperçu (masqué aux parents en version réelle)"):
        st.text(conversation[:500])
    
    st.success(f"✅ Conversation chargée – {len(conversation)} caractères analysés")
    
    with st.spinner("🤖 IA en cours d'analyse..."):
        time.sleep(1.5)
    
    # Mots clés
    GROOMING_KEYWORDS = [
        "don't tell anyone", "keep it secret", "just between us",
        "don't tell your parents", "they won't understand",
        "you're special", "only you", "trust me", "our secret"
    ]
    MANIPULATION_KEYWORDS = [
        "if you love me", "if you really care", "you owe me",
        "you're the only one", "don't abandon me", "prove your love"
    ]
    BULLYING_KEYWORDS = [
        "stupid", "useless", "nobody likes you", "hate you",
        "kill yourself", "worthless", "ugly", "loser"
    ]
    TOXICITY_KEYWORDS = ["shut up", "idiot", "moron", "bastard", "damn"]
    
    text_lower = conversation.lower()
    grooming_count = sum(1 for w in GROOMING_KEYWORDS if w in text_lower)
    manipulation_count = sum(1 for w in MANIPULATION_KEYWORDS if w in text_lower)
    bullying_count = sum(1 for w in BULLYING_KEYWORDS if w in text_lower)
    toxicity_count = sum(1 for w in TOXICITY_KEYWORDS if w in text_lower)
    
    max_score = 5
    grooming_score = min(100, (grooming_count / max_score) * 100)
    manipulation_score = min(100, (manipulation_count / max_score) * 100)
    bullying_score = min(100, (bullying_count / max_score) * 100)
    toxicity_score = min(100, (toxicity_count / max_score) * 100)
    
    global_score = (grooming_score + manipulation_score + bullying_score + toxicity_score) / 4
    
    # DASHBOARD
    st.markdown("---")
    st.markdown('<h2 style="text-align: center;">📊 Tableau de bord des risques</h2>', unsafe_allow_html=True)
    
    # SCORE CARD
    col1, col2, col3, col4 = st.columns(4)
    
    if global_score < 30:
        with col1:
            st.markdown(f"""
            <div class="score-card" style="border-bottom: 4px solid #10b981;">
                <h3 style="color: #64748b;">Score global</h3>
                <h1 style="font-size: 3.5rem; margin: 0; color: #10b981;">{global_score:.0f}%</h1>
                <p style="color: #10b981;">🟢 Niveau bas</p>
            </div>
            """, unsafe_allow_html=True)
    elif global_score < 60:
        with col1:
            st.markdown(f"""
            <div class="score-card" style="border-bottom: 4px solid #f59e0b;">
                <h3 style="color: #64748b;">Score global</h3>
                <h1 style="font-size: 3.5rem; margin: 0; color: #f59e0b;">{global_score:.0f}%</h1>
                <p style="color: #f59e0b;">🟡 Niveau moyen</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        with col1:
            st.markdown(f"""
            <div class="score-card" style="border-bottom: 4px solid #ef4444;">
                <h3 style="color: #64748b;">Score global</h3>
                <h1 style="font-size: 3.5rem; margin: 0; color: #ef4444;">{global_score:.0f}%</h1>
                <p style="color: #ef4444;">🔴 Niveau élevé</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="score-card">
            <h3 style="color: #64748b;">Grooming</h3>
            <h1 style="font-size: 2.5rem; margin: 0;">{grooming_score:.0f}%</h1>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="score-card">
            <h3 style="color: #64748b;">Manipulation</h3>
            <h1 style="font-size: 2.5rem; margin: 0;">{manipulation_score:.0f}%</h1>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="score-card">
            <h3 style="color: #64748b;">Cyberharcèlement</h3>
            <h1 style="font-size: 2.5rem; margin: 0;">{bullying_score:.0f}%</h1>
        </div>
        """, unsafe_allow_html=True)
    
    # GRAPHIQUE
    df = pd.DataFrame({
        "Type de menace": ["Grooming", "Manipulation", "Cyberharcèlement", "Toxicité"],
        "Score (%)": [grooming_score, manipulation_score, bullying_score, toxicity_score]
    })
    
    fig = px.bar(df, x="Type de menace", y="Score (%)", 
                 color="Score (%)",
                 color_continuous_scale=["#10b981", "#f59e0b", "#ef4444"],
                 title="Analyse par catégorie")
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", font_family="Inter", height=450)
    st.plotly_chart(fig, use_container_width=True)
    
    # ALERTES
    st.markdown("## ⚠️ Alertes détectées")
    alert_count = 0
    if grooming_score > 50:
        st.error("🔴 **Grooming élevé** – Tentative d'isolement ou de manipulation détectée")
        alert_count += 1
    if manipulation_score > 50:
        st.warning("🟡 **Manipulation émotionnelle** – Langage de culpabilisation détecté")
        alert_count += 1
    if bullying_score > 50:
        st.warning("🟡 **Cyberharcèlement** – Langage agressif détecté")
        alert_count += 1
    if alert_count == 0:
        st.success("✅ **Aucune menace significative** – La conversation semble sûre")
    
    # PRIVACY BADGE
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <div class="privacy-badge">
            🔒 Mode vie privée – Les parents ne voient pas le contenu des messages
        </div>
    </div>
    """, unsafe_allow_html=True)

# FOOTER
st.markdown("""
<div class="footer fade-in">
    <p style="margin: 0;">🔒 Protection sans espionnage – L'IA analyse localement, la vie privée est respectée</p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem;">© 2025 AI Guardian – Projet de cybersécurité éthique</p>
</div>
""", unsafe_allow_html=True)
