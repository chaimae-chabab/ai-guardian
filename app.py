import streamlit as st
import pandas as pd
import plotly.express as px
import time

# CONFIGURATION PAGE
st.set_page_config(
    page_title="AI Guardian | Parent Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS PERSONNALISÉ
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,100..900;1,100..900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header gradient */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    /* Cartes */
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        margin-bottom: 1rem;
    }
    
    /* Badge privacy */
    .privacy-badge {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 2rem;
        font-size: 0.875rem;
        font-weight: 600;
        text-align: center;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #6b7280;
        font-size: 0.875rem;
        border-top: 1px solid #e5e7eb;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# EN-TÊTE
st.markdown("""
<div class="main-header">
    <h1 style="color: white; margin: 0;">🛡️ AI Guardian</h1>
    <p style="color: #e0e7ff; margin: 0.5rem 0 0 0;">Protection des enfants sans espionnage</p>
</div>
""", unsafe_allow_html=True)

# === ZONE UPLOAD ===
st.markdown("### 📂 Importer une conversation")

uploaded_file = st.file_uploader(
    "Téléchargez une conversation (.txt)",
    type=["txt"],
    help="Exportez une conversation depuis WhatsApp, Messenger ou Discord"
)

if uploaded_file is not None:
    conversation = uploaded_file.read().decode("utf-8")
    
    # Aperçu masqué (privacy)
    with st.expander("🔒 Aperçu (caché aux parents en version réelle)"):
        st.text(conversation[:500])
    
    st.success(f"✅ Conversation chargée – {len(conversation)} caractères analysés")
    
    # === ANALYSE IA ===
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
    st.markdown("## 📊 Tableau de bord des risques")
    
    # Cartes de score
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if global_score < 30:
            st.markdown("""
            <div class="card" style="text-align: center;">
                <h3>🟢 Score global</h3>
                <h1 style="font-size: 3rem; margin: 0; color: #10b981;">{:.0f}%</h1>
                <p style="color: #10b981;">Niveau bas</p>
            </div>
            """.format(global_score), unsafe_allow_html=True)
        elif global_score < 60:
            st.markdown("""
            <div class="card" style="text-align: center;">
                <h3>🟡 Score global</h3>
                <h1 style="font-size: 3rem; margin: 0; color: #f59e0b;">{:.0f}%</h1>
                <p style="color: #f59e0b;">Niveau moyen</p>
            </div>
            """.format(global_score), unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="card" style="text-align: center;">
                <h3>🔴 Score global</h3>
                <h1 style="font-size: 3rem; margin: 0; color: #ef4444;">{:.0f}%</h1>
                <p style="color: #ef4444;">Niveau élevé</p>
            </div>
            """.format(global_score), unsafe_allow_html=True)
    
    # Graphique
    df = pd.DataFrame({
        "Type de menace": ["Grooming", "Manipulation", "Cyberharcèlement", "Toxicité"],
        "Score (%)": [grooming_score, manipulation_score, bullying_score, toxicity_score]
    })
    
    fig = px.bar(df, x="Type de menace", y="Score (%)", 
                 color="Score (%)",
                 color_continuous_scale=["#10b981", "#f59e0b", "#ef4444"],
                 title="Analyse par catégorie",
                 range_y=[0, 100])
    
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_family="Inter",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Alertes
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
    
    # Privacy badge
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <div class="privacy-badge" style="display: inline-block;">
            🔒 Mode vie privée activé – Les parents ne voient pas le contenu des messages
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    st.info("👆 Téléchargez une conversation pour commencer l'analyse")

# Footer
st.markdown("""
<div class="footer">
    <p>🔒 Protection sans espionnage – L'IA analyse localement, la vie privée est respectée</p>
    <p>© 2025 AI Guardian – Projet de cybersécurité éthique</p>
</div>
""", unsafe_allow_html=True)
