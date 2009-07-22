#!/bin/bash
echo "interactive python shell for pythonOCC and skdb/pymates"
echo ">>> pymates.start()"
echo ">>> pymates.demo()"
echo ">>> #pymates.mate_parts()"
echo ">>> pymates.show_interface_points()"
echo "#also try this:"
echo ">>> pymates.transform_point(5.,5.,5.)"
echo ">>> pymates.nontransform_point(5.,5.,5.)"
ipython -wthread -c "import pymates" -i
