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
import re

########################################
#	Définition locale de fonctions :

def verifIp(ip):
	###########################
	#	Detecter les @IPs :

	reg = re.compile("^([0-9]{1,3}\.){3}[0-9]{1,3}(:[0-9]{1,5})?$")
	if reg.match(ip):
		return true
	else:
		return false


def services(Service):
	listServ = Service.split(",")
	protocol = "none"
	printServ = ""
	for i in range(len(listServ)):
		cleanServ = listServ[i].split("/")
		if 2 <= len(cleanServ):
			if protocol not in (cleanServ[0]):
				protocol = cleanServ[0]
				printServ += "\tprotocol:: "+protocol+"\n"
			printServ += "\tport-destination:: "+cleanServ[1]+"/"+cleanServ[0]+"\n"
		else :
			printServ += "\tprotocol:: "+listServ[i]+"\n"

	return printServ


def header(foname, interName):
	###############################################
	#	Ecrire le header pour chaque interface :

	print("#################################################################")
	print("		Configuration du header de l'interface : "+interName)
	print("#################################################################\n")
	comment = raw_input("Veuillez entrer le \"comment\" du header : ")
	#nb_target = input("Veuillez entrer le nombre de \"target\" : ")
	#target = []
        #for i in range(nb_target):
	#	type_target = raw_input("Veuillez entrer le type de la target n"+str(i+1)+" : ")
	#	target.append(type_target)
	#iFile = open(finame, "rb")
	oFile = open(foname, "wb")
	try:
		oFile.write("header {\n\tcomment:: "+comment+"\n\n")
		#for i in range(nb_target):
			#oFile.write("\ttarget:: "+target[i]+" "+interName+"\n")
		oFile.write("\ttarget:: ciscoasa "+interName+"\n")
		oFile.write("}\n\n")
	finally:
		oFile.close()


def terms(finame):
	################################################
	#	Ecrire les terms de chaques interfaces :

	iFile = open(finame, "rb")
	interName = "none"
	try:
		reader = csv.DictReader(iFile)
		for row in reader:
			interListe = row["Interface"].split(" ")
			row["Interface"] = interListe[0]
			if row["Interface"] not in (interName):
				interName = row["Interface"]
				foname = interName+".pol"
				header(foname.replace("/", "_"), interName)

			oFile = open(foname.replace("/", "_"), "ab")
			oFile.write("term "+row["#"]+" {\n")

			if row["Description"] in ('[]'):
				oFile.write("\tcomment:: WITHOUT-DESCRIPTION\n")
			else:
				cleanDes = row["Description"].replace("[","")
				cleanDes = cleanDes.replace("]","")
				oFile.write("\tcomment:: "+cleanDes+"\n")

			oFile.write("\tsource-address:: "+row["Source"]+"\n")
			#cleanServ = row["Service"].split("/")
			#oFile.write("\tprotocol:: "+cleanServ[0]+"\n")
			oFile.write("\tsource-port:: \n")
			oFile.write("\tdestination-address:: "+row["Destination"]+"\n")
			recupProtServ = services(row["Service"])
			oFile.write(recupProtServ)

			#oFile.write("\tdestination-port::")
			#for i in range(1,len(cleanServ)):
			#	oFile.write(" "+cleanServ[i])
			#oFile.write("/"+cleanServ[0]+"\n")

			if row["Action"] in ('Permit'):
				oFile.write("\taction:: accept\n}\n\n")
			elif row["Action"] in ('Deny'):
				oFile.write("\taction:: deny\n}\n\n")

			oFile.close()
	finally:
		iFile.close()
		oFile.close()


######################################
#	Corps principal du programme :

def main():
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
	terms(finame)

if __name__ == "__main__":
    main()
