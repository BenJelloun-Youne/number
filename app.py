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

# Style CSS personnalisé - Design moderne et épuré
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Variables CSS modernes */
    :root {
        /* Palette de couleurs premium */
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
        --warning-light: #fbbf24;
        --warning-bg: rgba(245, 158, 11, 0.1);
        
        /* Couleurs neutres sophistiquées */
        --background: #f8fafc;
        --surface: #ffffff;
        --surface-elevated: #ffffff;
        --surface-hover: #f1f5f9;
        --border: #e2e8f0;
        --border-light: #f1f5f9;
        
        /* Texte moderne */
        --text-primary: #0f172a;
        --text-secondary: #334155;
        --text-muted: #64748b;
        --text-light: #94a3b8;
        
        /* Ombres élégantes */
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        
        /* Rayons et transitions */
        --radius: 12px;
        --radius-lg: 16px;
        --radius-xl: 20px;
        --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* Reset global */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    /* Body et conteneur principal */
    .main {
        background: var(--background);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-primary);
        padding: 2rem;
        min-height: 100vh;
    }

    /* Typographie moderne */
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

    h2 {
        font-size: 1.875rem;
        color: var(--text-primary);
    }

    h3 {
        font-size: 1.5rem;
        color: var(--text-secondary);
    }

    p {
        color: var(--text-secondary);
        line-height: 1.6;
        font-size: 1rem;
    }

    /* Boutons modernes */
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
        position: relative;
        overflow: hidden;
    }

    .stButton > button:before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }

    .stButton > button:hover:before {
        left: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
        background: linear-gradient(135deg, #5b5fc7 0%, #6b46c1 100%);
    }

    .stButton > button:active {
        transform: translateY(0);
        box-shadow: var(--shadow);
    }

    /* Cartes premium */
    .card {
        background: var(--surface);
        border-radius: var(--radius-lg);
        padding: 2rem;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }

    .card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-xl);
        border-color: var(--primary-light);
    }

    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--primary-gradient);
        border-radius: var(--radius-lg) var(--radius-lg) 0 0;
    }

    /* Boîtes d'information stylisées */
    .info-box {
        background: var(--surface);
        border: 1px solid var(--border);
        border-left: 4px solid var(--primary);
        padding: 1.5rem;
        border-radius: var(--radius);
        box-shadow: var(--shadow-sm);
        margin: 1rem 0;
        position: relative;
    }

    .info-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: var(--primary-gradient);
        border-radius: 0 0 0 var(--radius);
    }

    .success-box {
        background: var(--success-bg);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-left: 4px solid var(--success);
        padding: 1.5rem;
        border-radius: var(--radius);
        margin: 1rem 0;
    }

    .warning-box {
        background: var(--warning-bg);
        border: 1px solid rgba(245, 158, 11, 0.2);
        border-left: 4px solid var(--warning);
        padding: 1.5rem;
        border-radius: var(--radius);
        margin: 1rem 0;
    }

    .error-box {
        background: var(--error-bg);
        border: 1px solid rgba(239, 68, 68, 0.2);
        border-left: 4px solid var(--error);
        padding: 1.5rem;
        border-radius: var(--radius);
        margin: 1rem 0;
    }

    /* Feature boxes pour la page de connexion */
    .feature-box {
        background: var(--surface);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        border: 1px solid var(--border);
        box-shadow: var(--shadow-sm);
        transition: var(--transition);
        text-align: center;
        height: 100%;
    }

    .feature-box:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow);
        border-color: var(--primary-light);
    }

    /* Inputs modernes */
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
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        outline: none;
    }

    /* Sidebar moderne */
    .css-1d391kg {
        background: var(--surface);
        border-right: 1px solid var(--border);
    }

    .sidebar .sidebar-content {
        background: var(--surface);
    }

    /* Badges élégants */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 0.375rem 0.875rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.025em;
        text-transform: uppercase;
    }

    .badge-admin {
        background: var(--primary-gradient);
        color: white;
        box-shadow: var(--shadow-sm);
    }

    .badge-user {
        background: linear-gradient(135deg, var(--success) 0%, var(--success-light) 100%);
        color: white;
        box-shadow: var(--shadow-sm);
    }

    /* Tableau de données premium */
    .dataframe {
        border-radius: var(--radius-lg);
        overflow: hidden;
        box-shadow: var(--shadow);
        background: var(--surface);
        border: 1px solid var(--border);
    }

    .dataframe th {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        padding: 1.25rem !important;
        border-bottom: 2px solid var(--border) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.875rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }

    .dataframe td {
        padding: 1rem 1.25rem !important;
        color: var(--text-secondary) !important;
        border-bottom: 1px solid var(--border-light) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem !important;
    }

    .dataframe tr:hover td {
        background: var(--surface-hover) !important;
    }

    /* Statuts de validation modernes */
    .valid-true {
        background: var(--success-gradient) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
        border-radius: 9999px !important;
        text-align: center !important;
        font-size: 0.8rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        box-shadow: var(--shadow-sm) !important;
    }

    .valid-false {
        background: linear-gradient(135deg, var(--error) 0%, var(--error-light) 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
        border-radius: 9999px !important;
        text-align: center !important;
        font-size: 0.8rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        box-shadow: var(--shadow-sm) !important;
    }

    /* Progress bar moderne */
    .stProgress > div > div > div {
        background: var(--primary-gradient);
        border-radius: 9999px;
    }

    .stProgress > div > div {
        background: var(--border-light);
        border-radius: 9999px;
    }

    /* Messages d'état */
    .stError {
        background: var(--error-bg);
        border: 1px solid rgba(239, 68, 68, 0.2);
        border-left: 4px solid var(--error);
        color: var(--error);
        padding: 1rem;
        border-radius: var(--radius);
        margin: 1rem 0;
        font-family: 'Inter', sans-serif;
    }

    .stSuccess {
        background: var(--success-bg);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-left: 4px solid var(--success);
        color: var(--success);
        padding: 1rem;
        border-radius: var(--radius);
        margin: 1rem 0;
        font-family: 'Inter', sans-serif;
    }

    .stWarning {
        background: var(--warning-bg);
        border: 1px solid rgba(245, 158, 11, 0.2);
        border-left: 4px solid var(--warning);
        color: var(--warning);
        padding: 1rem;
        border-radius: var(--radius);
        margin: 1rem 0;
        font-family: 'Inter', sans-serif;
    }

    /* Animations fluides */
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

    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    .animate-in {
        animation: fadeInUp 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .animate-slide {
        animation: slideInRight 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* Header navigation */
    .nav-header {
        background: var(--surface);
        border-radius: var(--radius-lg);
        padding: 1rem 2rem;
        box-shadow: var(--shadow);
        border: 1px solid var(--border);
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .user-info {
        display: flex;
        align-items: center;
        gap: 1rem;
        color: var(--text-secondary);
        font-weight: 500;
    }

    /* Responsive design */
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
        
        .nav-header {
            padding: 1rem;
            flex-direction: column;
            gap: 1rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    else:
        # Utilisateurs par défaut
        default_users = {
            "youness": {"password": "admin123", "role": "admin"},
            "imad": {"password": "imad123", "role": "user"},
            "driss": {"password": "driss123", "role": "user"}
        }
        # Sauvegarder les utilisateurs par défaut
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
    # En-tête de la page de connexion
    st.markdown("""
        <div style="text-align: center; margin-bottom: 3rem;" class="animate-in">
            <h1>🔐 Connexion Sécurisée</h1>
            <p style="font-size: 1.2rem; color: var(--text-muted); margin-top: 1rem;">
                Accédez à votre plateforme de validation de numéros
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Présentation de la solution
    st.markdown("""
        <div class="info-box animate-in">
            <h2>📱 Validation de Numéros Français</h2>
            <p>Une solution professionnelle et sécurisée pour valider vos numéros de téléphone français avec une précision maximale.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Fonctionnalités principales
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class="feature-box animate-in">
                <h3>🔍 Validation en temps réel</h3>
                <p>Vérification instantanée et précise de la validité des numéros avec notre API avancée</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="feature-box animate-in">
                <h3>📊 Analyse détaillée</h3>
                <p>Informations complètes sur l'opérateur, le type de ligne et le formatage international</p>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="feature-box animate-in">
                <h3>📥 Export professionnel</h3>
                <p>Exportation des résultats en format CSV avec horodatage et traçabilité complète</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Formulaire de connexion moderne
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            st.markdown("""
                <div class="card animate-slide">
                    <h3 style="text-align: center; margin-bottom: 2rem; color: var(--text-primary);">
                        🚪 Authentification
                    </h3>
                </div>
            """, unsafe_allow_html=True)
            
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
    
    # Informations de connexion (pour la démo)
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div class="info-box animate-in" style="text-align: center;">
            <h4>🚀 Développé par DATAY</h4>
            <p>Solution professionnelle de validation de numéros</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.stop()

# --- Interface principale ---
# Header de navigation moderne
st.markdown(f"""
    <div class="nav-header animate-in">
        <div>
            <h1 style="margin: 0; font-size: 1.5rem;">📞 Validation de Numéros Français</h1>
            <p style="margin: 0; color: var(--text-muted);">Plateforme professionnelle de validation</p>
        </div>
        <div class="user-info">
            <span class="badge badge-{'admin' if is_admin() else 'user'}">
                {'👑 ' + st.session_state.users[st.session_state.current_user]["role"].upper() if st.session_state.current_user else ''}
            </span>
            <span>👤 {st.session_state.current_user}</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Bouton de déconnexion dans la sidebar
with st.sidebar:
    st.markdown("### 🎛️ Panneau de contrôle")
    if st.button("🚪 Déconnexion", use_container_width=True):
        logout()
        st.rerun()

# Interface admin
if is_admin():
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👑 Administration")
    
    if st.sidebar.button("⚙️ Gérer les utilisateurs", use_container_width=True):
        st.session_state.show_user_management = not st.session_state.get('show_user_management', False)
    
    if st.session_state.get('show_user_management', False):
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 👥 Gestion des utilisateurs")
        
        with st.sidebar.form("add_user_form"):
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
                        st.sidebar.success(f"✅ Utilisateur {new_username} ajouté!")
                        st.rerun()
                    else:
                        st.sidebar.error("❌ Cet utilisateur existe déjà")
                else:
                    st.sidebar.error("❌ Veuillez remplir tous les champs")
        
        # Liste des utilisateurs
        st.sidebar.markdown("**👥 Utilisateurs existants**")
        for user in st.session_state.users:
            with st.sidebar.container():
                col1, col2 = st.columns([3, 1])
                role_badge = "admin" if st.session_state.users[user]["role"] == "admin" else "user"
                col1.markdown(f"**{user}**")
                col1.markdown(f"<span class='badge badge-{role_badge}'>{role_badge}</span>", unsafe_allow_html=True)
                if col2.button("🗑️", key=f"del_{user}", help=f"Supprimer {user}"):
                    if user != st.session_state.current_user:  # Empêcher l'auto-suppression
                        del st.session_state.users[user]
                        save_users(st.session_state.users)
                        st.sidebar.success(f"✅ Utilisateur {user} supprimé!")
                        st.rerun()
                    else:
                        st.sidebar.error("❌ Vous ne pouvez pas vous supprimer")

# --- Fonctions de normalisation améliorées ---
def clean_phone_number(raw: str) -> str:
    # Supprimer tous les caractères non numériques sauf +
    cleaned = re.sub(r'[^\d+]', '', raw)
    return cleaned

def normalize_number(raw: str) -> str:
    # Nettoyer le numéro
    raw = clean_phone_number(raw)
    
    # Normalisation
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
st.markdown("""
    <div class="info-box animate-in">
        <h3>📝 Guide d'utilisation</h3>
        <p>Collez vos numéros de téléphone dans le champ ci-dessous (un numéro par ligne). Notre système supporte tous les formats français courants :</p>
        <ul style="margin-top: 1rem; color: var(--text-secondary);">
            <li><strong>Format international :</strong> +33612345678</li>
            <li><strong>Format national :</strong> 0612345678</li>
            <li><strong>Format avec espaces :</strong> +33 6 12 34 56 78</li>
            <li><strong>Format 00 :</strong> 0033612345678</li>
            <li><strong>Sans préfixe :</strong> 612345678</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown("""
        <div class="card animate-in">
            <h3>📋 Saisie des numéros</h3>
        </div>
    """, unsafe_allow_html=True)
    
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
        # --- Fonction d'appel API ---
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

        # --- Traitement par lots avec interface moderne ---
        st.markdown("""
            <div class="info-box animate-in">
                <h3>⚡ Traitement en cours</h3>
                <p>Validation des numéros via notre API professionnelle...</p>
            </div>
        """, unsafe_allow_html=True)
        
        results = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        total = len(raws)
        
        # Conteneur pour les statistiques en temps réel
        stats_container = st.empty()

        for i, raw in enumerate(raws, start=1):
            status_text.markdown(f"""
                <div style="text-align: center; padding: 1rem; background: var(--surface); border-radius: var(--radius); border: 1px solid var(--border);">
                    <h4>📊 Progression: {i}/{total}</h4>
                    <p>Traitement du numéro: <strong>{raw}</strong></p>
                </div>
            """, unsafe_allow_html=True)
            
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
            
            # Affichage des statistiques en temps réel
            valid_count = sum(1 for r in results if r.get("✅ Statut") == True)
            invalid_count = len(results) - valid_count
            
            stats_container.markdown(f"""
                <div style="display: flex; gap: 1rem; justify-content: center; margin: 1rem 0;">
                    <div class="success-box" style="text-align: center; flex: 1;">
                        <h4>✅ Valides</h4>
                        <h2 style="color: var(--success); margin: 0;">{valid_count}</h2>
                    </div>
                    <div class="error-box" style="text-align: center; flex: 1;">
                        <h4>❌ Invalides</h4>
                        <h2 style="color: var(--error); margin: 0;">{invalid_count}</h2>
                    </div>
                    <div class="info-box" style="text-align: center; flex: 1;">
                        <h4>📊 Total</h4>
                        <h2 style="color: var(--primary); margin: 0;">{len(results)}</h2>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            time.sleep(1)  # Délai pour respecter les limites de l'API
            progress_bar.progress(i/total)

        # Nettoyage de l'interface
        status_text.empty()
        progress_bar.empty()

        # Résultats finaux
        st.markdown("""
            <div class="success-box animate-in">
                <h3>🎉 Validation terminée avec succès!</h3>
                <p>Tous vos numéros ont été traités. Consultez les résultats ci-dessous.</p>
            </div>
        """, unsafe_allow_html=True)

        # Affichage du tableau avec style moderne
        df = pd.DataFrame(results)
        
        # Fonction pour styliser la colonne valid
        def highlight_status(val):
            if val == True:
                return 'background-color: var(--success-bg); color: var(--success); font-weight: 600; text-align: center; border-radius: 20px; padding: 0.5rem;'
            elif val == False:
                return 'background-color: var(--error-bg); color: var(--error); font-weight: 600; text-align: center; border-radius: 20px; padding: 0.5rem;'
            return ''

        # Application du style au dataframe
        if not df.empty:
            styled_df = df.style.applymap(highlight_status, subset=['✅ Statut'])
            
            st.markdown("""
                <div class="card animate-in">
                    <h3>📋 Résultats détaillés</h3>
                </div>
            """, unsafe_allow_html=True)
            
            st.dataframe(
                styled_df,
                use_container_width=True,
                height=min(400, len(df) * 40 + 100)
            )

            # Statistiques finales
            valid_final = sum(1 for r in results if r.get("✅ Statut") == True)
            invalid_final = len(results) - valid_final
            success_rate = (valid_final / len(results)) * 100 if results else 0

            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                    <div class="card" style="text-align: center; background: var(--success-bg);">
                        <h3 style="color: var(--success); margin: 0;">✅ Valides</h3>
                        <h1 style="color: var(--success); margin: 0.5rem 0;">{valid_final}</h1>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class="card" style="text-align: center; background: var(--error-bg);">
                        <h3 style="color: var(--error); margin: 0;">❌ Invalides</h3>
                        <h1 style="color: var(--error); margin: 0.5rem 0;">{invalid_final}</h1>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                    <div class="card" style="text-align: center; background: var(--primary-bg);">
                        <h3 style="color: var(--primary); margin: 0;">📊 Total</h3>
                        <h1 style="color: var(--primary); margin: 0.5rem 0;">{len(results)}</h1>
                    </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                    <div class="card" style="text-align: center; background: var(--warning-bg);">
                        <h3 style="color: var(--warning); margin: 0;">📈 Taux de succès</h3>
                        <h1 style="color: var(--warning); margin: 0.5rem 0;">{success_rate:.1f}%</h1>
                    </div>
                """, unsafe_allow_html=True)

            # Section d'export
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
                <div class="card animate-in">
                    <h3>📥 Exportation des résultats</h3>
                    <p>Téléchargez vos résultats au format CSV avec horodatage et traçabilité complète.</p>
                </div>
            """, unsafe_allow_html=True)

            # Génération du CSV
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            filename = f"validation_numeros_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.download_button(
                    label="📥 Télécharger les résultats (CSV)",
                    data=csv,
                    file_name=filename,
                    mime="text/csv",
                    use_container_width=True,
                    help=f"Fichier: {filename} - {len(results)} numéros traités"
                )

# --- Pied de page moderne ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center; padding: 2rem; color: var(--text-muted); border-top: 1px solid var(--border); margin-top: 3rem;">
        <p><strong>📞 Plateforme de Validation de Numéros Français</strong></p>
        <p>Développé par DATAY ❤️ | Version 2.0 | © 2024</p>
        <p style="font-size: 0.8rem;">Propulsé par Streamlit & Abstract API</p>
    </div>
""", unsafe_allow_html=True)