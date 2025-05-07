# AdvancedPython2BA_FinalProject
Ce projet est un client IA développé pour le jeu Quarto, dans le cadre du cours Python 2BA.

## Stratégie utilisée

L’algorithme implémente une stratégie d’anticipation jusqu’à deux coups à l’avance. 
Voici les grandes lignes de son comportement :

### Victoire anticipée : 
Si une victoire est possible en deux coups, l’IA privilégiera cette option.

### Prévention des risques : 
Si aucune victoire rapide n’est envisageable, elle tentera d’éviter les positions dangereuses,
en empêchant l’adversaire d’avoir des alignements de 2 ou 3 pièces partageant un attribut commun.

### Positionnement stratégique : 
À défaut de menace ou d’opportunité immédiate, l’IA joue sur une case avantageuse, notamment 
les positions centrales.

## Bibliothèques utilisées

### socket
    Pour la gestion de la communication réseau avec le serveur du jeu.
### json
    Lecture et écriture de fichiers JSON pour la configuration et les échanges.
### threading
    Exécution en parallèle de tâches, notamment pour la boucle de réception des messages.