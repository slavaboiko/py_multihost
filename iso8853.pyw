"""

(C) Copyright 2009 Igor V. Custodio

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""


from ISO8583.ISO8583 import ISO8583
from ISO8583.ISOErrors import *
from socket import *
from datetime import datetime
import threading
import logging
from ViewDesk import *
from utils import *
import traceback

DEBUG = False

def _handler(connection, address):

	iso = ISO8583(debug=True)
	#iso = ISO8583()
	logger = logging.getLogger()
	try:
		d = ({'color':'magenta4'})
		logger.debug("Connection with %s has been established", address)
		while True:
			data = connection.recv(1024)
			if data == "":
				logger.debug("Connection has been lost")
				break
			logger.debug("Request:   %s\n%s", datetime.now().strftime("%d/%m/%y %H:%M:%S"), dump(data), extra=d)
			iso.setIsoContent(ByteToHex(data[2:]))
			v3 = iso.getBitsAndValues()
			for v in v3:
				log_bit(v, iso, logger)
			connection.sendall(data)
			logger.debug("Response:   %s\n%s", datetime.now().strftime("%d/%m/%y %H:%M:%S"), dump(data), extra=d)
	except Exception, e:
		if ( DEBUG == True ):
			logger.exception("Problem handling request")
		else:
			logger.error("%s: %s" % (e.__class__.__name__,str(e),) )
	finally:
		logger.debug("Closing socket")
		connection.close()

if __name__ == '__main__':
	FORMAT = '%(asctime)-15s %(levelname)-9s %(message)s'
	logging.basicConfig(level=logging.DEBUG, format=FORMAT)
	logger = logging.getLogger('MultiHOST')
	try:
		txtWnd = ViewDesk('MultiHOST')
		txtWnd.attach()
		from InitHolder import Server
		server = Server('0.0.0.0', 802, _handler)
		server.start()
		txtWnd.mainloop()
		server.quit()
	except:
		logger.exception("Unexpected exception")
	finally:
		logger.info("Shutting down")