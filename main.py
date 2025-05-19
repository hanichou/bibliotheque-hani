import json
import os

FICHIER_BIBLIO = "bibliotheque.json"

# Chargement et sauvegarde

def charger_bibliotheque():
    if os.path.exists(FICHIER_BIBLIO):
        with open(FICHIER_BIBLIO, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def sauvegarder_bibliotheque(bibliotheque):
    with open(FICHIER_BIBLIO, "w", encoding="utf-8") as f:
        json.dump(bibliotheque, f, indent=4, ensure_ascii=False)

# Affichage

def afficher_livres(bibliotheque):
    if not bibliotheque:
        print("📭 La bibliothèque est vide.")
        return
    print("\n📚 Liste des livres :\n")
    for livre in bibliotheque:
        print(f"ID      : {livre['ID']}")
        print(f"Titre   : {livre['Titre']}")
        print(f"Auteur  : {livre['Auteur']}")
        print(f"Année   : {livre['Année']}")
        print(f"Lu      : {'✅ Oui' if livre['Lu'] else '❌ Non'}")
        print(f"Note    : {livre['Note'] if livre['Note'] is not None else '–'}")
        if livre.get('Commentaire'):
            print(f"Commentaire : {livre['Commentaire']}")
        print("-" * 40)

# Génération d'ID

def generer_id_unique(bibliotheque):
    if not bibliotheque:
        return 1
    derniers_ids = [livre['ID'] for livre in bibliotheque]
    return max(derniers_ids) + 1

# Ajout

def ajouter_livre(bibliotheque):
    print("\n➕ Ajouter un nouveau livre")
    titre = input("Titre : ").strip()
    auteur = input("Auteur : ").strip()
    while True:
        annee_str = input("Année de publication : ").strip()
        if annee_str.isdigit():
            annee = int(annee_str)
            break
        print("❌ Veuillez entrer une année valide.")
    nouvel_id = generer_id_unique(bibliotheque)
    nouveau = {"ID": nouvel_id, "Titre": titre, "Auteur": auteur, "Année": annee,
               "Lu": False, "Note": None, "Commentaire": None}
    bibliotheque.append(nouveau)
    print(f"✅ Livre '{titre}' ajouté (ID : {nouvel_id})")

# Suppression

def supprimer_livre(bibliotheque):
    print("\n🗑️ Supprimer un livre")
    id_str = input("ID du livre à supprimer : ").strip()
    if not id_str.isdigit():
        print("❌ ID invalide.")
        return
    idc = int(id_str)
    for livre in bibliotheque:
        if livre['ID'] == idc:
            conf = input(f"Confirmer suppression de '{livre['Titre']}' ? (o/N) : ").lower()
            if conf == 'o':
                bibliotheque.remove(livre)
                print("✅ Livre supprimé.")
            else:
                print("🚫 Suppression annulée.")
            return
    print("❌ Aucun livre trouvé avec cet ID.")

# Recherche

def rechercher_livre(bibliotheque):
    print("\n🔍 Rechercher un livre")
    cle = input("Mot-clé (titre ou auteur) : ").strip().lower()
    resultats = [l for l in bibliotheque
                 if cle in l['Titre'].lower() or cle in l['Auteur'].lower()]
    if resultats:
        afficher_livres(resultats)
    else:
        print("❌ Aucun résultat pour ce mot-clé.")

# Marquer comme lu

def marquer_comme_lu(bibliotheque):
    print("\n📖 Marquer un livre comme lu")
    id_str = input("ID du livre : ").strip()
    if not id_str.isdigit():
        print("❌ ID invalide.")
        return
    idc = int(id_str)
    for livre in bibliotheque:
        if livre['ID'] == idc:
            note_str = input("Note sur 10 (laisser vide pour aucune) : ").strip()
            note = None
            if note_str:
                if note_str.isdigit() and 0 <= int(note_str) <= 10:
                    note = int(note_str)
                else:
                    print("❌ Note invalide, ignorée.")
            commentaire = input("Commentaire (optionnel) : ").strip() or None
            livre['Lu'] = True
            livre['Note'] = note
            livre['Commentaire'] = commentaire
            print(f"✅ Livre '{livre['Titre']}' mis à jour.")
            return
    print("❌ Aucun livre trouvé pour cet ID.")

# Filtrer

def filtrer_livres(bibliotheque):
    print("\n📑 Filtrer livres")
    choix = input("Afficher (1) Lus, (2) Non lus : ").strip()
    if choix == '1':
        lus = [l for l in bibliotheque if l['Lu']]
        afficher_livres(lus)
    elif choix == '2':
        non_lus = [l for l in bibliotheque if not l['Lu']]
        afficher_livres(non_lus)
    else:
        print("❌ Choix invalide.")

# Trier

def trier_livres(bibliotheque):
    print("\n🔀 Trier livres")
    print("1. Par année\n2. Par auteur\n3. Par note")
    choix = input("Votre choix : ").strip()
    if choix == '1':
        tri = sorted(bibliotheque, key=lambda l: l['Année'])
    elif choix == '2':
        tri = sorted(bibliotheque, key=lambda l: l['Auteur'].lower())
    elif choix == '3':
        tri = sorted(bibliotheque, key=lambda l: (l['Note'] is None, l['Note']), reverse=True)
    else:
        print("❌ Choix invalide.")
        return
    afficher_livres(tri)

# Menu principal

def main():
    biblio = charger_bibliotheque()
    while True:
        print("\n=== MENU ===")
        print("1. Afficher tous les livres")
        print("2. Ajouter un livre")
        print("3. Supprimer un livre")
        print("4. Rechercher un livre")
        print("5. Marquer comme lu")
        print("6. Filtrer lus/non lus")
        print("7. Trier livres")
        print("0. Quitter")
        choix = input("Votre choix : ").strip()

        if choix == '1':
            afficher_livres(biblio)
        elif choix == '2':
            ajouter_livre(biblio)
        elif choix == '3':
            supprimer_livre(biblio)
        elif choix == '4':
            rechercher_livre(biblio)
        elif choix == '5':
            marquer_comme_lu(biblio)
        elif choix == '6':
            filtrer_livres(biblio)
        elif choix == '7':
            trier_livres(biblio)
        elif choix == '0':
            sauvegarder_bibliotheque(biblio)
            print("👋 Au revoir !")
            break
        else:
            print("❌ Choix non reconnu, veuillez réessayer.")

if __name__ == "__main__":
    main()
