"""
Terminator plugin to find git repo.

License: GPLv2
"""
from asyncio.subprocess import PIPE
import inspect, os, shlex, subprocess
from sys import stdout
from tabnanny import check
# import gtk
from terminatorlib.util import err, dbg
from terminatorlib import plugin
from terminatorlib import config

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk

AVAILABLE = ['GitPlugin']

class GitPlugin(plugin.MenuItem):
    """ Process URLs returned by commands. """
    capabilities = ['terminal_menu']

    def __init__(self):
        plugin.MenuItem.__init__(self)
        self.plugin_name = self.__class__.__name__
        self.current_path = None
        
    def callback(self, menuitems, menu, terminal):
        filepath = terminal.get_cwd()
        gitpath = filepath + '/.git/'
        #BUG si ls -l /etc/ suis encore dans home :( filepath pas bon !!
        print('here is my git folder: ' + gitpath)
        
        if os.path.exists(str(gitpath)):
            #item = gtk.MenuItem('Git Status')
            #menuitems.append(item)
            #item.connect("activate", self._execute, {'terminal' : terminal, 'command' : 'git status' })
            #dbg('Menu items git appended')
            
            item = gtk.MenuItem('Git')
            menuitems.append(item)
            submenu = gtk.Menu()
            item.set_submenu(submenu)
            
            menuitem = gtk.MenuItem('Status')
            submenu.append(menuitem)
            menuitem.connect("activate", self._execute, {'terminal' : terminal, 'command' : 'git status' })
            menuitem = gtk.SeparatorMenuItem()
            submenu.append(menuitem)
            
            # myBranche = subprocess.check_output(['git', 'symbolic-ref','HEAD', '--short']) 
            menuitem = gtk.MenuItem('Branches')
            submenu.append(menuitem)
            #menuitem.connect("activate", self._execute, {'terminal' : terminal, 'command' : 'git branch -a' })

            myBranches = subprocess.check_output(['/usr/bin/git','branch'], cwd=gitpath)
            print("Branches: " + str(myBranches.decode()))
            myBranches=myBranches.decode().split("\n")
            
            ssubmenu = gtk.Menu()
            menuitem.set_submenu(ssubmenu)

            for element in myBranches:
                if len(element)>1:
                    smenuitem = gtk.MenuItem(element)
                    ssubmenu.append(smenuitem)
                    smenuitem.connect("activate", self._execute, {'terminal' : terminal, 'command' : 'git checkout '+element.replace('* ','') })
            menuitem = gtk.SeparatorMenuItem()
            ssubmenu.append(menuitem)
            menuitem = gtk.MenuItem('List Branches')
            ssubmenu.append(menuitem)
            menuitem.connect("activate", self._execute, {'terminal' : terminal, 'command' : 'git branch -a' })
                
            menuitem = gtk.MenuItem('Logs')
            menuitem.connect("activate", self._execute, {'terminal' : terminal, 'command' : 'git log --oneline -n 6' })
            submenu.append(menuitem)
            menuitems.append(menuitem)
            
            
        else:
            print('Menu items git remove')
            
    def _execute(self, widget, data):
      command = data['command']
      if command[-1] != '\n':
        command = command + '\n'
        terminal = data['terminal']
        terminal.vte.feed_child(command.encode())

