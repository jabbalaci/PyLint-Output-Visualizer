#!/usr/bin/env python

"""
pylov.py (PyLint Output Visualizer)

Show the output of PyLint in a window. The report can be refreshed 
by pressing 'r', 'u', or F5.

This way you can switch easily between your favorite text editor and
the PyLint report. If you add or remove some lines in the source,
the line numbers indicated in the report become invalid. No problem,
you can refresh the report with a single key press.

TODO: when the main window is resized, the html panel should follow it.
"""

import wx
import wx.html
import os
import sys
import shlex

from subprocess import Popen, PIPE

VERSION = "0.1.1"

# location of pylint
PYLINT = '/usr/local/bin/pylint'
# size of the window
WIDTH, HEIGHT = 1024, 768

def execute_command(command):
    """Execute an external command and return its output."""
    args = shlex.split(command)
    return Popen(args, stdout=PIPE).communicate()[0]
    
class MyHtmlPanel(wx.Panel):
    """The PyLint report is shown in this panel."""
    
    def __init__(self, parent, id, parameters):
        """Constructor."""
        wx.Panel.__init__(self, parent, id)
        self.parent = parent
        self.parameters = parameters
        self.html1 = wx.html.HtmlWindow(self, id, pos=(0, 30), 
                                        size=(WIDTH-10, HEIGHT-60))
                                        
        self.html1.Bind(wx.EVT_KEY_DOWN, self.key_down)

        self.OnRefreshPage(None)
        
        self.btn1 = wx.Button(self, -1, "Refresh", pos=(0, 0))
        self.btn1.Bind(wx.EVT_BUTTON, self.OnRefreshPage)

        self.btn2 = wx.Button(self, -1, "Quit", pos=(110, 0))
        self.btn2.Bind(wx.EVT_BUTTON, self.OnQuit)
        
    def OnRefreshPage(self, event):
        """Relaunch pylint and show the new output."""
        rcfile_arg = ""
        rcfile = os.path.expanduser('~') + '/' + '.pylintrc'
        if os.path.isfile(rcfile):
            rcfile_arg = "--rcfile=%s" % rcfile
        command = "%s %s -f html %s" % (PYLINT, self.parameters[0], rcfile_arg)
        print "# command: %s" % command
        output = execute_command(command)
        self.html1.SetPage(output)
        self.html1.SetFocus()

    def key_down(self, event):
        """Key bindings."""
        # key codes: http://www.wxpython.org/docs/api/wx.KeyEvent-class.html
        key = event.GetKeyCode()
        key_func = { ord('R'):  self.OnRefreshPage,
                     ord('U'):  self.OnRefreshPage,
                     wx.WXK_F5: self.OnRefreshPage }
        if key in key_func:
            key_func[key](event)
        else:
            event.Skip()

    def OnQuit(self, event):
        """Quit the application."""
        self.parent.Destroy()
        
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "Jabba's PyLint Output Viewer %s" % VERSION
        print "Usage: %s <source.py>" % sys.argv[0]
        sys.exit(-1)
    # else
    if os.path.isfile(sys.argv[1]) is False:
        print "Error: %s: the specified file does not exist." % sys.argv[0]
        sys.exit(-2)
    # else
    app = wx.PySimpleApp()
    frame = wx.Frame(None, -1, "Jabba's PyLint Output Viewer %s" % VERSION, 
                     size=(WIDTH, HEIGHT))
    MyHtmlPanel(frame, -1, sys.argv[1:])
    frame.Show(True)
    app.MainLoop()
