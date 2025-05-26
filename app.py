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
API_KEY = "672787ca530e447c9887fd88d7ba1573"  # Votre clé API Abstract
API_BASE_URL = "https://phonevalidation.abstractapi.com/v1/"

# Configuration de la page
st.set_page_config(
    page_title="Validation de numéros FR",
    page_icon="📞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS moderne et professionnel
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        /* Couleurs principales */
        --primary: #6366f1;
        --primary-light: #818cf8;
        --primary-dark: #4f46e5;
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        
        /* Couleurs d'état */
        --success: #10b981;
        --success-light: #34d399;
        --success-bg: rgba(16, 185, 129, 0.1);
        --error: #ef4444;
        --error-light: #f87171;
        --error-bg: rgba(239, 68, 68, 0.1);
        --warning: #f59e0b;
        --warning-bg: rgba(245, 158, 11, 0.1);
        
        /* Couleurs neutres */
        --background: #f8fafc;
        --surface: #ffffff;
        --surface-hover: #f1f5f9;
        --border: #e2e8f0;
        --text-primary: #1e293b;
        --text-secondary: #334155;
        --text-muted: #475569;
        --text-light: #64748b;
        --text-lighter: #94a3b8;
        
        /* Ombres et effets */
        --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --radius: 12px;
        --radius-lg: 16px;
        --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    .main {
        background: var(--background);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-primary);
        padding: 2rem;
        min-height: 100vh;
    }

    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        letter-spacing: -0.025em;
        line-height: 1.2;
    }

    h1 {
        font-size: 2.5rem;
        font-weight: 700;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .stButton > button {
        background: var(--primary-gradient);
        color: white;
        border: none;
        padding: 0.875rem 2rem;
        border-radius: var(--radius);
        font-weight: 500;
        font-size: 0.95rem;
        font-family: 'Inter', sans-serif;
        transition: var(--transition);
        box-shadow: var(--shadow);
        cursor: pointer;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }

    .card {
        background: var(--surface);
        border-radius: var(--radius-lg);
        padding: 2rem;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
        transition: var(--transition);
        margin: 1rem 0;
    }

    .card h3 {
        color: var(--text-primary);
        font-weight: 600;
        margin-bottom: 1rem;
    }

    .card p {
        color: var(--text-secondary);
        font-weight: 500;
        line-height: 1.5;
    }

    .card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }

    .metric-card {
        background: var(--surface);
        border-radius: var(--radius);
        padding: 1.5rem;
        text-align: center;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
        transition: var(--transition);
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }

    .metric-valid {
        border-left: 4px solid var(--success);
        background: var(--success-bg);
    }

    .metric-invalid {
        border-left: 4px solid var(--error);
        background: var(--error-bg);
    }

    .metric-total {
        border-left: 4px solid var(--primary);
        background: rgba(99, 102, 241, 0.1);
    }

    .metric-rate {
        border-left: 4px solid var(--warning);
        background: var(--warning-bg);
    }

    .status-valid {
        background: var(--success);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .status-invalid {
        background: var(--error);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border: 2px solid var(--border);
        border-radius: var(--radius);
        padding: 0.875rem 1rem;
        font-size: 0.95rem;
        font-family: 'Inter', sans-serif;
        transition: var(--transition);
        background: var(--surface);
        color: var(--text-primary);
        font-weight: 500;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        outline: none;
    }

    .info-box {
        background: var(--surface);
        border: 1px solid var(--border);
        border-left: 4px solid var(--primary);
        padding: 1.5rem;
        border-radius: var(--radius);
        margin: 1rem 0;
        color: var(--text-primary);
    }

    .success-box {
        background: var(--success-bg);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-left: 4px solid var(--success);
        padding: 1.5rem;
        border-radius: var(--radius);
        margin: 1rem 0;
        color: var(--text-primary);
    }

    .error-box {
        background: var(--error-bg);
        border: 1px solid rgba(239, 68, 68, 0.2);
        border-left: 4px solid var(--error);
        padding: 1.5rem;
        border-radius: var(--radius);
        margin: 1rem 0;
        color: var(--text-primary);
    }

    .progress-container {
        background: var(--surface);
        border-radius: var(--radius);
        padding: 1.5rem;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
        margin: 1rem 0;
    }

    .stProgress > div > div > div {
        background: var(--primary-gradient);
        border-radius: 9999px;
    }

    .stProgress > div > div {
        background: var(--border);
        border-radius: 9999px;
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .animate-in {
        animation: fadeInUp 0.6s ease-out;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .main {
            padding: 1rem;
        }
        h1 {
            font-size: 2rem;
        }
        .card {
            padding: 1.5rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

def load_users():
    """Charge les utilisateurs depuis le fichier JSON"""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        default_users = {
            "youness": {"password": "admin123", "role": "admin", "quota": 1000, "quota_used": 0},
            "imad": {"password": "imad123", "role": "user", "quota": 100, "quota_used": 0},
            "driss": {"password": "driss123", "role": "user", "quota": 100, "quota_used": 0}
        }
        save_users(default_users)
        return default_users

def save_users(users):
    """Sauvegarde les utilisateurs dans le fichier JSON"""
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

# Initialisation des états de session
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'users' not in st.session_state:
    st.session_state.users = load_users()

# Fonctions d'authentification
def login(username, password):
    """Authentifie un utilisateur"""
    if username in st.session_state.users and st.session_state.users[username]["password"] == password:
        st.session_state.authenticated = True
        st.session_state.current_user = username
        return True
    return False

def logout():
    """Déconnecte l'utilisateur actuel"""
    st.session_state.authenticated = False
    st.session_state.current_user = None

def is_admin():
    """Vérifie si l'utilisateur actuel est admin"""
    return (st.session_state.current_user and 
            st.session_state.users[st.session_state.current_user]["role"] == "admin")

# Fonctions de validation des numéros
def clean_phone_number(raw: str) -> str:
    """Nettoie un numéro de téléphone en gardant seulement les chiffres et le +"""
    return re.sub(r'[^\d+]', '', str(raw).strip())

def normalize_number(raw: str) -> str:
    """Normalise un numéro de téléphone au format E164"""
    if not raw:
        return ""
    
    raw = clean_phone_number(raw)
    
    # Gestion des différents formats
    if raw.startswith("00"):
        raw = "+" + raw[2:]
    elif raw.startswith("0"):
        raw = "+33" + raw[1:]
    elif not raw.startswith("+") and len(raw) >= 9:
        raw = "+33" + raw
    
    try:
        num = phonenumbers.parse(raw, None)
        if phonenumbers.is_valid_number(num):
            return phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.E164)
    except phonenumbers.NumberParseException:
        pass
    
    return raw

def validate_phone_with_abstract(phone: str) -> dict:
    """
    Valide un numéro de téléphone avec l'API Abstract
    Retourne les données de validation selon la documentation officielle
    """
    try:
        # Construction de l'URL avec les paramètres requis
        params = {
            "api_key": API_KEY,
            "phone": phone,
            "country": "FR"  # Spécifie que c'est pour la France
        }
        
        # Appel à l'API
        response = requests.get(API_BASE_URL, params=params, timeout=15)
        
        # Vérification du statut HTTP
        if response.status_code == 200:
            data = response.json()
            # Vérification plus stricte de la validité
            is_valid = (
                data.get("valid", False) and 
                data.get("format", {}).get("international", "") and
                data.get("country", {}).get("code", "") == "FR" and
                data.get("type", "") in ["MOBILE", "LANDLINE"]
            )
            return {
                "success": True,
                "data": {**data, "valid": is_valid}
            }
        elif response.status_code == 401:
            return {"success": False, "error": "Clé API invalide ou manquante"}
        elif response.status_code == 422:
            return {"success": False, "error": "Quota API atteint"}
        elif response.status_code == 429:
            return {"success": False, "error": "Trop de requêtes par seconde"}
        elif response.status_code == 400:
            return {"success": False, "error": "Requête invalide"}
        else:
            return {"success": False, "error": f"Erreur HTTP {response.status_code}"}
            
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Timeout de l'API"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Erreur réseau: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": f"Erreur inattendue: {str(e)}"}

# Interface de connexion
if not st.session_state.authenticated:
    st.markdown("""
        <div style="text-align: center; margin-bottom: 3rem;" class="animate-in">
            <h1>🔐 Connexion Sécurisée</h1>
            <p style="font-size: 1.2rem; color: var(--text-muted); margin-top: 1rem;">
                Accédez à votre plateforme de validation de numéros français
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Présentation des fonctionnalités
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="card animate-in">
                <h3 style="color: #1e293b; font-weight: 600;">🔍 Validation temps réel</h3>
                <p style="color: #334155; font-weight: 500;">Vérifiez instantanément la validité de vos numéros français avec l'API Abstract</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card animate-in">
                <h3 style="color: #1e293b; font-weight: 600;">📊 Analyse complète</h3>
                <p style="color: #334155; font-weight: 500;">Obtenez les détails sur l'opérateur, le type de ligne et la localisation</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="card animate-in">
                <h3 style="color: #1e293b; font-weight: 600;">🔄 Intégration CRM</h3>
                <p style="color: #334155; font-weight: 500;">Intégration facile avec votre CRM pour une validation automatisée</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Avantages d'intégration CRM
    st.markdown("""
        <div class="card animate-in" style="margin-top: 2rem;">
            <h3 style="color: #1e293b; font-weight: 600; text-align: center; margin-bottom: 1.5rem;">💼 Avantages de l'intégration CRM</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
                <div style="background: var(--surface-hover); padding: 1.5rem; border-radius: var(--radius); border: 1px solid var(--border);">
                    <h4 style="color: var(--primary); font-weight: 600;">🔄 Synchronisation automatique</h4>
                    <p style="color: #334155; font-weight: 500;">Validation en temps réel des numéros lors de leur saisie dans votre CRM</p>
                </div>
                <div style="background: var(--surface-hover); padding: 1.5rem; border-radius: var(--radius); border: 1px solid var(--border);">
                    <h4 style="color: var(--primary); font-weight: 600;">📊 Qualité des données</h4>
                    <p style="color: #334155; font-weight: 500;">Base de données propre et fiable pour vos campagnes marketing</p>
                </div>
                <div style="background: var(--surface-hover); padding: 1.5rem; border-radius: var(--radius); border: 1px solid var(--border);">
                    <h4 style="color: var(--primary); font-weight: 600;">⚡ Performance</h4>
                    <p style="color: #334155; font-weight: 500;">Optimisation des taux de contact et réduction des coûts d'appel</p>
                </div>
                <div style="background: var(--surface-hover); padding: 1.5rem; border-radius: var(--radius); border: 1px solid var(--border);">
                    <h4 style="color: var(--primary); font-weight: 600;">🎯 ROI amélioré</h4>
                    <p style="color: #334155; font-weight: 500;">Augmentation de l'efficacité de vos campagnes et meilleure rentabilité</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Formulaire de connexion
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div class="card animate-in">
                <h3 style="text-align: center; margin-bottom: 2rem;">🚪 Authentification</h3>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("👤 Nom d'utilisateur", placeholder="Entrez votre nom d'utilisateur")
            password = st.text_input("🔑 Mot de passe", type="password", placeholder="Entrez votre mot de passe")
            submit = st.form_submit_button("🔓 Se connecter", use_container_width=True)
            
            if submit:
                if username and password:
                    if login(username, password):
                        st.success(f"🎉 Bienvenue {username}! Redirection en cours...")
                        time.sleep(1.5)
                        st.rerun()
                    else:
                        st.error("❌ Identifiants incorrects. Veuillez réessayer.")
                else:
                    st.error("❌ Veuillez remplir tous les champs.")
    
    # Comptes de démonstration
    st.markdown("""
        <div class="info-box animate-in" style="text-align: center; margin-top: 2rem;">
            <h4>📋 Comptes de démonstration</h4>

        </div>
    """, unsafe_allow_html=True)
    
    st.stop()

# Interface principale
st.markdown(f"""
    <div class="card animate-in" style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="margin: 0; font-size: 1.8rem;">📞 Validation de Numéros Français</h1>
            <p style="margin: 0; color: var(--text-muted);">Plateforme professionnelle powered by Datay</p>
        </div>
        <div style="text-align: right;">
            <span style="background: var(--primary-gradient); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600;">
                {'👑 ADMIN' if is_admin() else '👤 USER'}: {st.session_state.current_user}
            </span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎛️ Panneau de contrôle")
    
    if st.button("🚪 Déconnexion", use_container_width=True):
        logout()
        st.rerun()
    
    # Interface admin
    if is_admin():
        st.markdown("---")
        st.markdown("### 👑 Administration")
        
        if st.button("⚙️ Gérer les utilisateurs", use_container_width=True):
            st.session_state.show_user_management = not st.session_state.get('show_user_management', False)
        
        if st.session_state.get('show_user_management', False):
            st.markdown("---")
            st.markdown("### 👥 Gestion des utilisateurs")
            
            # Ajout d'utilisateur
            with st.form("add_user_form"):
                st.markdown("**➕ Ajouter un utilisateur**")
                new_username = st.text_input("Nom d'utilisateur")
                new_password = st.text_input("Mot de passe", type="password")
                new_role = st.selectbox("Rôle", ["user", "admin"])
                new_quota = st.number_input("Quota de validation", min_value=10, max_value=10000, value=100, step=10)
                submit = st.form_submit_button("✅ Ajouter", use_container_width=True)
                
                if submit:
                    if new_username and new_password:
                        if new_username not in st.session_state.users:
                            st.session_state.users[new_username] = {
                                "password": new_password,
                                "role": new_role,
                                "quota": new_quota,
                                "quota_used": 0
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
                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                role = st.session_state.users[user]["role"]
                quota = st.session_state.users[user]["quota"]
                quota_used = st.session_state.users[user].get("quota_used", 0)
                quota_remaining = quota - quota_used
                
                col1.markdown(f"**{user}** ({role})")
                col2.markdown(f"Quota total: {quota}")
                col3.markdown(f"Utilisé: {quota_used} / Restant: {quota_remaining}")
                
                if col4.button("🗑️", key=f"del_{user}", help=f"Supprimer {user}"):
                    if user != st.session_state.current_user:
                        del st.session_state.users[user]
                        save_users(st.session_state.users)
                        st.success(f"✅ Utilisateur {user} supprimé!")
                        st.rerun()
                    else:
                        st.error("❌ Vous ne pouvez pas vous supprimer")
                
                # Modification du quota
                with st.expander(f"📊 Modifier le quota de {user}"):
                    with st.form(f"quota_form_{user}"):
                        new_quota = st.number_input(
                            "Nouveau quota",
                            min_value=10,
                            max_value=10000,
                            value=quota,
                            step=10,
                            key=f"quota_{user}"
                        )
                        reset_quota = st.checkbox("Réinitialiser l'utilisation du quota", key=f"reset_{user}")
                        if st.form_submit_button("✅ Mettre à jour"):
                            st.session_state.users[user]["quota"] = new_quota
                            if reset_quota:
                                st.session_state.users[user]["quota_used"] = 0
                            save_users(st.session_state.users)
                            st.success(f"✅ Quota de {user} mis à jour!")
                            st.rerun()

# Interface de validation
st.markdown("""
    <div class="info-box animate-in">
        <h3>📝 Guide d'utilisation</h3>
        <p>Saisissez vos numéros de téléphone français (un par ligne). Formats supportés :</p>
        <ul style="margin-top: 1rem; color: var(--text-secondary);">
            <li><strong>International :</strong> +33612345678</li>
            <li><strong>National :</strong> 0612345678</li>
            <li><strong>Avec espaces :</strong> +33 6 12 34 56 78</li>
            <li><strong>Format 00 :</strong> 0033612345678</li>
            <li><strong>Sans préfixe :</strong> 612345678</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

# Affichage du quota
current_user = st.session_state.current_user
user_quota = st.session_state.users[current_user]["quota"]
quota_used = st.session_state.users[current_user].get("quota_used", 0)
quota_remaining = user_quota - quota_used

# Calcul du pourcentage d'utilisation
usage_percentage = (quota_used / user_quota) * 100 if user_quota > 0 else 0

st.markdown("### 📊 Votre quota de validation")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Quota total", user_quota)

with col2:
    st.metric("Restant", quota_remaining)

with col3:
    st.metric("Utilisé", quota_used)

st.progress(usage_percentage / 100)

# Zone de saisie
st.markdown("""
    <div class="card animate-in">
        <h3>📋 Saisie des numéros</h3>
    </div>
""", unsafe_allow_html=True)

numbers_text = st.text_area(
    "Collez vos numéros ici",
    placeholder="Exemple:\n+33612345678\n0612345678\n06 12 34 56 78\n0033612345678\n612345678",
    height=200,
    help=f"Un numéro par ligne. Quota restant : {quota_remaining} numéros"
)

# Validation
if st.button("🔍 Lancer la validation", use_container_width=True):
    raws = [line.strip() for line in numbers_text.splitlines() if line.strip()]
    
    if not raws:
        st.error("❌ Veuillez saisir au moins un numéro à valider.")
    elif len(raws) > quota_remaining:
        st.error(f"❌ Vous avez dépassé votre quota restant ({quota_remaining} numéros).")
    else:
        # Mise à jour du quota utilisé
        st.session_state.users[current_user]["quota_used"] = quota_used + len(raws)
        save_users(st.session_state.users)
        
        # Animation d'attente
        with st.spinner("⚡ Initialisation de la validation..."):
            time.sleep(1)
        
        st.markdown("""
            <div class="info-box animate-in">
                <h3 style="color: #1e293b; font-weight: 600;">⚡ Validation en cours</h3>
                <p style="color: #334155; font-weight: 500;">Traitement de vos numéros via l'API Abstract...</p>
            </div>
        """, unsafe_allow_html=True)
        
        results = []
        progress_bar = st.progress(0)
        status_container = st.empty()
        stats_container = st.empty()
        total = len(raws)

        for i, raw in enumerate(raws, start=1):
            # Animation de chargement pour chaque numéro
            with st.spinner(f"Validation du numéro {i}/{total}..."):
                # Affichage du statut
                status_container.markdown(f"""
                    <div class="progress-container">
                        <h4 style="color: #1e293b; font-weight: 600;">📊 Progression: {i}/{total}</h4>
                        <p style="color: #334155; font-weight: 500;">Traitement du numéro: <code>{raw}</code></p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Normalisation du numéro
                normalized = normalize_number(raw)
                
                # Appel à l'API Abstract
                api_result = validate_phone_with_abstract(normalized)
                
                if api_result["success"]:
                    data = api_result["data"]
                    results.append({
                        "🔢 Numéro original": raw,
                        "📱 Numéro normalisé": data.get("phone", normalized),
                        "✅ Statut": "✅ Valide" if data.get("valid", False) else "❌ Invalide",
                        "🌍 Format international": data.get("format", {}).get("international", ""),
                        "🏠 Format local": data.get("format", {}).get("local", ""),
                        "🏳️ Pays": data.get("country", {}).get("name", ""),
                        "📞 Type": data.get("type", ""),
                        "📡 Opérateur": data.get("carrier", ""),
                        "📍 Localisation": data.get("location", ""),
                        "👤 Validé par": st.session_state.current_user,
                        "⏰ Date validation": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                else:
                    results.append({
                        "🔢 Numéro original": raw,
                        "📱 Numéro normalisé": normalized,
                        "✅ Statut": "❌ Erreur",
                        "❌ Erreur": api_result["error"],
                        "👤 Validé par": st.session_state.current_user,
                        "⏰ Date validation": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                
                # Statistiques temps réel
                valid_count = sum(1 for r in results if "✅ Valide" in str(r.get("✅ Statut", "")))
                invalid_count = len(results) - valid_count
                
                stats_container.markdown(f"""
                    <div style="display: flex; gap: 1rem; margin: 1rem 0;">
                        <div class="metric-card metric-valid">
                            <h4 style="color: #1e293b; font-weight: 600;">✅ Valides</h4>
                            <h2 style="color: var(--success); font-weight: 700;">{valid_count}</h2>
                        </div>
                        <div class="metric-card metric-invalid">
                            <h4 style="color: #1e293b; font-weight: 600;">❌ Invalides</h4>
                            <h2 style="color: var(--error); font-weight: 700;">{invalid_count}</h2>
                        </div>
                        <div class="metric-card metric-total">
                            <h4 style="color: #1e293b; font-weight: 600;">📊 Total</h4>
                            <h2 style="color: var(--primary); font-weight: 700;">{len(results)}</h2>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Délai pour respecter les limites de l'API (1 req/sec sur plan gratuit)
                time.sleep(1.2)
                progress_bar.progress(i / total)
        
        # Nettoyage interface
        status_container.empty()
        progress_bar.empty()
        
        # Résultats finaux
        st.markdown("""
            <div class="success-box animate-in">
                <h3 style="color: #1e293b; font-weight: 600; margin-bottom: 1rem;">🎉 Validation terminée avec succès!</h3>
                <p style="color: #334155; font-weight: 500; font-size: 1.1rem;">Tous vos numéros ont été traités. Consultez les résultats ci-dessous.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Affichage du tableau
        if results:
            df = pd.DataFrame(results)
            
            st.markdown("""
                <div class="card animate-in">
                    <h3 style="color: #1e293b; font-weight: 600;">📋 Résultats détaillés</h3>
                </div>
            """, unsafe_allow_html=True)
            
            # Configuration de l'affichage du dataframe
            st.dataframe(
                df,
                use_container_width=True,
                height=min(500, len(df) * 50 + 100)
            )
            
            # Statistiques finales
            valid_final = sum(1 for r in results if "✅ Valide" in str(r.get("✅ Statut", "")))
            invalid_final = len(results) - valid_final
            success_rate = (valid_final / len(results)) * 100 if results else 0
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                    <div class="metric-card metric-valid">
                        <h3 style="color: #1e293b; font-weight: 600;">✅ Valides</h3>
                        <h1 style="color: var(--success); font-weight: 700;">{valid_final}</h1>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class="metric-card metric-invalid">
                        <h3 style="color: #1e293b; font-weight: 600;">❌ Invalides</h3>
                        <h1 style="color: var(--error); font-weight: 700;">{invalid_final}</h1>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                    <div class="metric-card metric-total">
                        <h3 style="color: #1e293b; font-weight: 600;">📊 Total</h3>
                        <h1 style="color: var(--primary); font-weight: 700;">{len(results)}</h1>
                    </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                    <div class="metric-card metric-rate">
                        <h3 style="color: #1e293b; font-weight: 600;">📈 Taux succès</h3>
                        <h1 style="color: var(--warning); font-weight: 700;">{success_rate:.1f}%</h1>
                    </div>
                """, unsafe_allow_html=True)
            
            # Export CSV
            st.markdown("""
                <div class="card animate-in">
                    <h3 style="color: #1e293b; font-weight: 600;">📥 Export des résultats</h3>
                    <p style="color: #334155; font-weight: 500;">Téléchargez vos résultats au format CSV avec traçabilité complète.</p>
                </div>
            """, unsafe_allow_html=True)
            
            csv_data = df.to_csv(index=False, encoding='utf-8-sig')
            filename = f"validation_numeros_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.download_button(
                    label="📥 Télécharger les résultats (CSV)",
                    data=csv_data,
                    file_name=filename,
                    mime="text/csv",
                    use_container_width=True,
                    help=f"Fichier: {filename} - {len(results)} numéros traités"
                )

# Section des avantages
st.markdown("---")
st.markdown("### 🎯 Avantages de notre solution")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        #### 🛡️ Sécurité renforcée
        - Élimination des faux numéros
        - Suppression des NRP
        - Base de données propre et sécurisée
    """)
    
    st.markdown("""
        #### 📞 Joignabilité optimale
        - Amélioration des taux de contact
        - Optimisation des campagnes
        - Meilleure efficacité opérationnelle
    """)

with col2:
    st.markdown("""
        #### ⚡ Performance
        - Optimisation du système téléphonique
        - Numéros validés et qualifiés
        - Traitement rapide et fiable
    """)
    
    st.markdown("""
        #### 📊 ROI garanti
        - Réduction des coûts opérationnels
        - Augmentation de l'efficacité
        - Meilleure rentabilité des campagnes
    """)

# Footer avec informations
st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 2rem; color: var(--text-muted); margin-top: 2rem;">
        <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; margin-bottom: 1rem;">
            <div style="background: var(--surface); padding: 1rem; border-radius: var(--radius); border: 1px solid var(--border);">
                <h4 style="color: var(--primary);">🚀 Développé par</h4>
                <p><strong>DATAY</strong></p>
            </div>
            <div style="background: var(--surface); padding: 1rem; border-radius: var(--radius); border: 1px solid var(--border);">
                <h4 style="color: var(--primary);">🎨 Design par</h4>
                <p><strong>A.Rochdi</strong></p>
            </div>
            <div style="background: var(--surface); padding: 1rem; border-radius: var(--radius); border: 1px solid var(--border);">
                <h4 style="color: var(--primary);">⚡ Powered by</h4>
                <p><strong>DATAY</strong></p>
            </div>
        </div>
        <p style="font-size: 0.9rem; color: var(--text-light);">
            📞 Plateforme professionnelle de validation de numéros français | Version 3.0 | © 2024
        </p>
        <p style="font-size: 0.8rem; color: var(--text-lighter);">
            Propulsé par Streamlit & Abstract Phone Validation API
        </p>
    </div>
""", unsafe_allow_html=True)
