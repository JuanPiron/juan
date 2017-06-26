# coding: utf8

#################################################
#	Programme Python 2.7			#
#	auteur : Juan Piron, Kourou, 2017	#
#	licence : GPL				#
#	script : termWrite.py			#
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


def header(foname, interName):
	###############################################
	#	Ecrire le header pour chaque interface :

	print("#################################################################")
	print("		Configuration du header de l'interface : "+interName)
	print("#################################################################\n")
	comment = raw_input("Veuillez entrer le \"comment\" du header : ")
	oFile = open(foname, "wb")
	try:
		oFile.write("header {\n\tcomment:: "+comment+"\n\n")
		oFile.write("\ttarget:: ciscoasa "+interName+"\n")
		oFile.write("}\n\n")
	finally:
		oFile.close()


def traitement():
	#################################
	#	Fonction principale

	# Définition des regexs
	aclRegex1 = r"^\['access-list',(.)*$"
	#aclRegex2 = r"^\['access-list',(.)*'extended', 'deny'(.)*([0-9]{1,3}\.){3}[0-9]{1,3}(:[0-9]{1,5})?' '([0-9]{1,3}\.){3}[0-9]{1,3}(:[0-9]{1,5})?'gt', '1023', 'host'(.)*$"
	aclRegex2 = r"^\['access-list',(.)*'extended', 'deny', (?!'host)(.)*'gt', '1023', 'host'(.)*$"
	remarkRegex = r"^\['access-list',(.)*'remark'(.)*$"
	iFile = open("showRun.csv", "rb")
	iNet = open("NETWORK.net", "rb")
	iSer = open("SERVICES.svc", "rb")

	try:
		lines = iFile.readlines()

		# test des différents cas et écriture des objets capirca dans les fichiers NETWORK.net et SERVICES.svc
		interName = ""
		for i in range(0,len(lines)):
			line = lines[i].rstrip("\r\n")
			row = line.split(",")

			if re.match(aclRegex1,str(row)) is not None:
				if row[1] not in (interName):
					interName = row[1]
					foname = interName+".pol"
					header(foname.replace("/", "_"), interName)
				oFile = open("./policies/"+foname.replace("/", "_"), "ab")
				oFile.write("term "+str(i)+" {\n")
				if re.match(remarkRegex,str(row)) is not None:
					oFile.write("comment:: "+str(row[3]).replace(" ","_")+"\n\n")
					oFile.close()
				elif re.match(aclRegex2,str(row)) is not None:
					mask = maskConverter(row[6])
					oFile.write("source-address:: "+str(row[5])+"/"+str(mask)+"\n")
					oFile.write("source-port:: "+"1024-65535/"+str(row[4])+"\n")
					oFile.write("destination-address:: "+str(row[10])+"/32\n")
					port = row[12]
					protocol = row[4]
					if not port.isdigit():
						try:
                                        		port = socket.getservbyname(port,protocol)
                                        	except socket.error:
                                        		if port in ("citrix-ica"):
                                                		port = 1494
							else:
								# chercher les ports correspondant au motifs.
                                                	else:
                                                		print("Attention port inconnu, entrer le numéro de port correspondant à \""+port+"\" :")
                                                        	port = input()
							oFile.write("destination-port:: "+str(port)+"/"+protocol+"\n")

                                  	else:
                                        	oFile.write("destination-port:: "+port+"/"+protocol+"\n")
					oFile.write("protocol:: "+protocol+"\n")
					oFile.write("action:: "+row[3]+"\n}\n\n")
					oFile.close()

	finally:
		iFile.close()
		iNet.close()
		iSer.close()
		oFile.close()


######################################
#	Corps principal du programme :

def main():
	# gestion des arguments
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
