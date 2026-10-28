# 🌐 BIBRAI - Le protocole de communication des réseaux extrêmes

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Version](https://img.shields.io/badge/Version-1.0_%28Lite%29-blue)
![Language](https://img.shields.io/badge/Language-Python_3-yellow)
![License](https://img.shields.io/badge/License-MIT-orange)

**BIBRAI** (pour *Binaire + Braille*) est un protocole de communication binaire ultra-léger. Il est conçu spécifiquement pour les environnements où la bande passante est rare, instable ou coûteuse (réseaux hertziens, Wi-Fi faibles, zones rurales ou en voie de développement).

Face à l'inefficacité des encodages classiques comme l'ASCII ou l'UTF-8 (qui allouent 1 octet complet par caractère et par espace), BIBRAI propose une approche optimisée pour transmettre plus d'informations avec moins de données.

---

## 🚀 Le Concept : BIBRAI Lite

La première version du protocole, **BIBRAI Lite**, repose sur deux piliers fondamentaux :

1. **L'élimination des espaces inutiles :** Les espaces sont supprimés pour alléger le flux. La structure des mots est déduite logiquement par le décodeur.
2. **Le Dictionnaire Statique Universel :** Les 64 mots les plus fréquents (en français et en anglais) sont "gravés" dans une table de correspondance commune au client et au serveur. Un mot comme "pour" n'est plus envoyé sous forme de 4 lettres (4 octets), mais sous forme d'un seul code binaire (1 octet).

### 📊 Preuve par les chiffres

Sur notre phrase de test : *"Le chat est dans la maison pour le repas. Il est content !"*

| Encodage | Taille | Gain |
| :--- | :--- | :--- |
| **UTF-8 Classique** | 58 octets | - |
| **BIBRAI Lite** | 39 octets | **🚀 -32,76 %** |

*Dans un scénario de communication d'urgence ou sur un réseau hertzien saturé, ce gain de 30 à 50 % représente la différence entre un message qui passe ou qui est perdu.*

---

## 🛠️ Utilisation & Test

Le prototype actuel est écrit en **Python 3** (sans aucune dépendance externe) pour démontrer la viabilité du concept.

1. Clonez ce dépôt.
2. Lancez le script de démonstration :

```bash
python3 bibrai_lite.py
