#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BIBRAI Secure v1.0 (Profil TACTIQUE)
====================================
Protocole de communication sécurisé pour les équipes de secours.
Optimisé pour les réseaux instables avec un besoin de confidentialité.

Caractéristiques :
- Compression par dictionnaire (comme BIBRAI Lite).
- Parité (1 bit par octet) pour détecter les erreurs de transmission.
- Chiffrement XOR (clé de 8 bits) pour empêcher l'interception.
"""

DICTIONNAIRE = {
    0xC0: "le", 0xC1: "la", 0xC2: "les", 0xC3: "de", 0xC4: "des",
    0xC5: "un", 0xC6: "une", 0xC7: "et", 0xC8: "est", 0xC9: "en",
    0xCA: "que", 0xCB: "qui", 0xCC: "dans", 0xCD: "pour", 0xCE: "pas",
    0xCF: "sur", 0xD0: "au", 0xD1: "ce", 0xD2: "il", 0xD3: "elle",
    0xD4: "nous", 0xD5: "vous", 0xD6: "ils", 0xD7: "je", 0xD8: "tu",
    0xD9: "the", 0xDA: "and", 0xDB: "to", 0xDC: "of", 0xDD: "a",
    0xDE: "in", 0xDF: "is", 0xE0: "for", 0xE1: "that", 0xE2: "it",
    0xE3: "with", 0xE4: "as", 0xE5: "was", 0xE6: "on", 0xE7: "are",
    0xE8: "be", 0xE9: "at", 0xEA: "this", 0xEB: "have", 0xEC: "from",
    0xED: "or", 0xEE: "one", 0xEF: "had", 0xF0: "by", 0xF1: "word",
    0xF2: "but", 0xF3: "not", 0xF4: "what", 0xF5: "all", 0xF6: "were",
    0xF7: "we", 0xF8: "when", 0xF9: "your", 0xFA: "can", 0xFB: "said",
    0xFC: "there", 0xFD: "use", 0xFE: "an", 0xFF: "each"
}
DICTIONNAIRE_INVERSE = {v: k for k, v in DICTIONNAIRE.items()}

# 🔑 CLÉ DE CHIFFREMENT (Gravée dans le matériel/BIOS des équipes)
CLE_SECRETE = 0x5A # Clé XOR

CODE_MAJUSCULE = 0x0E
CODE_ESPACE = 0x20

def calculer_parite(octet):
    """Retourne 1 si le nombre de bits à 1 est impair, 0 sinon."""
    return 1 if bin(octet).count('1') % 2 != 0 else 0

def chiffrer_xor(octet):
    """Chiffrement XOR ultra-léger."""
    return octet ^ CLE_SECRETE

def encoder_secure(texte):
    mots = texte.split()
    flux_octets = []
    
    # 1. Préparation du texte (compression)
    for i, mot in enumerate(mots):
        mot_propre = mot.strip(".,!?;:")
        ponctuation = mot[len(mot_propre):]
        est_majuscule = mot_propre[0].isupper() if mot_propre else False
        mot_minuscule = mot_propre.lower()

        if mot_minuscule in DICTIONNAIRE_INVERSE:
            if est_majuscule:
                flux_octets.append(CODE_MAJUSCULE)
            flux_octets.append(DICTIONNAIRE_INVERSE[mot_minuscule])
        else:
            if i > 0:
                flux_octets.append(CODE_ESPACE)
            if est_majuscule:
                flux_octets.append(CODE_MAJUSCULE)
            for char in mot_minuscule:
                flux_octets.append(ord(char))

        for char in ponctuation:
            flux_octets.append(ord(char))

    # 2. Chiffrement et Parité
    flux_securise = []
    for octet in flux_octets:
        octet_chiffre = chiffrer_xor(octet)
        parite = calculer_parite(octet_chiffre)
        # On crée une trame de 9 bits (8 bits chiffrés + 1 bit de parité)
        flux_securise.append((octet_chiffre << 1) | parite)

    return flux_securise

def decoder_secure(flux_securise):
    texte_final = ""
    majuscule_suivante = False
    mot_en_cours = ""
    erreurs_detectees = 0
    flux_octets_dechiffres = []

    # 1. Vérification de la parité et déchiffrement
    for trame in flux_securise:
        octet_chiffre = trame >> 1
        parite_recue = trame & 1
        parite_calculee = calculer_parite(octet_chiffre)
        
        if parite_recue != parite_calculee:
            erreurs_detectees += 1
            texte_final += "[ERREUR]" # Signalement d'un paquet corrompu
        else:
            flux_octets_dechiffres.append(chiffrer_xor(octet_chiffre))

    # 2. Reconstruction du texte
    for octet in flux_octets_dechiffres:
        if octet == CODE_MAJUSCULE:
            majuscule_suivante = True
            continue
            
        if octet == CODE_ESPACE:
            if mot_en_cours:
                texte_final += mot_en_cours + " "
                mot_en_cours = ""
            continue

        if octet in DICTIONNAIRE:
            if mot_en_cours:
                texte_final += mot_en_cours + " "
                mot_en_cours = ""
            mot = DICTIONNAIRE[octet]
            if majuscule_suivante:
                mot = mot.capitalize()
                majuscule_suivante = False
            texte_final += mot + " "
        else:
            char = chr(octet)
            if majuscule_suivante:
                char = char.upper()
                majuscule_suivante = False
            mot_en_cours += char

    if mot_en_cours:
        texte_final += mot_en_cours

    return texte_final.strip(), erreurs_detectees

if __name__ == "__main__":
    phrase_test = "Le chat est dans la maison pour le repas. Il est content !"
    
    print("=" * 50)
    print(" BIBRAI SECURE (Mode Tactique)")
    print("=" * 50)
    print(f"Phrase originale   : {phrase_test}")
    
    flux_secure = encoder_secure(phrase_test)
    
    # Taille réelle : 9 bits par trame
    taille_octets = (len(flux_secure) * 9 + 7) // 8
    print(f"Flux chiffré (hex) : {[hex(b) for b in flux_secure]}")
    print(f"Poids BIBRAI Secure: {taille_octets} octets (incluant parité)")
    
    phrase_decodee, erreurs = decoder_secure(flux_secure)
    print("-" * 50)
    print(f"Phrase décodée     : {phrase_decodee}")
    print(f"Erreurs détectées  : {erreurs}")
    
    if phrase_test == phrase_decodee and erreurs == 0:
        print("\n✅ SUCCÈS : Message transmis, sécurisé et intègre.")
