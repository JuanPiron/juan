# coding: utf8

#################################################
#	Programme Python 2.7						#
#	auteur : Juan Piron, Kourou, 2017			#
#	licence : GPL								#
#	script : regexObjet.py						#
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
	#################################
	#	Fonction principale

	# Définition des regexs
	netRegex1 = r"^\['object', 'network'(.)*$"
	netRegex2 = r"^\['host'(.)*$"
	netRegex3 = r"^\['subnet'(.)*$"
	netRegex4 = r"^\['range'(.)*$"
	netRegex5 = r"^\['object-group', 'network'(.)*$"
	netRegex6 = r"^\['network-object', 'host'(.)*$"
	netRegex7 = r"^\['network-object',(.)*255(.)*$"
	netRegex8 = r"^\['network-object', 'object'(.)*$"
	netRegex9 = r"^\['group-object',(.)*$"

	serRegex1 = r"^\['object', 'service'(.)*$"
	serRegex2 = r"^\['service', ('tcp'|'udp')?, 'destination', 'eq'(.)*$"
	serRegex3 = r"^\['service', ('tcp'|'udp')?, 'destination', 'range'(.)*$"
	serRegex4 = r"^\['service', ('tcp'|'udp')?, 'source', 'eq'(.)*, 'destination', 'eq'(.)*$"
	serRegex5 = r"^\['service', ('tcp'|'udp')?, 'source', 'eq'(.)*, 'destination', 'range'(.)*$"
	serRegex6 = r"^\['object-group', 'service'(.)*$"
	serRegex7 = r"^\['port-object', 'eq'(.)*$"
	serRegex8 = r"^\['port-object', 'range'(.)*$"
	serRegex9 = r"^\['service-object'(.)*'destination', 'eq'(.)*$"
	serRegex10 = r"^\['service-object'(.)*'destination', 'range'(.)*$"
	serRegex11 = r"^\['group-object',(.)*$"

	#serRegex5.1 = r"^\['service', ('tcp'|'udp')?, 'source', 'range'(.)*, 'destination', 'eq'(.)*$"
	#serRegex5.2 = r"^\['service', ('tcp'|'udp')?, 'source', 'range'(.)*, 'destination', 'range'(.)*$"

	desRegex = r"^\['description'(.)*$"

	iFile = open("showRun.csv", "rb")
	oFile1 = open("NETWORK.net", "wb")
	oFile2 = open("SERVICES.svc", "wb")

	try:
		lines = iFile.readlines()

		# test des différents cas et écriture des objets capirca dans les fichiers NETWORK.net et SERVICES.svc
		for i in range(0,len(lines)):
			line = lines[i].rstrip("\r\n")
			row = line.split(",")

			# cas : object

			# cas : object network
			if re.match(netRegex1,str(row)) is not None:
				next = lines[i+1].rstrip("\r\n")
				below = next.split(",")
				if re.match(desRegex,str(below)) is not None:
					description = ''.join(below[1:])
					oFile1.write('# '+description+"\n")
					next = lines[i+2].rstrip("\r\n")
					below = next.split(",")
				#name = ''.join(row[2:])
				#oFile1.write(name+" = ")
				oFile1.write(row[2]+" = ")
				if re.match(netRegex2,str(below)) is not None:
					oFile1.write(below[1]+"/32\n")
				elif re.match(netRegex3,str(below)) is not None:
					mask = maskConverter(below[2])
					oFile1.write(below[1]+"/"+str(mask)+"\n")
				elif re.match(netRegex4, str(below)) is not None:
					splitAddrLow = below[1].split(".")
					splitAddrUpp = below[2].split(".")
					lowRange = splitAddrLow[3]
					uppRange = splitAddrUpp[3]
					for k in range(int(lowRange),int(uppRange)):
						oFile1.write(splitAddrLow[0]+"."+splitAddrLow[1]+"."+splitAddrLow[2]+"."+str(k)+"\n")
				oFile1.write("\n")

			# cas : object service
			elif re.match(serRegex1,str(row)) is not None:
				next = lines[i+1].rstrip("\r\n")
				below = next.split(",")
				if re.match(desRegex,str(below)) is not None:
					description = ''.join(below[1:])
					oFile1.write('# '+description+"\n")
					next = lines[i+2].rstrip("\r\n")
					below = next.split(",")
				#name = ''.join(row[2:])
				#oFile1.write(name+" = ")
				protocol = below[1]
				if re.match(serRegex2,str(below)) is not None:
					oFile2.write(row[2]+" = ")
					port = below[4]
					if not port.isdigit():
						port = socket.getservbyname(port,protocol)
						oFile2.write(str(port)+"/"+protocol+"\n")
					else:
						oFile2.write(port+"/"+protocol+"\n")
				if re.match(serRegex3,str(below)) is not None:
					oFile2.write(row[2]+" = ")
					portInf = below[4]
					portSup = below[5]
					if not portInf.isdigit() and not portSup.isdigit():
						portInf = socket.getservbyname(row[i+1],protocol)
						portSup = socket.getservbyname(row[i+2],protocol)
						oFile2.write(str(portInf)+"-"+str(portSup)+"/"+protocol+"\n")
					else:
						oFile2.write(portInf+"-"+portSup+"/"+protocol+"\n")
				if re.match(serRegex4,str(below)) is not None:
					# source
					oFile2.write(row[2]+"-source = ")
					port = below[4]
					if not port.isdigit():
						port = socket.getservbyname(port,protocol)
						oFile2.write(str(port)+"/"+protocol+"\n")
					else:
						oFile2.write(port+"/"+protocol+"\n")

					# destination
					oFile2.write(row[2]+"-dest = ")
					port = below[7]
					if not port.isdigit():
						port = socket.getservbyname(port,protocol)
						oFile2.write(str(port)+"/"+protocol+"\n")
					else:
						oFile2.write(port+"/"+protocol+"\n")
				oFile2.write("\n")

			# cas : object-group

			# cas : object-group  network
			if re.match(netRegex5,str(row)) is not None:
				next = lines[i+1].rstrip("\r\n")
				below = next.split(",")
				if re.match(desRegex,str(below)) is not None:
					description = ''.join(below[1:])
					oFile1.write('# '+description+"\n")
					next = lines[i+2].rstrip("\r\n")
					below = next.split(",")
				#name = ''.join(row[2:])
				#oFile1.write(name+" = ")
				oFile1.write(row[2]+" = ")
				j = i
				while below[0] not in ("object-group"):
					if re.match(netRegex6,str(below)) is not None:
						oFile1.write(below[2]+"/32\n")
					elif re.match(netRegex7,str(below)) is not None:
						mask = maskConverter(below[2])
						oFile1.write(below[1]+"/"+str(mask)+"\n")
					elif re.match(netRegex8,str(below)) is not None:
						oFile1.write(below[2]+"\n")
					elif re.match(netRegex9,str(below)) is not None:
						oFile1.write(below[1]+"\n")
					j = j+1
					next = lines[j+1].rstrip("\r\n")
					below = next.split(",")
				oFile1.write("\n")

			# cas : object-group  service
			if re.match(serRegex6,str(row)) is not None:
				next = lines[i+1].rstrip("\r\n")
				below = next.split(",")
				if re.match(desRegex,str(below)) is not None:
					description = ''.join(below[1:])
					oFile1.write('# '+description+"\n")
					next = lines[i+2].rstrip("\r\n")
					below = next.split(",")
				#name = ''.join(row[2:])
				#oFile1.write(name+" = ")
				oFile2.write(row[2]+" = ")
				j = i
				while below[0] not in ("object-group"):
					if re.match(serRegex7,str(below)) is not None:
						protocol = row[3]
						port = below[2]
						#print("ligne : "+str(row)+"\n")
						#print("port :"+str(below[2])+"\n")
						if not port.isdigit():
							try:
								port = socket.getservbyname(port,protocol)
							except socket.error:
								if port in ("citrix-ica"):
									port = 1494
								else:
									print("Attention port inconnu, entrer le numéro de port correspondant à "+port+"\n")
									port = input()
							oFile2.write(str(port)+"/"+protocol+"\n")

						else:
							oFile2.write(port+"/"+protocol+"\n")
					elif re.match(serRegex8,str(below)) is not None:
						protocol = row[3]
						portInf = below[2]
						portSup = below[3]
						if not portInf.isdigit() and not portSup.isdigit():
							portInf = socket.getservbyname(portInf,protocol)
							portSup = socket.getservbyname(portSup,protocol)
							oFile2.write(str(portInf)+"-"+str(portSup)+"/"+protocol+"\n")
						else:
							oFile2.write(portInf+"-"+portSup+"/"+protocol+"\n")
					elif re.match(serRegex9,str(below)) is not None:
						protocol = below[1]
						port = below[4]
						if not port.isdigit():
							port = socket.getservbyname(port,protocol)
							oFile2.write(str(port)+"/"+protocol+"\n")
						else:
							oFile2.write(port+"/"+protocol+"\n")
					elif re.match(serRegex10,str(below)) is not None:
						protocol = below[1]
						portInf = below[4]
						portSup = below[5]
						if not portInf.isdigit() and not portSup.isdigit():
							portInf = socket.getservbyname(portInf,protocol)
							portSup = socket.getservbyname(portSup,protocol)
							oFile2.write(str(portInf)+"-"+str(portSup)+"/"+protocol+"\n")
						else:
							oFile2.write(portInf+"-"+portSup+"/"+protocol+"\n")
					elif re.match(serRegex11,str(below)) is not None:
						oFile2.write(below[1]+"\n")
					j = j+1
					try:
						next = lines[j+1].rstrip("\r\n")
						below = next.split(",")
					except IndexError:
						return None

				oFile2.write("\n")


	finally:
		iFile.close()
		oFile1.close()
		oFile2.close()


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
