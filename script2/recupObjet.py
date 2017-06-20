# coding: utf8

#################################################
#	Programme Python 2.7			#
#	auteur : Juan Piron, Kourou, 2017	#
#	licence : GPL				#
#	script : recupObjet.py			#
#################################################


############################################
#	importations de fonctions externes :

import getopt
import sys
import csv
import re
from netaddr import IPAddress
import socket

########################################
#	Définition locale de fonctions :

def maskConverter(mask):
	return IPAddress(mask).netmask_bits()


def traitement():
###################################################################################################
# traitement des différents cas d'objets en présence et écriture dans NETWORK.net et SERVICES.svc #

#	iFile = open(finame, "rb")
#	oFile1 = open(foname1, "wb")
#	oFile2 = open(foname2, "wb")
	iFile = open("showRun.csv", "rb")
	oFile1 = open("NETWORK.net", "wb")
	oFile2 = open("SERVICES.svc", "wb")
	try:
		#traitement de object
		reader = csv.reader(iFile)
		for row in reader:
			if row[0] in ("object"):
				previous = row
				if row[1] in ("network"):
					oFile1.write(row[2]+" = ")
				elif row[1] in ("service"):
					oFile2.write(row[2]+" = ")
			
			# traitement de object network
			elif row[0] in ("host"):
				oFile1.write(row[1]+"/32\n")
			elif row[0] in ("subnet"):
				mask = maskConverter(row[2])
				oFile1.write(row[1]+"/"+str(mask)+"\n")
			elif row[0] in ("range"):
				splitAddrLow = row[1].split(".")
				splitAddrUpp = row[2].split(".")
				lowRange = splitAddrLow[3]
				uppRange = splitAddrUpp[3]
				for i in range(int(lowRange),int(uppRange)):
					oFile1.write(splitAddrLow[0]+"."+splitAddrLow[1]+"."+splitAddrLow[2]+"."+str(i)+"\n")
			# traitement de object service
			elif row[0] in ("service"):
				protocol = row[1]
				eq = False
				ranger = False
				for i in range(len(row)):
					if row[i] in ("eq"):
						if eq or ranger:
							oFile2.write(previous[2]+"-dest = ")
						eq = True
						port = row[i+1]
						if not port.isdigit():
							port = socket.getservbyname(row[i+1],protocol)
							oFile2.write(str(port)+"/"+protocol+"\n")
						else:
							oFile2.write(port+"/"+protocol+"\n")

					elif row[i] in ("range"):
						if ranger or eq:
							oFile2.write(previous[1]+" = ")
						ranger = True
						portInf = row[i+1]
						portSup = row[i+2]
						if not portInf.isdigit() and  not portSup.isdigit():
							portInf = socket.getservbyname(row[i+1],protocol)
							portSup = socket.getservbyname(row[i+2],protocol)
							oFile2.write(str(portInf)+"-"+str(portSup)+"/"+protocol+"\n")
						else:
							oFile2.write(portInf+"-"+portSup+"/"+protocol+"\n")
			

	finally:
		iFile.close()
		oFile1.close()
		oFile2.close()


######################################
#	Corps principal du programme :

def main():
	opts, args = getopt.getopt(sys.argv[1:], "hi:o1:o2:", ["help", "input=", "output1=", "output2="])
	for o, a in opts:
		if o in ('-i', '--input'):
			finame=a
		if o in ('-o1', 'output1'):
			foname1=a
		if o in ('-o2', 'output2'):
			foname2=a
		elif o in ('-h', '--help'):
			print("--help (-h) : afficher l'aide")
			print("--input (-i) : fichier csv à traiter")
			print("--output1 (-o1) : fichier.net de destination")
			print("--output12 (-o2) : fichier.svc de destination")

	traitement()

if __name__ == "__main__":
    main()
