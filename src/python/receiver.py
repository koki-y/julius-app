import os
import sys
import threading
import xml.etree.ElementTree as ET
import julius_conf as conf
import julius_utils as utils

def main():
	client = utils.makeConnection()

	receive_and_print = threading.Thread(target=receiving_julius_msg_and_print, args=[client])
	try:
		receive_and_print.start()
		wait_stdin_and_send_command(client)
	except KeyboardInterrupt:
		client.close()

def wait_stdin_and_send_command(client):
	while True:
		message = input()
		message = message.upper()
		print('[PROC_MSG] SND: "'+ message + '"')
		message += os.linesep
		client.send(message.encode('utf-8'))

def receiving_julius_msg_and_print(client):
	data = ''
	while True:
		data += str(client.recv(1024).decode('utf-8'))
		if conf.escapeChar in data:
			splitedDot = data.split(conf.escapeChar)
			onReceiveMessage(splitedDot[0:-1])
			data = ''.join(splitedDot[-1:])
	
def onReceiveMessage(datas):
	for data in datas:
		xmldata = perse_xml(remove_gabage(data))
		print_xml(xmldata)

def perse_xml(data):
	return ET.fromstring(data)

def print_xml(xml_data):
	print('> ', xml_data.tag, xml_data.attrib)
	for child in xml_data:
		print('>   ', child.tag, child.attrib)
		for mago in child:
			print('>     ', mago.tag, mago.attrib)

def remove_gabage(data):
	for gabage in conf.gabages:
		if gabage in data:
			data = data.replace(gabage, '')
	return data
	
def checkPython3():
	if sys.version_info[0] < 3:
		raise Exception('Must be using Python3.')

if __name__ == "__main__":
	checkPython3()
	main()
