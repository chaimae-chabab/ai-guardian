import streamlit as st
import pandas as pd
import plotly.express as px
import re

# Configuration de la page
st.set_page_config(
    page_title="AI Guardian",
    page_icon="🛡️",
    layout="wide"
)

# Titre principal
st.title("🛡️ AI Guardian")
st.subheader("Protecting children without spying")

# === LISTE DES MOTS DANGEREUX À DÉTECTER ===
GROOMING_KEYWORDS = [
    "don't tell anyone", "keep it secret", "just between us",
    "don't tell your parents", "they won't understand",
    "you're special", "only you", "trust me", "our secret",
    "between you and me", "secret", "don't tell", "hide this",
    "don't share", "private message", "just us", "secret chat",
    "your parents don't understand", "they don't get you"
]

MANIPULATION_KEYWORDS = [
    "if you love me", "if you really care", "you owe me",
    "after everything i did", "you're the only one",
    "don't abandon me", "prove your love", "prove you care",
    "you would if you loved me", "you're making me sad",
    "you're hurting me", "after all i've done", "i sacrificed"
]

BULLYING_KEYWORDS = [
    "stupid", "useless", "nobody likes you", "hate you",
    "kill yourself", "worthless", "ugly", "fat", "loser",
    "idiot", "moron", "dumb", "pathetic", "disappointment",
    "everyone hates you", "you're a joke", "give up"
]

TOXICITY_KEYWORDS = [
    "shut up", "bastard", "damn", "hell", "crap",
    "screw you", "what's wrong with you", "are you stupid"
]

NEGATIVE_WORDS = [
    "hate", "terrible", "awful", "horrible", "sad", "depressed",
    "lonely", "hopeless", "scared", "anxious", "hurt", "pain"
]

def analyze_conversation(text):
    """Analyse le texte et retourne des scores de danger"""
    
    text_lower = text.lower()
    
    # Compter les mots dangereux
    grooming_count = 0
    for word in GROOMING_KEYWORDS:
        grooming_count += text_lower.count(word)
    
    manipulation_count = 0
    for word in MANIPULATION_KEYWORDS:
        manipulation_count += text_lower.count(word)
    
    bullying_count = 0
    for word in BULLYING_KEYWORDS:
        bullying_count += text_lower.count(word)
    
    toxicity_count = 0
    for word in TOXICITY_KEYWORDS:
        toxicity_count += text_lower.count(word)
    
    negative_count = 0
    for word in NEGATIVE_WORDS:
        negative_count += text_lower.count(word)
    
    # NOUVEAU : Calcul plus sensible (max 5 mots = 100%)
    max_score = 5  # Changé de 15 à 5
    
    grooming_score = min(100, (grooming_count / max_score) * 100)
    manipulation_score = min(100, (manipulation_count / max_score) * 100)
    bullying_score = min(100, (bullying_count / max_score) * 100)
    toxicity_score = min(100, (toxicity_count / max_score) * 100)
    
    # Bonus : si plusieurs catégories, augmenter le score
    total_detections = (grooming_count > 0) + (manipulation_count > 0) + (bullying_count > 0) + (toxicity_count > 0)
    if total_detections >= 2:
        grooming_score = min(100, grooming_score + 15)
        manipulation_score = min(100, manipulation_score + 15)
    
    # Score de négativité
    negativity_score = min(100, (negative_count / max_score) * 100)
    
    return {
        "Grooming": round(grooming_score, 1),
        "Emotional Manipulation": round(manipulation_score, 1),
        "Cyberbullying": round(bullying_score, 1),
        "Toxicity": round(toxicity_score, 1),
        "Negativity": round(negativity_score, 1)
    }
# Upload fichier
st.markdown("### 📂 Upload a conversation")
uploaded_file = st.file_uploader("Choose a .txt file", type=["txt"])

