# Validation de lots de numéros français

Cette application Streamlit permet de valider des lots de numéros de téléphone français en utilisant l'API Abstract.

## Prérequis

- Python 3.8 ou supérieur
- Une clé API Abstract (gratuite) : https://www.abstractapi.com/phone-validation

## Installation

1. Clonez ce dépôt
2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

1. Lancez l'application :
```bash
streamlit run app.py
```

2. Dans l'interface web :
   - Entrez votre clé API Abstract
   - Collez vos numéros de téléphone (un par ligne)
   - Cliquez sur "Valider"

## Formats de numéros acceptés

- 0033612345678
- 0612345678
- +33612345678
- 612345678

## Fonctionnalités

- Normalisation automatique des numéros
- Validation via l'API Abstract
- Affichage des résultats dans un tableau
- Informations sur le type de ligne et l'opérateur 