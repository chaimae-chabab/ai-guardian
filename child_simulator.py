import streamlit as st
import time

st.set_page_config(
    page_title="AI Guardian | Protection Enfant",
    page_icon="📱",
    layout="centered"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,100..900;1,100..900&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .slide-in { animation: slideIn 0.5s ease-out; }
    
    .phone-header {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 1.5rem;
        border-radius: 1.5rem 1.5rem 0 0;
        text-align: center;
    }
    
    .message-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 1rem;
        border-radius: 1rem;
        margin-bottom: 0.5rem;
        border-left: 4px solid;
        box-shadow: 0 1px 3px rgb(0 0 0 / 0.1);
    }
    
    .alert-card {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        padding: 1rem;
        border-radius: 1rem;
        border-left: 4px solid #ef4444;
    }
    
    .success-card {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        padding: 1rem;
        border-radius: 1rem;
        border-left: 4px solid #10b981;
    }
    
    .warning-card {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        padding: 1rem;
        border-radius: 1rem;
        border-left: 4px solid #f59e0b;
    }
    
    .footer {
        background: #1e293b;
        padding: 1rem;
        border-radius: 0 0 1rem 1rem;
        text-align: center;
        color: #94a3b8;
        font-size: 0.7rem;
    }
    
    .button-glow {
        transition: all 0.3s ease;
    }
    .button-glow:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px -5px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div class="phone-header">
    <h1 style="color: white; margin: 0; font-size: 1.5rem;">📱 AI Guardian</h1>
    <p style="color: #94a3b8; margin: 0.25rem 0 0 0; font-size: 0.8rem;">Protection automatique en arrière-plan</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📩 Simulation d'arrivée de messages")
st.caption("L'application analyse automatiquement chaque message reçu")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔴 Message suspect", use_container_width=True):
        st.session_state['type'] = "suspect"

with col2:
    if st.button("🟡 Manipulation", use_container_width=True):
        st.session_state['type'] = "manipulation"

with col3:
    if st.button("🟢 Message normal", use_container_width=True):
        st.session_state['type'] = "normal"

if 'type' in st.session_state:
    
    messages = {
        "suspect": "« Tu es spécial(e). Ne dis rien à tes parents. Envoie-moi une photo. »",
        "manipulation": "« Si tu tenais vraiment à moi, tu ferais ce que je te demande. Tu es la seule personne qui me comprend. »",
        "normal": "« Salut ! Tu as fini les devoirs ? On se voit demain au lycée ? »"
    }
    
    scores = {
        "suspect": {"score": 87, "niveau": "CRITIQUE", "categorie": "Grooming", "color": "#ef4444"},
        "manipulation": {"score": 54, "niveau": "MOYEN", "categorie": "Manipulation", "color": "#f59e0b"},
        "normal": {"score": 12, "niveau": "FAIBLE", "categorie": "Aucune menace", "color": "#10b981"}
    }
    
    with st.spinner("🤖 IA en cours d'analyse..."):
        time.sleep(1.2)
    
    st.markdown('<div class="slide-in">', unsafe_allow_html=True)
    
    # Message reçu
    st.markdown("**📱 Message reçu :**")
    st.markdown(f'<div class="message-card" style="border-left-color: {scores[st.session_state["type"]]["color"]};">{messages[st.session_state["type"]]}</div>', unsafe_allow_html=True)
    
    # Analyse
    st.markdown("**🤖 Analyse automatique :**")
    score = scores[st.session_state['type']]["score"]
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Score", f"{score}%")
    with col_b:
        st.metric("Niveau", scores[st.session_state['type']]["niveau"])
    with col_c:
        st.metric("Catégorie", scores[st.session_state['type']]["categorie"])
    
    # Alerte parent
    st.markdown("**📲 Alerte envoyée au parent :**")
    if score >= 70:
        st.markdown(f'''
        <div class="alert-card">
            🔴 <strong>ALERTE ROUGE – DANGER ÉLEVÉ</strong><br>
            <span style="font-size: 0.9rem;">Le parent reçoit : « Danger de grooming détecté – Score {score}% – Parlez calmement avec votre enfant »</span>
        </div>
        ''', unsafe_allow_html=True)
    elif score >= 40:
        st.markdown(f'''
        <div class="warning-card">
            🟡 <strong>ALERTE JAUNE – DANGER MOYEN</strong><br>
            <span style="font-size: 0.9rem;">Le parent reçoit : « Manipulation émotionnelle détectée – Score {score}% – Surveillez les interactions »</span>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div class="success-card">
            ✅ <strong>AUCUNE ALERTE</strong><br>
            <span style="font-size: 0.9rem;">Le parent reçoit : « Aucun danger détecté – Conversation normale »</span>
        </div>
        ''', unsafe_allow_html=True)
    
    # Privacy note
    st.info("🔒 **Le parent ne voit PAS le contenu du message** – Seul le niveau de danger est partagé")
    
    if st.button("🔄 Simuler un nouveau message", use_container_width=True):
        del st.session_state['type']
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("👆 Cliquez sur un bouton ci-dessus pour simuler l'arrivée d'un message")

# FOOTER
st.markdown("""
<div class="footer">
    🔒 Protection sans espionnage – L'IA analyse sans violer la vie privée
</div>
""", unsafe_allow_html=True)
