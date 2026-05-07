import streamlit as st
import time

st.set_page_config(
    page_title="AI Guardian - Enfant",
    page_icon="📱",
    layout="centered"
)

st.title("📱 AI Guardian")
st.subheader("Téléphone de l'enfant - Protection automatique")

st.markdown("---")

st.markdown("### Simulation de réception de message")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔴 Message suspect"):
        st.session_state['message'] = "danger"

with col2:
    if st.button("🟡 Manipulation"):
        st.session_state['message'] = "manipulation"

with col3:
    if st.button("🟢 Message normal"):
        st.session_state['message'] = "normal"

if 'message' in st.session_state:
    with st.spinner("Analyse en cours..."):
        time.sleep(1)
    
    if st.session_state['message'] == "danger":
        st.error("🔴 DANGER ÉLEVÉ - Score 87%")
    elif st.session_state['message'] == "manipulation":
        st.warning("🟡 DANGER MOYEN - Score 54%")
    else:
        st.success("🟢 AUCUN DANGER - Score 12%")
    
    if st.button("Nouveau message"):
        del st.session_state['message']
        st.rerun()