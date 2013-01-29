from Tkinter import *
import tkFont
from ansicolortext import AnsiColorText

def killme():
    root.quit()
    root.destroy()
	
root = Tk()
root.title('Multihost')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
dFont=tkFont.Font(family="Courier New", size=10)
text = AnsiColorText(root)
text.config(font=dFont)
text.pack(side=LEFT, fill=BOTH, expand = YES)
yscrollbar=Scrollbar(root, orient=VERTICAL, command=text.yview)
yscrollbar.pack(side=RIGHT, fill=Y)
text["yscrollcommand"]=yscrollbar.set


text.colored_write("Hello",1)
text.colored_write("Hello",2)
text.colored_write("Hello",3)
text.colored_write("Hello",4)
#

#lb=Text(root, width=16, height=5, font=dFont)

#lb.pack(side=LEFT, fill=BOTH, expand = YES)

root.mainloop()