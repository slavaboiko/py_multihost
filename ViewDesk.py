from mtTkinter import *
from threading import *
import tkFont
import ttk
import logging
from ansicolortext import AnsiColorText

global _viewdesk
_viewdesk = None

def _color_by_level(level):
	return {
		'ERROR': 'Red',
		'WARNING' : 'Orange',
		'DEBUG' : 'gray55',
		'INFO': 'Blue'
	}.get(level, 'Black')

class ViewDeskHandler(logging.Handler):
	def __init__(self, viewdesk):
		""" Create handler """
		logging.Handler.__init__(self)
		self.desk = viewdesk

	def emit(self, record):
		""" Process a log message """
		try:
			color = record.color
		except:
			color = _color_by_level(record.levelname)
		self.desk.write(self.format(record), color)
		
class ViewDesk(Tk):
	def __init__(self, name):
		Tk.__init__(self)
		global _viewdesk
		
		if not _viewdesk:
			_viewdesk = self
		else:
			raise RuntimeError('Its a singleton object. First time use ViewDesk(title) then get_desk()')
			
		self.h = ViewDeskHandler(self)
		self.known_tags = set([])
		self.protocol("WM_DELETE_WINDOW", self.callback)
		self.name = name
		self.title(name)
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		dFont=tkFont.Font(family="Courier New", size=10)
		self.text = Text(self)
		self.text.config(font=dFont)
		self.text.pack(side=LEFT, fill=BOTH, expand = YES)
		yscrollbar=ttk.Scrollbar(self, orient=VERTICAL, command=self.text.yview)
		yscrollbar.pack(side=RIGHT, fill=Y)
		self.text["yscrollcommand"]=yscrollbar.set
		self.write(name, 'grey50')
	def callback(self):
		self.quit()
	def write(self, txt, color='Black'):
		txt += '\n'
		self.text.tag = self._gettag(color)
		self.text.insert(END,txt,self.text.tag)
		self.text.see(END)
	def _gettag(self,color):
		if color not in self.known_tags:
			self.text.tag_config(color, foreground=color)
			self.known_tags.add(color)
		return color
	def attach(self,logger=logging.getLogger()):
		""" Attach handler to the logging system """
		logger.addHandler(self.h)
	def detach(self,logger=logging.getLogger()):
		""" Detach logger from the logging system """
		logger.removeHandler(self.h)

def get_desk():
	if not _viewdesk:
		raise RuntimeError('Call constructor first!')
	return _viewdesk