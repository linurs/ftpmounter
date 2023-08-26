#!/usr/bin/python3

## @package ftpmounter 
# @author urs lindegger urs@linurs.org  

## @todo 
# - messagebox to show command that made message
# - gui improvement icons
# - ebuild with dependencies to curlftpfs
# - create host files

## @mainpage ftpmounter
# ftpmounter is a simple gui to mount ftp 
# 

import os
import subprocess
import shlex
import argparse
import logging
import sys

from tkinter import *   
from tkinter import messagebox   
from tkinter import filedialog    

## Version of ftpmounter
ftpmounterversion="0.0"

## favicon file to seen in window decoration
faviconname='favicon.gif'

userpath=os.path.expanduser("~")          # check what user

ftpfs="curlftpfs"
configdir=userpath+"/.ftpmounter"
pathtoconfig=configdir+"/conf"
default_hostname="default"
hostname_suffix=".conf"
default_host="ftp://pangea.stanford.edu/"
default_opts="-o utf8,allow_other"

buttonwidth=20

default_ftpmountdir=configdir+"/"+default_hostname   

class app_t():           
## Constructor    
    def __init__(self):
        if os.path.isdir(configdir)==False:  # check if user has a directory containing persistent data
          os.mkdir(configdir)                        # if not, create the directory
        logging.debug("Config file "+pathtoconfig) 
        
        ## select the host from the config file
        if os.path.isfile(pathtoconfig)==False:  # check if file exists containing persistent data
          os.system("touch "+pathtoconfig)   # if not, create the empty file
        pathtoconfigfile=open(pathtoconfig)       # now read the file containing persistent data or being empty
        ftpmounter_config=pathtoconfigfile.readlines()  
        self.hostname=default_hostname
        for i in ftpmounter_config:
            logging.debug(i) 
            t=i.split("=")
            if(t[0]=="hostname"):
               self.hostname=t[1].strip()
        pathtoconfigfile.close()
        
        ## read the hostfile
        self.pathtohostconfig=configdir+"/"+self.hostname+hostname_suffix
        if os.path.isfile(self.pathtohostconfig)==False:  # check if file exists containing persistent data
          os.system("touch "+self.pathtohostconfig)   # if not, create the empty file
        pathtohostfile=open(self.pathtohostconfig)         # now read the file containing persistent data or being empty
        self.read_hostconfig(pathtohostfile)
        pathtoconfigfile.close()
        
        ## flag to check if ftpfs is mounted
        self.mountflag=0

        ## setup the gui stuff
        self.window=Tk()
        self.window.title('ftpmounter')
        
        # add an icon
        img = PhotoImage(file=favicon)
        self.window.call("wm", "iconphoto", self.window, "-default", img)

        ## create the menus   
        self.menubar = Menu(self.window)
        
        filemenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Exit", command=self.quit)
        
        optionsmenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Options", menu=optionsmenu)
        
        optionsmenu.add_command(label="Change Host", command=self.changehost)
        optionsmenu.add_command(label="Edit ftp configuration", command=self.edit_config)
        
        self.menubar.add_command(label="About", command=self.about)
      
        self.window.config(menu=self.menubar)
       
        self.host_gui=StringVar()
        self.host_gui.set(self.hostname)
        self.window.pathlabel = Label(master=self.window, textvariable=self.host_gui)
        self.window.pathlabel.pack()
       
       # set up and register the buttons
        self.window.mountbutton=Button(master=self.window,text='Mount',width=buttonwidth, command=self.mount)
        self.window.mountbutton.pack()
        self.window.unmountbutton=Button(master=self.window,text='UnMount',width=buttonwidth, relief=SUNKEN, command=self.unmount)
        self.window.unmountbutton.pack()
        self.window.openbutton=Button(master=self.window,text='Open',width=buttonwidth, relief=SUNKEN, command=self.open)
        self.window.openbutton.pack()
        
        self.dir_gui=StringVar()
        self.dir_gui.set(self.ftpmountdir)
        self.window.dirlabel = Label(master=self.window, textvariable=self.dir_gui)
        self.window.dirlabel.pack()

        self.window.mainloop()      

##
# mounts
    def open(self):
        if self.mountflag==1:
          cmd="xdg-open "+self.ftpmountdir
          os.system(cmd)

##
# edit config
    def edit_config(self):
          cmd="xdg-open "+self.pathtohostconfig
          os.system(cmd)

##
# mounts
    def mount(self):
        if (self.mountflag==0):
            if os.path.isdir(self.ftpmountdir)==False:  # check if user has it
              os.mkdir(self.ftpmountdir)                        # if not, create the directory
            cmd=ftpfs+" "+self.ftphost+" "+self.ftpmountdir+" "+self.ftpopts
            args=shlex.split(cmd)
            try:
                p = subprocess.Popen(args, 
                  stdin=subprocess.PIPE, 
                 stdout=subprocess.PIPE,
                 stderr=subprocess.STDOUT, # standard err are passed to stdout
                 ) # open new process
                stdout_value, stderr_value = p.communicate()# communicate is a one time action, afterwards p is closed
                if (stdout_value==b''):
                   messagebox.showinfo("mount","Successfully mounted")
                   self.mountflag=1
                   self.window.unmountbutton.config(relief=RAISED)
                   self.window.openbutton.config(relief=RAISED)
                   self.window.mountbutton.config(relief=SUNKEN)
                else:  
                   messagebox.showinfo("mount",stdout_value)
            except:       
                 messagebox.showerror("mount","Error mounting with "+self.mtpfs.get())
        
