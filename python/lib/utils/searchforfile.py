import tkinter as tk, os
from tkinter import filedialog

def search_for_file (currdir = os.getcwd()):
	'''use a widget dialog to selecting a file.  Increasing the default fontsize seems too involved for right now.'''
	root = tk.Tk()
	# root.config(font=("Courier", 44))
	tempdir = filedialog.askopenfilename(parent=root,
										 initialdir=currdir,
										 title="Please select a file")#,
										 # filetypes = (("all files","*.*")))
	root.destroy()
	if len(tempdir) > 0:
		print ("File: %s" % tempdir)
	return tempdir
