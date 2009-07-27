#!/usr/bin/env python
# coding: utf-8
#
#       Tangible Bit text mode client
#       by Smári McCarthy <smari@fabfolk.com>
#
# TODO:
#    Cache settings for some period between executions if running standalone
#    See TODO lists in functions.
#
import sys
import os
import xmlrpclib
import ConfigParser

configfiles = ["tbdefaults.conf", "~/.tangiblebit/tb.conf"]
settings = ConfigParser.ConfigParser()

def LoadSettings():
        # Load settings. RFC 822.
        cfgs = []
        for cfg in configfiles:
                cfgs.append(os.path.abspath(os.path.expanduser(cfg)))
                
        settings.read(cfgs)

def Connection():
        # TODO:
        #   if username and password are set in settings, use the Authenticated XMLRPC module...
        #   if settings["ssl"] == True, use the SSL interface
        return xmlrpclib.Server(settings.get("server", "xmlrpcpath"))

def Help(args):
        print("tb-get - Tangible Bit text mode client")
        print("------------------------------------------------------")
        print("help               - get help")
        print("fetch              - download object definition")
        print("sites              - get a list of sites")
        print("materials          - get a list of properties")
        print("order              - put in an order for an object")
        print("login              - log in to Tangible Bit server")

def Login(args):
        if len(args) < 2:
                print("Provide a username and password to log in.")
                print("You can also specify these in the config file (%s) to log in automagically" % settings["configfile"])
                return False
        settings.set("server", "username", args[0])
        settings.set("server", "password", args[1])

def LoggedIn():
        # TODO: Perhaps this should check if they're actually valid?
        return settings.has_option("server", "username") and settings.has_option("server", "password")

def Fetch(args):
        # TODO: Fetching functionality...
        #   - GetObject not implemented on the XMLRPC
        #   - objects recieved need to be unpacked and put into a folder with appropriate files
        conn = Connection()
        objectname = args[0]
        object = conn.GetObject(objectname)

def Sites(args):
        # TODO: Search functions that make sense for looking up sites
        #  - Get a list of sites
        #  - Get details for a certain site
        #  - Get sites within a certain radius of a certain location
        #  - What orders are currently being processed at a site
        #  - What is the access model of a certain site
        #  - What sites are within a certain region
        pass

def Materials(args):
        # TODO: Search functions that make sense for looking up materials
        #  - which materials fulfil a certain set of properties
        #  - which objects use a certain material
        #  - which materials are available within a certain radius of a certain location
        #  - which materials are available within a certain region
        #  - which materials exist in a certain inventory
        #  - compare two or more materials
        pass

def Order(args):
        # TODO: Appropriate ordering functions
        #  - Place order (interactive?)
        #  - Set shipping destination
        #  - Change where to order from (only possible if order hasn't been processed)
        #  - Compare object prices between sites (if applicable)
        if not LoggedIn():
                print("E: You must log in to place orders.")
                return False

        pass




LoadSettings()

if __name__ == "__main__":
        if len(sys.argv) < 2:
                action = "help"
        else:
                action = sys.argv[1]
        
        if action == "help":            Help(sys.argv[2:])
        elif action == "fetch":         Fetch(sys.argv[2:])
        elif action == "login":         Login(sys.argv[2:])
        elif action == "sites":         Sites(sys.argv[2:])
        elif action == "materials":     Materials(sys.argv[2:])
        elif action == "order":         Order(sys.argv[2:])
        else:
                print("E: Unknown action. Try 'help'.")
