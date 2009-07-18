#!/usr/bin/python
#ipython -wthread -c "import shell" -i
#shell.start()
import OCC.Display.wxSamplesGui

if __name__ == '__main__':
    OCC.Display.wxSamplesGui.start_display()

def start():
    OCC.Display.wxSamplesGui.display.Create()
