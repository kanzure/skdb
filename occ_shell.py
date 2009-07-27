#!/usr/bin/python
#occ_shell.py: display a simple GUI that doesn't take over your python session
#
#how to get an interactive interpreter with pythonOCC running:
#ipython -wthread -c "import occ_shell as shell" -i
#
#>>>shell.start()
#how to get something you have clicked on:
#>>>my_shape = shell.selected()

import OCC.Display.wxSamplesGui

if __name__ == '__main__':
    OCC.Display.wxSamplesGui.start_display()

def start():
    OCC.Display.wxSamplesGui.display.Create()
def selected():
    return OCC.Display.wxSamplesGui.display.Context.SelectedShape()
