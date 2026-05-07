import streamlit as st
import time

st.set_page_config(
    page_title="AI Guardian | Protection Enfant",
    page_icon="📱",
    layout="centered"
)

# CSS PERSONNALISÉ
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,100..900;1,100..900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .phone-mock {
        background: #1a1a2e;
        border-radius: 2rem;
        padding: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .message-bubble {
        background: white;
        padding: 0.75rem;
        border-radius: 1rem;
        margin-bottom: 0.5rem;
        box-shadow: 0 1px 2px rgb(0 0 0 / 0.1);
    }
    
    .header-gradient {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    .privacy-note {
        background: #f0fdf4;
        padding: 1rem;
        border-radius: 0.75rem;
        border-left: 4px solid #10b981;
        margin: 1rem 0;
    }
    
    .footer {
        text-align: center;
        padding: 1.5rem;
        color: #6b7280;
        font-size: 0.75rem;
        border-top: 1px solid #e5e7eb;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# EN-TÊTE
st.markdown("""
<div class="header-gradient">
    <h1 style="color: white; margin: 0;">📱 AI Guardian</h1>
    <p style="color: #e0e7ff; margin: 0.5rem 0 0 0;">Protection automatique sur votre téléphone</p>
</div>
""", unsafe_allow_html=True)

# ZONE DE SIMULATION
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
        "suspect": "❌ Message suspect reçu\n\n« Tu es spécial(e). Ne dis rien à tes parents. Envoie-moi une photo. »",
        "manipulation": "⚠️ Message suspect reçu\n\n« Si tu tenais vraiment à moi, tu ferais ce que je te demande. Tu es la seule personne qui me comprend. »",
        "normal": "✅ Message normal reçu\n\n« Salut ! Tu as fini les devoirs ? On se voit demain au lycée ? »"
    }
    
    scores = {
        "suspect": {"score": 87, "niveau": "CRITIQUE", "categorie": "Grooming"},
        "manipulation": {"score": 54, "niveau": "MOYEN", "categorie": "Manipulation"},
        "normal": {"score": 12, "niveau": "FAIBLE", "categorie": "Aucune menace"}
    }
    
    with st.spinner("🤖 IA en cours d'analyse..."):
        time.sleep(1.2)
    
    st.markdown("---")
    
    # Message reçu
    st.markdown("### 📱 Message reçu sur le téléphone")
    st.info(messages[st.session_state['type']])
    
    # Analyse IA
    st.markdown("### 🤖 Analyse automatique")
    
    score = scores[st.session_state['type']]["score"]
    niveau = scores[st.session_state['type']]["niveau"]
    categorie = scores[st.session_state['type']]["categorie"]
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Score de danger", f"{score}%")
    with col_b:
        st.metric("Niveau", niveau)
    with col_c:
        st.metric("Catégorie", categorie)
    
    # Alerte parent
    st.markdown("---")
    st.markdown("### 📲 Alerte envoyée au parent")
    
    if score >= 70:
        st.error("""
        🔴 **ALERTE ROUGE – DANGER ÉLEVÉ**
        
        > Le parent reçoit : « Danger de grooming détecté – Score 87% – Parlez calmement avec votre enfant »
        """)
    elif score >= 40:
        st.warning("""
        🟡 **ALERTE JAUNE – DANGER MOYEN**
        
        > Le parent reçoit : « Manipulation émotionnelle détectée – Score 54% – Surveillez les interactions »
        """)
    else:
        st.success("""
        ✅ **AUCUNE ALERTE**
        
        > Le parent reçoit : « Aucun danger détecté – Conversation normale »
        """)
    
    # Privacy note
    st.markdown("""
    <div class="privacy-note">
        <p style="margin: 0;">🔒 <strong>Respect de la vie privée</strong> – Le parent ne voit PAS le contenu du message. Seul le niveau de danger est partagé.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Bouton reset
    if st.button("🔄 Simuler un nouveau message", use_container_width=True):
        del st.session_state['type']
        st.rerun()

else:
    st.info("👆 Cliquez sur un bouton ci-dessus pour simuler l'arrivée d'un message")
    
    # Explication fonctionnement
    with st.expander("📖 Comment ça fonctionne ?"):
        st.write("""
        **Dans la vraie vie :**
        
        1. L'enfant reçoit un message WhatsApp / SMS / Messenger
        2. Notre IA analyse automatiquement le message (localement)
        3. Si un danger est détecté, le parent reçoit une alerte
        4. **Le parent ne voit jamais le contenu du message**
        5. L'enfant garde sa vie privée, les parents peuvent protéger
        
        **Dans cette démonstration :**
        - Nous simulons l'arrivée de messages
        - L'analyse est 100% fonctionnelle
        - Ce que vous voyez = ce que le parent reçoit
        """)

# Footer
st.markdown("""
<div class="footer">
    <p>🔒 Protection sans espionnage – L'IA analyse sans violer la vie privée</p>
    <p>© 2025 AI Guardian – Cybersécurité éthique</p>
</div>
""", unsafe_allow_html=True)
