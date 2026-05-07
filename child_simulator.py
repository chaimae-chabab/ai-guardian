import streamlit as st
import time

st.set_page_config(
    page_title="AI Guardian - Téléphone Enfant",
    page_icon="📱",
    layout="centered"
)

st.title("📱 AI Guardian")
st.subheader("Protection automatique sur le téléphone de l'enfant")

st.markdown("---")

# Simulation d'arrivée de message
st.markdown("### 📩 Simulation d'arrivée d'un message")

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
    
    # Définition des messages simulés
    messages_exemples = {
        "suspect": "❌ Message reçu : 'Hey, tu es spécial(e). Ne dis rien à tes parents. Envoie-moi une photo.'",
        "manipulation": "⚠️ Message reçu : 'Si tu tenais vraiment à moi, tu ferais ce que je te demande. Tu es la seule personne qui me comprend.'",
        "normal": "✅ Message reçu : 'Salut, tu as fini les devoirs de maths ? On se voit au lycée demain ?'"
    }
    
    scores = {
        "suspect": {"score": 87, "niveau": "CRITIQUE", "categorie": "Grooming / Manipulation"},
        "manipulation": {"score": 54, "niveau": "MOYEN", "categorie": "Manipulation émotionnelle"},
        "normal": {"score": 12, "niveau": "FAIBLE", "categorie": "Aucune menace"}
    }
    
    with st.spinner("🤖 IA en cours d'analyse..."):
        time.sleep(1.5)
    
    st.markdown("---")
    
    # 1. CE QUE L'ENFANT REÇOIT (le vrai message)
    st.markdown("### 📱 Sur le téléphone de l'enfant")
    st.write(messages_exemples[st.session_state['type']])
    
    st.markdown("---")
    
    # 2. ANALYSE DE L'IA
    st.markdown("### 🤖 Analyse automatique de l'IA")
    
    score = scores[st.session_state['type']]["score"]
    niveau = scores[st.session_state['type']]["niveau"]
    categorie = scores[st.session_state['type']]["categorie"]
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Score de danger", f"{score}%")
    with col_b:
        st.metric("Niveau", niveau)
    
    st.info(f"**Catégorie :** {categorie}")
    
    st.markdown("---")
    
    # 3. CE QUE LE PARENT REÇOIT (PAS le message original)
    st.markdown("### 📲 Ce que le parent reçoit sur son téléphone")
    
    if score >= 70:
        st.error("🔴 **ALERTE ROUGE - DANGER ÉLEVÉ**")
        st.warning("Le parent voit : 'Niveau de danger : 87% - Catégorie : Grooming - Parlez calmement avec votre enfant'")
    elif score >= 40:
        st.warning("🟡 **ALERTE JAUNE - DANGER MOYEN**")
        st.info("Le parent voit : 'Niveau de danger : 54% - Catégorie : Manipulation - Surveillez les interactions'")
    else:
        st.success("✅ **AUCUNE ALERTE**")
        st.info("Le parent voit : 'Aucun danger détecté - Conversation normale'")
    
    # Message important pour le jury
    st.info("🔒 **Le parent ne voit PAS le message original** - Seul le niveau de danger est partagé")
    
    st.markdown("---")
    
    # Explication pour le jury
    with st.expander("ℹ️ Comment le parent reçoit l'alerte (dans un vrai produit)"):
        st.write("""
        **Dans la version réelle du produit :**
        
        1. **Notification push** : Le parent reçoit une alerte sur son téléphone (comme WhatsApp)
        2. **SMS automatique** : Un message texte est envoyé au parent
        3. **Email** : Un email d'alerte est envoyé
        4. **Dashboard sécurisé** : Le parent peut se connecter pour voir l'historique des alertes
        
        **Dans cette démonstration :**
        - Nous simulons ce que le parent verrait sur son téléphone
        - La technologie pour envoyer de vraies notifications existe (Firebase, Twilio, etc.)
        - Par manque de temps (10 jours), nous nous concentrons sur le cœur : l'IA et la protection de la vie privée
        """)
    
    if st.button("🔄 Nouvelle simulation", use_container_width=True):
        del st.session_state['type']
        st.rerun()

else:
    st.info("👆 Cliquez sur un bouton pour simuler l'arrivée d'un message")
    
    with st.expander("📖 Comment ça fonctionne (pour le jury)"):
        st.write("""
        **1. L'enfant reçoit un message** → L'application l'analyse automatiquement
        
        **2. L'IA détecte les dangers** → Grooming, manipulation, harcèlement
        
        **3. Le parent reçoit UNIQUEMENT l'alerte** → Pas le contenu du message
        
        **4. La vie privée est respectée** → L'enfant n'est pas espionné
        
        **5. Le parent peut agir** → Dialogue éducatif, pas punitif
        """)

st.markdown("---")
st.caption("🔒 **Protection sans espionnage** - L'IA protège, ne surveille pas")



