#!/usr/bin/python
import skdb
from skdb import settings, Mate
import os

#load a screw
screw_package = skdb.load_package("screw")
screws = screw_package.load(open(os.path.join(settings.package_path("screw"),"data.yaml")),only_classes="<class 'screw.Screw'>") #load from "data.yaml"
#print out your screws if you want
for screw in screws:
    assert screw.makes_sense() == True, "the screw must make sense" #the data sucked

#load a bearing
#the bearing package at the moment is a dummy package and isn't really important
bearing_pack = skdb.load_package("bearing")
stuff = open(os.path.join(settings.package_path("bearing"),"data.yaml"))
bearings = bearing_pack.load(stuff, only_classes="<class 'bearing.Bearing'>") #how can this be simplified?
for bearing in bearings:
    assert bearing.makes_sense() == True, "the bearing must make sense" #the data sucked

def visualize_and_pause(result):
    '''visualize the object and then wait for user input'''
    raw_input("visualize and pass?")
    assert False, "not implemented"
    return

#this is actually a dummy object (a dummy process)
class Press_Fit(skdb.Process):
    '''a technique to fit two things together'''
    def options(self, parts1, parts2):
        '''we're assuming that it's only a matter of whether or not two interfaces are compatible'''
        return_list = []
        for part1 in parts1:
            for part2 in parts2:
                if not part2 == part1: #unless it's really flexible
                    #FIXME: for some reason the screws and bearings have no interfaces??
                    for interface1 in part1.interfaces:
                        for interface2 in part2.interfaces:
                            if interface1.compatible(interface2) and interface2.compatible(interface1):
                                return_list.append(Mate(interface1, interface2))
        return return_list
    def feasibility(self, option):
        '''ridiculously simple feasibility test on a possible set of starting conditions for this technique'''
        if option.makes_sense(): return 1
        else: return 0 

#until we can load up a process..
press_fit = Press_Fit("press fit process") #skdb.load(press_fit_yaml)
#press_fit_machine = skdb.load("press_fit_machine").Machine()

#figure out all possible options (and apply and look at the good ones)
good_list = []
for option in press_fit.options(screws, bearings):
    #different screws in different bearings can be used for different scenarios.
    #let's see how this option fares with electron beaming
    score = press_fit.feasibility(option)
    option.score = score
    if score >= .84: #if score >= press_fit.recommended_minimum_feasibility
        print "good option: ", option
        result = option.apply() #return a copy of what the parts would be like if they were actually mated
        good_list.append(result)

#show each result to the user and wait for input to go to the next one
for result in good_list:
    visualize_and_pause(result)

exit()
#everything below is old and doesn't necessarily work


#now let's say we have a particular screw in mind that we want to setup
screw = screw_package.Screw()
screw.setup(length="4mm")
#not sure about the skdb.options method
possibilities2 = skdb.options(screw, bearings) #or (bearings, screw)
#print out the possibilities that have a certain score
for option in possibilities2:
    #score the option somehow
    if option.score >= .8:
        print option

#is an assembly made up of multiple <skdb.options()>? or a Mate.apply()'d?
assembly = skdb.Assembly()
assembly += possible1 #add a particular possibility

#load a lego
lego_pack = skdb.load_package("lego")
legos = lego_pack.load()
for lego in legos:
    assert lego.makes_sense() == True, "the lego must make sense" #the data sucked

#make a lego that we have in mind and want to setup
block = lego_pack.Lego()
block.setup(num_holes=4,num_pegs=16)
#figure out what it can connect to
possible_connections = skdb.options(block, legos)

#the following may be silly
#make sure all of these legos are at least once compatible
for lego1 in legos:
    for lego2 in legos:
        assert len(skdb.options(lego1,lego2)) > 0, "all legos must at least be compatible once with all other legos"

