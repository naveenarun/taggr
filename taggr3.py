import tkinter, tkinter.filedialog
from tkinter import ttk
import os

class TkFileDialogExample(tkinter.Frame):

  def __init__(self, root):

    self.mydir = ''
    tkinter.Frame.__init__(self, root)

    # options for buttons
    button_opt = {'padx': 5, 'pady': 5}

    # define buttons
    self.myTitle = tkinter.Label(self,text="Taggr: Photo Tagging with Artificial Intelligence",font=("Arial",30))
    self.myTitle.pack()
    self.dirselect = tkinter.Button(self, text='Select a directory', command=self.askdirectory, width="20")
    self.dirselect.pack(**button_opt)
    self.status = tkinter.Label(self,text="Current directory: None selected.")
    self.status.pack()
    self.startbutton = tkinter.Button(self, text="Start", command=self.start)
    self.progress = ttk.Progressbar(self, orient="horizontal", length=500,mode="determinate")
    self.progresstext = tkinter.Label(self,text="Progress: Not started yet.")
    self.progress["maximum"] = 100
    self.progress.pack()
    self.progresstext.pack()
    self.startbutton.pack()

    # This is only available on the Macintosh, and only when Navigation Services are installed.
    #options['message'] = 'message'

    # if you use the multiple file version of the module functions this option is set automatically.
    #options['multiple'] = 1

    # defining options for opening a directory
    self.dir_opt = options = {}
    options['initialdir'] = '~/Github/hacktech_2017/Sample Pics'
    options['mustexist'] = False
    options['parent'] = root
    options['title'] = 'Choose a Folder'

  def askdirectory(self):

    """Returns a selected directoryname."""
    self.mydir = tkinter.filedialog.askdirectory(**self.dir_opt)
    self.status["text"] = "Current directory: " + self.mydir
    root.update_idletasks()

  def start(self):
    picture_paths = [os.path.join(dirpath, f) for dirpath, dirnames, files in os.walk(self.mydir) for f in files if max([f.endswith(i) for i in ('.jpeg','.jpg','.png', '.gif', '.bmp')])]
    if len(picture_paths) == 0:
    	return
    numpics = len(picture_paths)
    numcomplete = 0
    self.progresstext["text"] = "Progress: %s of %s pictures tagged." % (numcomplete, numpics)
    self.dirselect["state"] = "disabled"
    self.startbutton["state"] = "disabled"
    root.update_idletasks()
    for i in picture_paths:
        root.update_idletasks()
        numcomplete += 1
        os.system('python ' + os.getcwd() + '/taggr_api_request.py ' + '\'' + i + '\'')
        self.progresstext["text"] = "Progress: %s of %s pictures tagged." % (numcomplete, numpics)
        self.progress["value"] = float(numcomplete)/float(numpics)*100.0
        root.update_idletasks()

if __name__=='__main__':
  root = tkinter.Tk()
  root.wm_title("Taggr: Photo Tagging with Artificial Intelligence")
  TkFileDialogExample(root).pack(padx=50,pady=50)
  root.mainloop()
