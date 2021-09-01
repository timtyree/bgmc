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

def get_all_files_matching_pattern(file,trgt):
	"""returns a list of files in same folder as file.
	all files in list end in the string trgt.
	Example, trgt='_unwrap.csv'.
	"""
	# get all .csv files in the working directory of ^that file
	folder_name = os.path.dirname(file)
	os.chdir(folder_name)
	retval = os.listdir()#!ls
	file_name_list = list(retval)
	# check each file if it ends in .csv before merging it

	def is_trgt(file_name,trgt):
		return file_name[-len(trgt):]==trgt
	# def is_csv(file_name):
	#     return file_name[-4:]=='_unwrap.csv'
	file_name_list = [os.path.abspath(f) for f in file_name_list if is_trgt(f,trgt)]
	return file_name_list
