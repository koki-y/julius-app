import socket
import xml.etree.ElementTree as ET
import julius_conf as conf
import julius_utils as utils

def main():
	client = utils.makeConnection()
	client.close()

if __name__ == "__main__":
	main()
