// Création du menu au clic droit
browser.contextMenus.create({
  id: "bibrai-encode",
  title: "Encoder en BIBRAI",
  contexts: ["selection"]
});

browser.contextMenus.create({
  id: "bibrai-decode",
  title: "Décoder depuis BIBRAI",
  contexts: ["selection"]
});

// Action quand on clique sur le menu
browser.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "bibrai-encode" || info.menuItemId === "bibrai-decode") {
    browser.tabs.sendMessage(tab.id, {
      action: info.menuItemId
    });
  }
});