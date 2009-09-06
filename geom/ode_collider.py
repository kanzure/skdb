#!/usr/bin/python
#http://pyode.sourceforge.net/tutorials/tutorial3.html
#collision detection with pyODE
import ode, random
from math import *

# create_box
def create_box(name, world, space, density, lx, ly, lz):
    """Create a box body and its corresponding geom."""

    # Create body
    body = ode.Body(world)
    M = ode.Mass()
    M.setBox(density, lx, ly, lz) 
    body.setMass(M)

    # Set parameters for drawing the body
    body.shape = "box"
    body.boxsize = (lx, ly, lz) 

    # Create a box geom for collision detection
    geom = ode.GeomBox(space, lengths=body.boxsize)
    geom.setBody(body)

    geom.name = name
    body.name = name
    return body

# drop_object
def drop_object():
    """Drop an object into the scene."""

    global bodies, counter, objcount

    body = create_box("box #%s" % (objcount), world, space, 1000, 1.0,0.2,0.2)
    body.setPosition( (random.gauss(0,0.1),3.0,random.gauss(0,0.1)) )
    theta = random.uniform(0,2*pi)
    ct = cos (theta)
    st = sin (theta)
    body.setRotation([ct, 0., -st, 0., 1., 0., st, 0., ct])
    bodies.append(body)
    counter=0
    objcount+=1
    return body

# Collision callback
def near_callback(args, geom1, geom2):
    """Callback function for the collide() method.

    This function checks if the given geoms do collide and
    creates contact joints if they do.

    for two colliding blocks there should be four "contacts", w
    """

    # Check if the objects do collide
    contacts = ode.collide(geom1, geom2)
    #print "contacts = ", contacts
    # Create contact joints
    world,contactgroup = args
    for c in contacts:
        body1 = geom1.getBody()
        body2 = geom2.getBody()
        if not body1 is None and not body2 is None:
            print "collision between %s and %s" % (body1.name, body2.name)
        (position, normal, depth, geom1, geom2) = c.getContactGeomParams()
        print ".. and position = ", position
        restitution = c.getBounce()
        print ".. and restitituion = ", restitution
    
    #if len(contacts) > 0:
        #there was definitely a collision


def configure_world(erp=0.8, cfm=1E-5, gravity=(0,0,0)):
    '''returns a pyODE world object
    gravity should be a triple'''
    world = ode.World()
    world.setGravity(gravity)
    world.setERP(erp)
    world.setCFM(cfm)
    return world

world = configure_world()
space = ode.Space()
floor = ode.GeomPlane(space, (0,1,0), 0)
contactgroup = ode.JointGroup()

objcount = 0
bodies = []
fps = 50
dt = 1.0/fps
dt = dt/2

#start simulation
body1 = drop_object()
world.step(100)
body2 = drop_object()
#body2.addForce((0, -2, 0)) #when you uncomment this line the bodies no longer have names? (see the attribute error)
world.step(10)

space.collide((world,contactgroup), near_callback)
contactgroup.empty()


