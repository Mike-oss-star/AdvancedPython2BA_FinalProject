# AdvancedPython2BA_FinalProject
Ce code est un Client IA pour un jeu Quarto

## Stratégie utilisée

L'IA anticipe jusqu'à deux coups à l'avance.
Il joue le coup qui le rapproche le plus de la victoire si elle est possible en deux 
coups, sinon il préfèrera jouer un coup qui évite les positions dangereuses pour 
l'adversaire (deux ou trois pièces avec des attributs communs sont alignées).
Si aucun de ces deux cas n'est présent, il jouera sur une position avantageuse 
(au centre).

## Bibliothèques utilisées

### socket
    Pour les communications
### json
    Pour les fichiers json
### threading
    Pour la lecture en boucle