#!/bin/bash
echo "interactive python shell for pythonOCC and skdb/pymates"
echo ">>> pymates.start()"
echo ">>> pymates.demo()"
echo ">>> #pymates.mate_parts()"
echo ">>> pymates.show_interface_points()"
ipython -wthread -c "import pymates" -i
