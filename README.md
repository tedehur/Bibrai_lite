
# 🌐 BIBRAI - Le protocole de communication des réseaux extrêmes

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Version](https://img.shields.io/badge/Version-1.1-blue)
![Language](https://img.shields.io/badge/Language-Python_3-yellow)
![License](https://img.shields.io/badge/License-MIT-orange)

**BIBRAI** (pour *Binaire + Braille*) est un protocole de communication binaire ultra-léger. Il est conçu spécifiquement pour les environnements où la bande passante est rare, instable ou coûteuse (réseaux hertziens, Wi-Fi faibles, zones rurales ou en voie de développement).

Face à l'inefficacité des encodages classiques comme l'ASCII ou l'UTF-8 (qui allouent 1 octet complet par caractère et par espace), BIBRAI propose une approche optimisée pour transmettre plus d'informations avec moins de données.

---

## 🛡️ Les 3 Profils BIBRAI

Le protocole s'adapte à votre situation. Trois modes sont disponibles dans ce dépôt :

### 1. 🚀 BIBRAI Lite (`bibrai_lite.py`)
**Le mode standard.** C'est le meilleur compromis pour un usage quotidien sur un réseau faible.
*   **Fonctionnement :** Compression par dictionnaire + gestion intelligente des espaces.
*   **Gain de bande passante :** ~32 %.
*   **Cas d'usage :** Bureautique, messagerie classique sur réseau instable.

### 2. 🆘 BIBRAI Ultra-Light (`bibrai_ultra_light.py`)
**Le mode survie absolue.** À utiliser quand le réseau est au bord de la rupture (catastrophe, hertzien saturé).
*   **Fonctionnement :** Compression maximale. **Zéro espace transmis**. Les mots peuvent être collés à la réception, mais l'humain peut lire le message.
*   **Gain de bande passante :** ~40 à 50 %.
*   **Cas d'usage :** SOS, transmission de coordonnées critiques, télémétrie d'urgence.

### 3. 🔒 BIBRAI Secure (`bibrai_secure.py`)
**Le mode tactique.** Pour les équipes de secours et de sécurité qui ont besoin de confidentialité.
*   **Fonctionnement :** Compression + Parité (détection d'erreurs réseau) + Chiffrement XOR (clé secrète).
*   **Gain de bande passante :** ~25 % (le coût de la sécurité).
*   **Cas d'usage :** Communications militaires, secours sensibles, transfert de données médicales.

---

## 📊 Preuve par les chiffres (BIBRAI Lite)

Sur notre phrase de test : *"Le chat est dans la maison pour le repas. Il est content !"*

| Encodage | Taille | Gain |
| :--- | :--- | :--- |
| **UTF-8 Classique** | 58 octets | - |
| **BIBRAI Lite** | 39 octets | **🚀 -32,76 %** |

*Dans un scénario de communication d'urgence, ce gain de 30 à 50 % représente la différence entre un message qui passe ou qui est perdu.*

---
## 🦊 Extension Firefox (Mode Clic Droit)

Le dossier `bibrai-firefox/` contient une extension prête à l'emploi.
Elle permet d'encoder ou de décoder du texte directement sur n'importe quelle page web via le menu contextuel (clic droit).

**Installation :**
1. Tapez `about:debugging` dans la barre d'adresse de Firefox.
2. Cliquez sur "Ce Firefox" > "Charger un module temporaire...".
3. Sélectionnez le fichier `manifest.json` dans le dossier `bibrai-firefox/`.
4. Sélectionnez du texte sur une page web, faites un clic droit et choisissez "Encoder en BIBRAI".

---
## 🛠️ Utilisation & Test

Le prototype actuel est écrit en **Python 3** (sans aucune dépendance externe) pour démontrer la viabilité du concept.

1. Clonez ce dépôt.
2. Lancez le script de démonstration du mode qui vous intéresse :

```bash
python3 bibrai_lite.py
python3 bibrai_ultra_light.py
python3 bibrai_secure.py
