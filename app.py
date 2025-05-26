# streamlit_app.py
import time
import requests
import phonenumbers
import pandas as pd
import streamlit as st
import json
import os
from datetime import datetime
import re

# --- Configuration initiale ---
USERS_FILE = "users.json"

# Configuration de la page
st.set_page_config(
    page_title="Validation de numéros FR",
    page_icon="📞",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    else:
        default_users = {
            "youness": {"password": "admin123", "role": "admin"},
            "imad": {"password": "imad123", "role": "user"},
            "driss": {"password": "driss123", "role": "user"}
        }
        save_users(default_users)
        return default_users

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'users' not in st.session_state:
    st.session_state.users = load_users()

# --- Fonctions d'authentification ---
def login(username, password):
    if username in st.session_state.users and st.session_state.users[username]["password"] == password:
        st.session_state.authenticated = True
        st.session_state.current_user = username
        return True
    return False

def logout():
    st.session_state.authenticated = False
    st.session_state.current_user = None

def is_admin():
    return st.session_state.current_user and st.session_state.users[st.session_state.current_user]["role"] == "admin"

# --- Interface de connexion ---
if not st.session_state.authenticated:
    st.title("🔐 Connexion Sécurisée")
    st.subheader("Accédez à votre plateforme de validation de numéros")
    
    # Présentation de la solution
    st.info("📱 Validation de Numéros Français\n\nUne solution professionnelle et sécurisée pour valider vos numéros de téléphone français avec une précision maximale.")
    
    # Fonctionnalités principales
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("🔍 Validation en temps réel\n\nVérification instantanée et précise de la validité des numéros avec notre API avancée")
    with col2:
        st.info("📊 Analyse détaillée\n\nInformations complètes sur l'opérateur, le type de ligne et le formatage international")
    with col3:
        st.info("📥 Export professionnel\n\nExportation des résultats en format CSV avec horodatage et traçabilité complète")
    
    # Formulaire de connexion
    with st.form("login_form"):
        username = st.text_input("👤 Nom d'utilisateur", placeholder="Entrez votre nom d'utilisateur")
        password = st.text_input("🔑 Mot de passe", type="password", placeholder="Entrez votre mot de passe")
        submit = st.form_submit_button("🔓 Se connecter", use_container_width=True)
        
        if submit:
            if login(username, password):
                st.success(f"🎉 Bienvenue {username}! Redirection en cours...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Identifiants incorrects. Veuillez réessayer.")
    
    # Pied de page
    st.markdown("---")
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown("🚀 Développé par DATAY | Solution professionnelle de validation de numéros")
    st.markdown("Designé par A.Rochdi 🚛")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- Interface principale ---
# Header
st.title("📞 Validation de Numéros Français")
st.caption("Plateforme professionnelle de validation")

# Sidebar
with st.sidebar:
    st.title("🎛️ Panneau de contrôle")
    if st.button("🚪 Déconnexion", use_container_width=True):
        logout()
        st.rerun()
    
    # Interface admin
    if is_admin():
        st.markdown("---")
        st.subheader("👑 Administration")
        
        if st.button("⚙️ Gérer les utilisateurs", use_container_width=True):
            st.session_state.show_user_management = not st.session_state.get('show_user_management', False)
        
        if st.session_state.get('show_user_management', False):
            st.markdown("---")
            st.subheader("👥 Gestion des utilisateurs")
            
            with st.form("add_user_form"):
                st.markdown("**➕ Ajouter un utilisateur**")
                new_username = st.text_input("Nom d'utilisateur")
                new_password = st.text_input("Mot de passe", type="password")
                new_role = st.selectbox("Rôle", ["user", "admin"])
                submit = st.form_submit_button("✅ Ajouter", use_container_width=True)
                
                if submit:
                    if new_username and new_password:
                        if new_username not in st.session_state.users:
                            st.session_state.users[new_username] = {
                                "password": new_password,
                                "role": new_role
                            }
                            save_users(st.session_state.users)
                            st.success(f"✅ Utilisateur {new_username} ajouté!")
                            st.rerun()
                        else:
                            st.error("❌ Cet utilisateur existe déjà")
                    else:
                        st.error("❌ Veuillez remplir tous les champs")
            
            # Liste des utilisateurs
            st.markdown("**👥 Utilisateurs existants**")
            for user in st.session_state.users:
                col1, col2 = st.columns([3, 1])
                role_badge = "admin" if st.session_state.users[user]["role"] == "admin" else "user"
                col1.markdown(f"**{user}** ({role_badge})")
                if col2.button("🗑️", key=f"del_{user}", help=f"Supprimer {user}"):
                    if user != st.session_state.current_user:
                        del st.session_state.users[user]
                        save_users(st.session_state.users)
                        st.success(f"✅ Utilisateur {user} supprimé!")
                        st.rerun()
                    else:
                        st.error("❌ Vous ne pouvez pas vous supprimer")

# --- Fonctions de normalisation ---
def clean_phone_number(raw: str) -> str:
    cleaned = re.sub(r'[^\d+]', '', raw)
    return cleaned

def normalize_number(raw: str) -> str:
    raw = clean_phone_number(raw)
    
    if raw.startswith("00"):
        raw = "+" + raw[2:]
    elif raw.startswith("0"):
        raw = "+33" + raw[1:]
    elif not raw.startswith("+"):
        raw = "+33" + raw
    
    try:
        num = phonenumbers.parse(raw, None)
        if phonenumbers.is_valid_number(num):
            return phonenumbers.format_number(
                num, phonenumbers.PhoneNumberFormat.E164
            )
    except phonenumbers.NumberParseException:
        pass
    return raw

# --- Interface de validation ---
st.info("""
📝 Guide d'utilisation

Collez vos numéros de téléphone dans le champ ci-dessous (un numéro par ligne). Notre système supporte tous les formats français courants :

- Format international : +33612345678
- Format national : 0612345678
- Format avec espaces : +33 6 12 34 56 78
- Format 00 : 0033612345678
- Sans préfixe : 612345678
""")

st.subheader("📋 Saisie des numéros")
numbers_text = st.text_area(
    "Collez vos numéros ici",
    placeholder="Exemple:\n+33612345678\n0612345678\n06 12 34 56 78\n0033612345678\n612345678",
    height=200,
    help="Un numéro par ligne. Tous les formats français sont acceptés."
)

if st.button("🔍 Lancer la validation", use_container_width=True):
    raws = [line.strip() for line in numbers_text.splitlines() if line.strip()]
    if not raws:
        st.error("❌ Veuillez saisir au moins un numéro à valider.")
    else:
        def call_abstract(phone: str) -> dict:
            url = "https://phonevalidation.abstractapi.com/v1/"
            params = {
                "api_key": "672787ca530e447c9887fd88d7ba1573",
                "phone": phone,
                "country": "FR"
            }
            try:
                r = requests.get(url, params=params, timeout=10)
                r.raise_for_status()
                return r.json()
            except requests.exceptions.RequestException as e:
                return {"error": str(e)}

        st.info("⚡ Traitement en cours\n\nValidation des numéros via notre API professionnelle...")
        
        results = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        total = len(raws)
        
        stats_container = st.empty()

        for i, raw in enumerate(raws, start=1):
            status_text.info(f"📊 Progression: {i}/{total}\nTraitement du numéro: {raw}")
            
            e164 = normalize_number(raw)
            try:
                data = call_abstract(e164)
                if "error" not in data:
                    results.append({
                        "🔢 Numéro original": raw,
                        "📱 Numéro normalisé": data.get("phone", e164),
                        "✅ Statut": data.get("valid", False),
                        "🌍 Format international": data.get("format", {}).get("international", ""),
                        "🏠 Format local": data.get("format", {}).get("local", ""),
                        "🏳️ Code pays": data.get("country", {}).get("code", ""),
                        "📞 Type de ligne": data.get("type", ""),
                        "📡 Opérateur": data.get("carrier", ""),
                        "👤 Validé par": st.session_state.current_user,
                        "⏰ Date de validation": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                else:
                    results.append({
                        "🔢 Numéro original": raw,
                        "📱 Numéro normalisé": e164,
                        "✅ Statut": False,
                        "❌ Erreur": data.get("error", "Erreur inconnue"),
                        "👤 Validé par": st.session_state.current_user,
                        "⏰ Date de validation": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
            except Exception as e:
                results.append({
                    "🔢 Numéro original": raw,
                    "📱 Numéro normalisé": e164,
                    "✅ Statut": False,
                    "❌ Erreur": str(e),
                    "👤 Validé par": st.session_state.current_user,
                    "⏰ Date de validation": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            
            valid_count = sum(1 for r in results if r.get("✅ Statut") == True)
            invalid_count = len(results) - valid_count
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("✅ Valides", valid_count)
            with col2:
                st.metric("❌ Invalides", invalid_count)
            with col3:
                st.metric("📊 Total", len(results))
            
            time.sleep(1)
            progress_bar.progress(i/total)

        status_text.empty()
        progress_bar.empty()

        st.success("🎉 Validation terminée avec succès!\n\nTous vos numéros ont été traités. Consultez les résultats ci-dessous.")

        df = pd.DataFrame(results)
        if not df.empty:
            st.subheader("📋 Résultats détaillés")
            st.dataframe(
                df,
                use_container_width=True,
                height=min(400, len(df) * 40 + 100)
            )

            valid_final = sum(1 for r in results if r.get("✅ Statut") == True)
            invalid_final = len(results) - valid_final
            success_rate = (valid_final / len(results)) * 100 if results else 0

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("✅ Valides", valid_final)
            with col2:
                st.metric("❌ Invalides", invalid_final)
            with col3:
                st.metric("📊 Total", len(results))
            with col4:
                st.metric("📈 Taux de succès", f"{success_rate:.1f}%")

            st.subheader("📥 Exportation des résultats")
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            filename = f"validation_numeros_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            st.download_button(
                label="📥 Télécharger les résultats (CSV)",
                data=csv,
                file_name=filename,
                mime="text/csv",
                use_container_width=True,
                help=f"Fichier: {filename} - {len(results)} numéros traités"
            )

# --- Pied de page ---
st.markdown("---")
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
st.markdown("🚀 Développé par DATAY | Solution professionnelle de validation de numéros")
st.markdown("Designé par A.Rochdi 🚛")
st.markdown("</div>", unsafe_allow_html=True)
st.caption("Propulsé par Streamlit & Abstract API")
