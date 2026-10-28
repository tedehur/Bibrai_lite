#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BIBRAI Ultra-Light v1.0 (Profil SURVIE)
========================================
Protocole de communication d'urgence absolue.
Optimisé pour les réseaux au bord de la rupture (hertzien saturé, catastrophe).

Règle d'or : Compression maximale. 
- Zéro espace transmis.
- Seuls les 64 mots du dictionnaire sont traduits en 1 octet.
- Le reste est envoyé lettre par lettre.
Le message peut être "collé" à la réception, mais l'humain peut le lire.
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

CODE_MAJUSCULE = 0x0E 

def encoder_ultra_light(texte):
    mots = texte.split()
    flux_octets = []
    
    for mot in mots:
        mot_propre = mot.strip(".,!?;:")
        ponctuation = mot[len(mot_propre):]
        est_majuscule = mot_propre[0].isupper() if mot_propre else False
        mot_minuscule = mot_propre.lower()

        if mot_minuscule in DICTIONNAIRE_INVERSE:
            # Mot dans le dictionnaire : 1 seul octet !
            if est_majuscule:
                flux_octets.append(CODE_MAJUSCULE)
            flux_octets.append(DICTIONNAIRE_INVERSE[mot_minuscule])
        else:
            # Mot inconnu : on encode lettre par lettre, SANS AUCUN ESPACE
            if est_majuscule:
                flux_octets.append(CODE_MAJUSCULE)
            for char in mot_minuscule:
                flux_octets.append(ord(char))

        for char in ponctuation:
            flux_octets.append(ord(char))

    return flux_octets

def decoder_ultra_light(flux_octets):
    texte_final = ""
    majuscule_suivante = False
    
    for octet in flux_octets:
        if octet == CODE_MAJUSCULE:
            majuscule_suivante = True
            continue
            
        if octet in DICTIONNAIRE:
            mot = DICTIONNAIRE[octet]
            if majuscule_suivante:
                mot = mot.capitalize()
                majuscule_suivante = False
            texte_final += mot
        else:
            char = chr(octet)
            if majuscule_suivante:
                char = char.upper()
                majuscule_suivante = False
            texte_final += char
            
    return texte_final

if __name__ == "__main__":
    phrase_test = "Le chat est dans la maison pour le repas. Il est content !"
    
    print("=" * 50)
    print(" BIBRAI ULTRA-LIGHT (Mode Survie)")
    print("=" * 50)
    print(f"Phrase originale   : {phrase_test}")
    
    taille_utf8 = len(phrase_test.encode('utf-8'))
    print(f"Poids UTF-8        : {taille_utf8} octets")
    
    flux_bibrai = encoder_ultra_light(phrase_test)
    taille_bibrai = len(flux_bibrai)
    print(f"Poids BIBRAI       : {taille_bibrai} octets")
    
    gain = (1 - (taille_bibrai / taille_utf8)) * 100
    print("-" * 50)
    print(f"GAIN DE BANDE PASSANTE : {gain:.2f} %")
    print("-" * 50)
    
    phrase_decodee = decoder_ultra_light(flux_bibrai)
    print(f"Phrase décodée     : {phrase_decodee}")
    print("\n(Note : L'absence d'espaces est normale en mode Survie. L'humain lit le message collé.)")
