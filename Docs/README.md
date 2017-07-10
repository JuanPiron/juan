Stage 4A STI INSA CVL
06 Juin 2017 - 04 Aout 2017

Stagiaire :  Juan PIRON
Entreprise : Telespazio France

Sujet du stage : etude de la gestion en configuration des demandes de flux PGL via le logiciel CAPIRCA.

Description :
CAPIRCA est un logiciel développé par GOOGLE pour automatiser la création des ACL sur les firewalls.

Il prend en compte les access-list cisco et à ce titre devrait moyennant quelques adaptations, prendre en compte le firewall interne du CSG (PGL).

Le stagiaire étudiera la possibilité de migrer les règles existantes du PGL dans ce logiciel et mettra en place les mécanismes adéquat permettant la gestion de configuration des demandes flux.



Le stage consistera donc à

·         Adapter CAPIRCA pour la génération d’accès-list ASA (similaires à celles des routeurs cisco)

·         Mettre en place un mécanisme de génération des règles et de leur gestion en configuration (git ou subversion ?) à partir des demandes de flux utilisateurs.

·         Adapter les règles existante pour les injecter dans le système CAPIRCA.

Reformulation :

1/ Créer un generator CiscoASA pour les routeurs PGL.

2/

a) Suffit de mettre capirca sur un remote repository de creer la policie ou de la modifer et de lancer le script python, suffit juste ensuite de faire git add, commit et push.
b) Mettre en place un remote repository sur GitHub permettant la gestion des différents ACLs (filters et policies (surtout)), tout cela directement dans les repertoires de pol et filters de capirca.

3/ créer les policies des ACLs déjà existante au niveau de PGLs


Compte-rendu journalier :

06 Juin 2017 :
Visite rapide du CT + badge.
Prise en main de capirca.

07 Juin 2017 :
Circuit arrivé. Revision de GitHub. Modif de aclgen.py pour le rep de dest des acls crées (filters).

08 Juin 2017 :
Debut de redaction du STB, et installation de Gobs sur une debian.

09 Juin 2017 :
Formation sauvegarde au CDL3 et finalisation du STB v1.

12 Juin 2017 :
Fin redaction du STB et envoie. Config de Gobs, git.

13 Juin 2017 :
Fonctionnement de capirca, test, qu'est ce que le PGL.

14 Juin 2017
Debut de programmation de translate.py, permettant de passer d'un langage de bas niveau asa cisco à du .pol, def de la sol de recup de la show-run existante dans capirca.

15 Juin 2017
Suite de la prog de translate.py.

16 Juin 2017
Obtention de la derniere show-run. Decisions de recommencer le translate.py en ne ce bassant plus sur le .csv mais directement sur la .txt. Debut de prog de recupObjet.py.

19 Juin 2017
Prog de recupObjet.txt. Changement avec utilisation des regexs en regexObject.txt.

20 Juin 2017
Fin prog de regexObject.py (à pofiner). Plannification du dev de termWrite.py.

21 Juin 2017
regexObject.py

22 Juin 2017
regexObject.py

23 Juin 2017
regexObject.py, termWrite.py

24 Juin 2017
STB2 et petit tour à Atlas pour trouver des rapports de stage.

25 Juin 2017
Travail sur sync. 

26 Juin 2017
Travail sur sync.

27 Juin 2017
Travail surs sync. Plus documentation.

28 Juin 2017
Travail sur diff, et run.sh. Plus documentation.

29 Juin 2017
Travail sur diff. Fin test avec run.sh , premiere version beta.

30 Juin 2017
Configuration du serveur test avec installation de centos 7 et maj.

03 Juillet 2017
Installation et configuration de gogs.

04 Juillet 2017
Test de gitolite.

05 Juillet 2017
Test de gitolite et verif code.

06 Juillet 2017
Mise en place maquette ciscoasa 5520.

07 Juillet 2017
Travail sur pexpect de python pour recuperer la running-config.
