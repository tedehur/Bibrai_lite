#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <sstream>
#include <iomanip>

using namespace std;

// Le Dictionnaire BIBRAI
const map<int, string> DICTIONNAIRE = {
    {0xC0, "le"}, {0xC1, "la"}, {0xC2, "les"}, {0xC3, "de"}, {0xC4, "des"},
    {0xC5, "un"}, {0xC6, "une"}, {0xC7, "et"}, {0xC8, "est"}, {0xC9, "en"},
    {0xCA, "que"}, {0xCB, "qui"}, {0xCC, "dans"}, {0xCD, "pour"}, {0xCE, "pas"},
    {0xCF, "sur"}, {0xD0, "au"}, {0xD1, "ce"}, {0xD2, "il"}, {0xD3, "elle"},
    {0xD4, "nous"}, {0xD5, "vous"}, {0xD6, "ils"}, {0xD7, "je"}, {0xD8, "tu"},
    {0xD9, "the"}, {0xDA, "and"}, {0xDB, "to"}, {0xDC, "of"}, {0xDD, "a"},
    {0xDE, "in"}, {0xDF, "is"}, {0xE0, "for"}, {0xE1, "that"}, {0xE2, "it"},
    {0xE3, "with"}, {0xE4, "as"}, {0xE5, "was"}, {0xE6, "on"}, {0xE7, "are"},
    {0xE8, "be"}, {0xE9, "at"}, {0xEA, "this"}, {0xEB, "have"}, {0xEC, "from"},
    {0xED, "or"}, {0xEE, "one"}, {0xEF, "had"}, {0xF0, "by"}, {0xF1, "word"},
    {0xF2, "but"}, {0xF3, "not"}, {0xF4, "what"}, {0xF5, "all"}, {0xF6, "were"},
    {0xF7, "we"}, {0xF8, "when"}, {0xF9, "your"}, {0xFA, "can"}, {0xFB, "said"},
    {0xFC, "there"}, {0xFD, "use"}, {0xFE, "an"}, {0xFF, "each"}
};

const int CODE_MAJUSCULE = 0x0E;
const int CODE_ESPACE = 0x20;

// Dictionnaire inversé (Mot -> Code)
map<string, int> DICTIONNAIRE_INVERSE;
void initialiserDictionnaireInverse() {
    for (auto const& [code, mot] : DICTIONNAIRE) {
        DICTIONNAIRE_INVERSE[mot] = code;
    }
}

// Fonction pour séparer un mot de sa ponctuation
void separerPonctuation(const string& mot, string& motPropre, string& ponctuation) {
    size_t pos = mot.find_first_of(".,!?;:");
    if (pos != string::npos) {
        motPropre = mot.substr(0, pos);
        ponctuation = mot.substr(pos);
    } else {
        motPropre = mot;
        ponctuation = "";
    }
}

// Encodage BIBRAI en C++
vector<int> encoderBibrai(const string& texte) {
    vector<int> flux;
    stringstream ss(texte);
    string mot;
    bool premierMot = true;

    while (ss >> mot) {
        string motPropre, ponctuation;
        separerPonctuation(mot, motPropre, ponctuation);

        bool estMajuscule = !motPropre.empty() && isupper(motPropre[0]);
        string motMinuscule = motPropre;
        for (char& c : motMinuscule) c = tolower(c);

        if (DICTIONNAIRE_INVERSE.find(motMinuscule) != DICTIONNAIRE_INVERSE.end()) {
            // Mot dans le dictionnaire
            if (estMajuscule) flux.push_back(CODE_MAJUSCULE);
            flux.push_back(DICTIONNAIRE_INVERSE[motMinuscule]);
        } else {
            // Mot inconnu
            if (!premierMot) flux.push_back(CODE_ESPACE);
            if (estMajuscule) flux.push_back(CODE_MAJUSCULE);
            for (char c : motMinuscule) {
                flux.push_back(static_cast<int>(c));
            }
        }

        // Ajout ponctuation
        for (char c : ponctuation) {
            flux.push_back(static_cast<int>(c));
        }
        
        premierMot = false;
    }
    return flux;
}

// Décodage BIBRAI en C++
string decoderBibrai(const vector<int>& flux) {
    string texteFinal = "";
    bool majusculeSuivante = false;
    string motEnCours = "";

    for (int octet : flux) {
        if (octet == CODE_MAJUSCULE) {
            majusculeSuivante = true;
            continue;
        }
        if (octet == CODE_ESPACE) {
            if (!motEnCours.empty()) {
                texteFinal += motEnCours + " ";
                motEnCours = "";
            }
            continue;
        }

        if (DICTIONNAIRE.find(octet) != DICTIONNAIRE.end()) {
            if (!motEnCours.empty()) {
                texteFinal += motEnCours + " ";
                motEnCours = "";
            }
            string mot = DICTIONNAIRE.at(octet);
            if (majusculeSuivante) {
                mot[0] = toupper(mot[0]);
                majusculeSuivante = false;
            }
            texteFinal += mot + " ";
        } else {
            char c = static_cast<char>(octet);
            if (majusculeSuivante) {
                c = toupper(c);
                majusculeSuivante = false;
            }
            motEnCours += c;
        }
    }
    if (!motEnCours.empty()) texteFinal += motEnCours;
    
    // Nettoyage de l'espace final
    if (!texteFinal.empty() && texteFinal.back() == ' ') {
        texteFinal.pop_back();
    }
    return texteFinal;
}

// --- ZONE DE TEST ---
int main() {
    initialiserDictionnaireInverse();
    
    string phraseTest = "Le chat est dans la maison pour le repas. Il est content !";
    cout << "Phrase originale : " << phraseTest << endl;

    vector<int> flux = encoderBibrai(phraseTest);
    
    cout << "Flux BIBRAI (Hex) : ";
    for (int b : flux) {
        cout << "0x" << uppercase << hex << setw(2) << setfill('0') << b << " ";
    }
    cout << dec << endl; // Reset hex
    
    string phraseDecodee = decoderBibrai(flux);
    cout << "Phrase decodee   : " << phraseDecodee << endl;

    return 0;
}
