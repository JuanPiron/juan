# coding: utf8

#################################################
#	Programme Python 2.7			#
#	auteur : Juan Piron, Kourou, 2017	#
#	licence : GPL				#
#################################################


############################################
#	importations de fonctions externes :

import getopt
import sys
import csv

########################################
#	Définition locale de fonctions :

def traitement(finame, foname):
	iFile = open(finame, "rb")
	oFile = open(foname, "wb") 
	try:
		reader = csv.DictReader(iFile)
		for row in reader:
			oFile.write(row["Action"])
	finally:
		iFile.close()
		oFile.close()


######################################
#	Corps principal du programme :

def main():
	type[]
	opts, args = getopt.getopt(sys.argv[1:], "hi:o:t:", ["help", "input=", "output=", "type="])
	for o, a in opts:
		if o in ('-i', '--input'):
			finame=a
		if o in ('-o', 'output'):
			foname=a
		elif o in ('-h', '--help'):
			print("--help (-h) : afficher l'aide")
			print("--input (-i) : fichier csv à traiter")
			print("--output (-o) : fichier.asdm de destination")
		elif o in ('-t', '--type'):
			if a in ('ciscoasa'):
				type.append(a)
	traitement(finame, foname)

if __name__ == "__main__":
    main()