if uploaded_file is not None:
    conversation = uploaded_file.read().decode("utf-8")
    
    with st.expander("Preview (hidden from parents in real version)"):
        st.text(conversation[:500] + ("..." if len(conversation) > 500 else ""))
    
    st.success(f"✅ Conversation loaded successfully! ({len(conversation)} characters)")
    
    # === ANALYSE IA RÉELLE ===
    scores = analyze_conversation(conversation)
    
    # Score global (moyenne des 4 premiers scores)
    global_score = (scores["Grooming"] + scores["Emotional Manipulation"] + 
                    scores["Cyberbullying"] + scores["Toxicity"]) / 4
    
    # === DASHBOARD ===
    st.markdown("---")
    st.markdown("## 📊 Risk Analysis Dashboard")
    
    # Affichage du score global
    col1, col2, col3 = st.columns(3)
    with col1:
        if global_score < 30:
            st.metric("🟢 Global Risk Score", f"{global_score:.0f}%", delta="Safe")
        elif global_score < 55:
            st.metric("🟡 Global Risk Score", f"{global_score:.0f}%", delta="Medium Risk")
        else:
            st.metric("🔴 Global Risk Score", f"{global_score:.0f}%", delta="High Risk")
    
    with col2:
        if global_score < 30:
            threat_level = "LOW"
        elif global_score < 55:
            threat_level = "MEDIUM"
        else:
            threat_level = "HIGH"
    
    with col3:
        high_threats = sum(1 for k in ["Grooming", "Emotional Manipulation", "Cyberbullying", "Toxicity"] 
                          if scores.get(k, 0) > 50)
        st.metric("📊 Threats Detected", high_threats)
    
    # Graphique des menaces
    st.markdown("### 🔍 Threats Breakdown")
    
    df = pd.DataFrame({
        "Threat Type": ["Grooming", "Emotional Manipulation", "Cyberbullying", "Toxicity"],
        "Risk Score (%)": [scores["Grooming"], scores["Emotional Manipulation"], 
                          scores["Cyberbullying"], scores["Toxicity"]]
    })
    
    fig = px.bar(df, x="Threat Type", y="Risk Score (%)", 
                 color="Risk Score (%)",
                 color_continuous_scale=["green", "yellow", "red"],
                 title="Risk Scores by Category",
                 range_y=[0, 100])
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Alertes spécifiques
    st.markdown("### ⚠️ Alerts")
    
    alert_count = 0
    
    if scores["Grooming"] > 70:
        st.error("🔴 **HIGH GROOMING RISK** - Suspicious secrecy/manipulation patterns detected")
        alert_count += 1
    elif scores["Grooming"] > 40:
        st.warning("🟡 **Medium Grooming Risk** - Monitor conversation for secrecy language")
        alert_count += 1
    
    if scores["Emotional Manipulation"] > 70:
        st.error("🔴 **Emotional manipulation detected** - Guilt-inducing or pressure language")
        alert_count += 1
    elif scores["Emotional Manipulation"] > 40:
        st.warning("🟡 Suspicious emotional language detected")
        alert_count += 1
    
    if scores["Cyberbullying"] > 70:
        st.error("🔴 **Cyberbullying detected** - Aggressive or humiliating language")
        alert_count += 1
    elif scores["Cyberbullying"] > 40:
        st.warning("🟡 Potential harassment patterns detected")
        alert_count += 1
    
    if scores["Toxicity"] > 70:
        st.error("🔴 **High toxicity level** - Abusive language present")
        alert_count += 1
    elif scores["Toxicity"] > 40:
        st.warning("🟡 Moderate toxicity detected")
        alert_count += 1
    
    if scores["Negativity"] > 60:
        st.info("📉 **Very negative tone detected** - Conversation shows distress or sadness indicators")
    
    if alert_count == 0 and global_score < 30:
        st.success("✅ **No significant threats detected** - Conversation appears safe")
    
    # Privacy mode
    st.markdown("---")
    st.success("🔒 **Privacy Mode Enabled** - Parents see only alerts, not conversation content")
    
    # Conseils pour les parents
    with st.expander("💡 Parental Guidance & Recommendations"):
        st.write("**Based on AI analysis, here are recommendations:**")
        if global_score > 60:
            st.write("⚠️ **Urgent:** Have a calm, non-judgmental conversation with your child")
            st.write("🔍 Ask open-ended questions about their online friendships")
            st.write("🛡️ Reinforce that they can tell you anything without punishment")
            st.write("📞 Consider speaking with a school counselor if needed")
        elif global_score > 30:
            st.write("👂 **Proactive:** Listen actively to your child's online experiences")
            st.write("💬 Encourage open communication without fear")
            st.write("📚 Use this as an opportunity to discuss online safety")
        else:
            st.write("✅ **Maintain trust:** Continue having regular conversations about online safety")
            st.write("🎯 Reinforce positive online behavior and boundaries")
    
    # Statistiques détaillées
    with st.expander("📊 Detailed Analysis Statistics"):
        st.write(f"**Conversation length:** {len(conversation)} characters")
        st.write(f"**Words analyzed:** Approximately {len(conversation.split())}")
        st.write(f"**Negative sentiment score:** {scores['Negativity']:.0f}%")
        st.write("---")
        st.write("**Detection keywords found:**")
        st.write(f"- Grooming-related terms: {int(scores['Grooming'] / 100 * 15)} occurrences")
        st.write(f"- Manipulation-related terms: {int(scores['Emotional Manipulation'] / 100 * 15)} occurrences")
        st.write(f"- Bullying-related terms: {int(scores['Cyberbullying'] / 100 * 15)} occurrences")

else:
    st.info("📁 Please upload a conversation file (.txt)")