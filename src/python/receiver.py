import os
import xml.etree.ElementTree as ET
import julius_conf as conf
import julius_utils as utils

opsQueue = []
receiving = False

def main():
	client = utils.makeConnection()
	try:
		data = ''
		while 1:
			if opsQueue:
				if not receiving:
					ops = opsQueue.pop()
					print('#### send message.')
					message = ops.encode('utf-8')
					client.send(message)
					receiving = True
			else:
				data += str(client.recv(1024).decode('utf-8'))
				if conf.escapeChar in data:
					splitedDot = data.split(conf.escapeChar)
					processOnReceive(splitedDot[0:-1])
					data = ''.join(splitedDot[-1:])
					receiving = False
	except KeyboardInterrupt:
		client.close()

def processOnReceive(datas):
	for data in datas:
		xmldata = perse_xml(remove_gabage(data))
		print_xml(xmldata)

		# command送信テスト部分 (状態が整ったらQueueに置く)
		if xmldata.tag == 'INPUT':
			if xmldata.attrib['STATUS'] == 'LISTEN':
				print('#### is INPUT.LISTEN')
				opsQueue.append('STATUS' + os.linesep)
				# opsQueue.append('VERSION' + os.linesep)
				# opsQueue.append('GRAMINFO' + os.linesep)
				# 以下のコマンドはパースエラーが出る
				# opsQueue.append('LISTPROCESS' + os.linesep)

def perse_xml(data):
	return ET.fromstring(data)

def print_xml(xml_data):
	print(xml_data.tag, xml_data.attrib)
	for child in xml_data:
		print('  ', child.tag, child.attrib)
		for mago in child:
			print('    ', mago.tag, mago.attrib)
	print()

def remove_gabage(data):
	for gabage in conf.gabages:
		if gabage in data:
			data = data.replace(gabage, '')
	return data
	

if __name__ == "__main__":
	main()
