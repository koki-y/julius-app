import os
import sys
import threading
import xml.etree.ElementTree as ET

import julius_conf as conf
import julius_utils as utils

def main():
	client = utils.makeConnection()

	wait_and_send_command = threading.Thread(target=wait_stdin_and_send_command, args=[client])
	try:
		# wait_and_send_command.start()
		receiving_julius_msg_and_print(client)
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
		print_xml_for_demo(xmldata) # for demo
		# print_xml(xmldata)

def perse_xml(data):
	return ET.fromstring(data)

def print_xml_for_demo(xml_data):
	if xml_data.tag == 'INPUT':
		if xml_data.attrib['STATUS'] == 'LISTEN':
			print('<<< please speak >>>')
		if xml_data.attrib['STATUS'] == 'STARTREC':
			print('Recoginition...' + os.linesep)
	if xml_data.tag == 'REJECTED':
		print('Recected :' + xml_data.attrib['REASON'] + os.linesep)
	if xml_data.tag == 'RECOGOUT':
		result = ''
		for child in xml_data:
			for mago in child:
				if (mago.attrib['PHONE'] != 'silB'
				    and mago.attrib['PHONE'] != 'silE'):
					result += mago.attrib['WORD']
		print('Sentence: ' + result + os.linesep)

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
