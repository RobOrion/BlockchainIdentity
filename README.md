# BlockchainIdentity

## Définition de l'identité numérique

L’identité numérique est l’ensemble des traces numériques laissées par un utilisateur en navigant.  Cela comprend alors a fortiori son nom et prénom, une adresse mail, son adresse IP, les cookies générés, les pseudos utilisés, les photos etc.

## Implémentation de la preuve d'autorité

Notre modèle utilise une preuve d'autorité. Ce choix se justifie par le fait que nous sommes sur une blockchain privée et dont l'identité numérique est gérée par un groupe de personnes qui valident la création/modification d'informations.
Dans les transactions nous écrirons alors l'accès à de nouvelles ressources : 
- accès à des liens
- accès à des machines virtuelles
- accès à des fichiers

## Interface GUI

Nous mettons en place une interface permettant aux utilisateurs de rédiger leurs différentes demandes et pour qu'ils puissent consulter leur profil, et pour les administrateurs d'accepter ou de refuser ces mêmes demandes.
