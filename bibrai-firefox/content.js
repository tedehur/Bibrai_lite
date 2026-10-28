// Le Dictionnaire BIBRAI
const DICTIONNAIRE = {
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
};
const DICTIONNAIRE_INVERSE = {};
for (const [code, mot] of Object.entries(DICTIONNAIRE)) { DICTIONNAIRE_INVERSE[mot] = parseInt(code); }
const CODE_MAJUSCULE = 0x0E;
const CODE_ESPACE = 0x20;

// Écoute du clic droit venant du background
browser.runtime.onMessage.addListener((request) => {
  let selection = window.getSelection();
  if (!selection || selection.toString().length === 0) return;

  if (request.action === "bibrai-encode") {
    let encoded = encoderBibrai(selection.toString());
    remplacerTexte(selection, encoded);
  } else if (request.action === "bibrai-decode") {
    let decoded = decoderBibrai(selection.toString());
    remplacerTexte(selection, decoded);
  }
});

function remplacerTexte(selection, nouveauTexte) {
  if (selection.rangeCount > 0) {
    let range = selection.getRangeAt(0);
    range.deleteContents();
    range.insertNode(document.createTextNode(nouveauTexte));
    selection.removeAllRanges(); // Désélectionne après remplacement
  }
}

function encoderBibrai(texte) {
    let flux = [];
    let mots = texte.split(/\s+/);
    for (let i = 0; i < mots.length; i++) {
        let mot = mots[i];
        if (!mot) continue;
        let match = mot.match(/^([a-zA-ZÀ-ÿ]+)([.,!?;:]*)$/);
        let motPropre = match ? match[1] : mot;
        let ponctuation = match ? match[2] : "";
        let estMajuscule = motPropre[0] === motPropre[0].toUpperCase() && motPropre[0] !== motPropre[0].toLowerCase();
        let motMinuscule = motPropre.toLowerCase();

        if (DICTIONNAIRE_INVERSE.hasOwnProperty(motMinuscule)) {
            if (estMajuscule) flux.push(CODE_MAJUSCULE);
            flux.push(DICTIONNAIRE_INVERSE[motMinuscule]);
        } else {
            if (i > 0 && flux.length > 0) flux.push(CODE_ESPACE);
            if (estMajuscule) flux.push(CODE_MAJUSCULE);
            for (let j = 0; j < motMinuscule.length; j++) {
                flux.push(motMinuscule.charCodeAt(j));
            }
        }
        for (let j = 0; j < ponctuation.length; j++) {
            flux.push(ponctuation.charCodeAt(j));
        }
    }
    return flux.map(b => '0x' + b.toString(16).toUpperCase().padStart(2, '0')).join(' ');
}

function decoderBibrai(texteHex) {
    let hexArray = texteHex.trim().split(/\s+/);
    let fluxOctets = hexArray.map(h => parseInt(h, 16)).filter(n => !isNaN(n));
    let texteFinal = "";
    let majusculeSuivante = false;
    let motEnCours = "";

    for (let i = 0; i < fluxOctets.length; i++) {
        let octet = fluxOctets[i];
        if (octet === CODE_MAJUSCULE) { majusculeSuivante = true; continue; }
        if (octet === CODE_ESPACE) {
            if (motEnCours) { texteFinal += motEnCours + " "; motEnCours = ""; }
            continue;
        }
        if (DICTIONNAIRE[octet]) {
            if (motEnCours) { texteFinal += motEnCours + " "; motEnCours = ""; }
            let mot = DICTIONNAIRE[octet];
            if (majusculeSuivante) { mot = mot.charAt(0).toUpperCase() + mot.slice(1); majusculeSuivante = false; }
            texteFinal += mot + " ";
        } else {
            let char = String.fromCharCode(octet);
            if (majusculeSuivante) { char = char.toUpperCase(); majusculeSuivante = false; }
            motEnCours += char;
        }
    }
    if (motEnCours) texteFinal += motEnCours;
    return texteFinal.trim();
}