##
# unmounts
    def unmount(self):
        cmd ="fusermount -u "+self.ftpmountdir
        args=shlex.split(cmd)
        p = subprocess.Popen(args, 
                      stdin=subprocess.PIPE, 
                      stdout=subprocess.PIPE,
                      stderr=subprocess.STDOUT, # standard err are passed to stdout
        ) # open new process
        stdout_value, stderr_value = p.communicate()# communicate is a one time action, afterwards p is closed
        if (stdout_value==b''):
           messagebox.showinfo("unmount","Successfully umounted")
           self.mountflag=0
           self.window.unmountbutton.config(relief=SUNKEN)
           self.window.openbutton.config(relief=SUNKEN)
           self.window.mountbutton.config(relief=RAISED)
        else:  
           messagebox.showinfo("unmount",stdout_value)

    def read_hostconfig(self, fileobject):
        ftpmounter_config=fileobject.readlines()  
        self.ftpmountdir=default_ftpmountdir
        self.ftphost=default_host
        self.ftpopts=default_opts
        for i in ftpmounter_config:
            logging.debug(i) 
            t=i.split("=")
            if(t[0]=="ftpmountdir"):
                self.ftpmountdir=t[1].strip()
            if(t[0]=="ftphost"):
                self.ftphost=t[1].strip()
            if(t[0]=="ftpopts"):
                if(len(t)==2):
                   self.ftpopts=t[1].strip() 
                else:
                   self.ftpopts=t[1].strip()+"="+t[2].strip()    

    def changehost(self):
      if(self.mountflag==0):
          newhost=filedialog.askopenfile(initialdir =configdir, filetypes = (("conf files","*.conf"),("all files","*")))
          if(newhost!=None) :    
              self.pathtohostconfig=newhost.name
              name_split=self.pathtohostconfig.split("/")
              name_split_more=name_split[len(name_split)-1].split(".")
              self.host_gui.set(name_split_more[0])
              self.read_hostconfig(newhost)
              self.dir_gui.set(self.ftpmountdir)
              newhost.close() 
      else:
       messagebox.showinfo("Info","Unmount first")
    
      
# updates the config file by re-creating it
    def updateconfig(self):
        configfilename=pathtoconfig
        pathtoconfigfile=open(configfilename,  'w')
        pathtoconfigfile.write("hostname="+self.host_gui.get()+"\n")  
        pathtoconfigfile.close()
        
        configfilename=configdir+"/"+self.host_gui.get()+hostname_suffix
        pathtoconfigfile=open(configfilename,  'w')
        pathtoconfigfile.write("ftpmountdir="+self.ftpmountdir+"\n")  
        pathtoconfigfile.write("ftphost="+self.ftphost+"\n")  
        pathtoconfigfile.write("ftpopts="+self.ftpopts+"\n")  
        pathtoconfigfile.close()
##
# Quits the application
    def quit(self):
           if(self.mountflag==1):
                messagebox.showwarning("Warning","Ftp server is still mounted")
           self.updateconfig()
           self.window.destroy()

##
# Shows abbout messagebox
    def about(self):
         messagebox.showinfo("About","ftpmounter a mounter for mtp from https://www.linurs.org \nVersion "+ftpmounterversion)

if __name__ == "__main__":
    ## manage the command line parameters
    # sets default values to variables and modifies their content according the command line parameter passed
    # additionally it handles the -h and --help command line parameter automatically
    parser = argparse.ArgumentParser(
                                     description='ftpmounter - Mount ftp servers to the local file system',
                                     epilog='urs@linurs.org')
    ## command line option to show the programs version
    parser.add_argument('-v', '--version', action='version', \
    ## version used in command line option to show the programs version
    version='%(prog)s '+ftpmounterversion)
    ## command line option to enable debug messages
    parser.add_argument('-d', '--debug',   help="print debug messages",   action='store_true')  

    ## the command line arguments passed
    args = parser.parse_args()      
    
    # Configuring the logger. Levels are DEBUG, INFO, WARNING, ERROR and CRITICAL
    # the parameter filename='example.log' would write it into a file
    logging.basicConfig() # init logging 
    ## The root logger 
    logger = logging.getLogger() 
    if args.debug==True:
        logger.setLevel(logging.DEBUG)    # the level producing debug messages
    else:    
        logger.setLevel(logging.WARNING)
    logger.debug('Logging debug messages')
    
    ## pyinstaller stuff required to create bundled versions:      
    frozen = 'not '
    if getattr(sys, 'frozen', False): # pyinstaller adds the name frozen to sys 
            frozen = ''  # we are running in a bundle (frozen)
            ## temporary folder of pyinstaller
            bundle_dir = sys._MEIPASS  
    else:
            bundle_dir = os.path.dirname(os.path.abspath(__file__))   # we are running in a normal Python environment 
   
    logging.debug('Script is '+frozen+'frozen')
    logging.debug('Bundle dir is '+bundle_dir )
    logging.debug('sys.argv[0] is '+sys.argv[0] )
    logging.debug('sys.executable is '+sys.executable )
    logging.debug('os.getcwd is '+os.getcwd() )

    ## makes that the files are found
    favicon=bundle_dir+os.sep+faviconname    
    if (os. path. isfile(favicon)==False):
        logging.debug(favicon+' not found' )
        favicon="/usr/share/ftpmounter/"+faviconname
        logging.debug('so try to find it at '+favicon )

        if (os. path. isfile(favicon)==False):
             logging.error(faviconname+' not found')
             exit()

    ## start the application
    app=app_t()
