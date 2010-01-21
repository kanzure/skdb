""" Tech.py Tools for reading a technology tree from a csv text file or string.
Note that this expects the annoyingly statndard excel csv format with
and its testing """
#url: http://www.charlesmerriam.com/blog/2008/04/fun-with-programming-a-technology-tree/
#url: http://www.charlesmerriam.com/blog/wp-content/uploads/2008/04/techpy.txt

import csv
import StringIO
import logging
#logging.basicConfig(level=logging.DEBUG, 
#                    format="%(levelname)s:%(pathname)s:%(lineno)d:%(message)s")
logging.basicConfig(level=logging.WARNING, 
                    format="%(levelname)s:%(pathname)s:%(lineno)d:%(message)s")
from logging import debug 

def is_dict(d):
    return type(d) is dict

def is_list(l):
    return type(l) is list

def is_string(s):
    return isinstance(s, basestring)

def is_iter(i):
    return hasattr(i, "next") and hasattr(i, "__iter__")


def check_form(tech):
    """ check types, lengths, and properly trimmed strings """
    assert is_dict(tech) and len(tech) > 0
    
    for name, values in tech.iteritems():
        assert is_string(name)
        assert is_list(values) and len(values) == 5
        for i in values:
            assert is_list(i) 
            for s in i:
                assert is_string(s) and s.find(",") == -1 and s == s.strip() and len(s) > 0
            
        
def check_unique(tech):
    """ test that units, buildings, and wonders are unique """
    def simplify(s):
        """ reduce to a simple form so that close matches will conflict """
        return s.replace(' ','').replace('_','').lower()
        
    units_seen, buildings_seen, wonders_seen = set(), set(), set()
    for name, (unused_depends, units, buildings, wonders, unused_specials) in tech.iteritems():
        for u in units:
            assert simplify(u) not in units_seen, "Duplicate unit %s found in technology %s" % (u, name)
            units_seen.add(simplify(u))
        for b in buildings:
            assert simplify(b) not in buildings_seen, "Duplicate building %s found in technology %s" % (b, name)
            buildings_seen.add(simplify(b))
        for w in wonders:
            assert simplify(w) not in wonders_seen, "Duplicate wonder %s found in technology %s" % (w, name)
            wonders_seen.add(simplify(w))

def check_dependencies(tech):
    """ Tests dependencies to be sure they all exist and have no cycles.
        OK, this is a wierd version of Depth First Search, because we don't
        know the heads, there may be disjoint graphs, no cycles or multiple
        visits are allowed, and we want to cache previously checked techs. """
    
    def check_name(name):
        debug(" checking %s", name)
        if name in techs_checked:
            debug(" ->skip checked %s", name)
            return
        assert name not in techs_seen, "Cyclic dependency detected at technology %s for %s" % (name, start_name)
        techs_seen.add(name)
        for d in sorted(tech[name][0]):
            assert tech.has_key(d), "Missing dependency %s in technology %s" % (d, name)                
            check_name(d)
        techs_checked.add(name)
        
    techs_checked = set()
    for start_name in sorted(tech.iterkeys()):
        debug("starting with %s", start_name)
        techs_seen = set()
        check_name(start_name)
    
def check_redundancies(tech):
    """ check that no technology names a dependency that just depends
    on another depency. """
    def contains(inner,outer):
        if (inner,outer) in checked:
            return False
        debug("does %s contain a dependency %s?" % (inner,outer))
        
        debug(" does %s contain a dependency on %s?", inner, outer)
        if inner == outer:
            return True
        else:
            for dep in tech[inner][0]:
                if contains(dep, outer):
                    return True
            debug("   No, %s does not contain a dependency on %s", inner, outer)
            checked.add((inner,outer))
            return False
        
    checked = set()
    for start_name in sorted(tech.iterkeys()):
        debug("Checking redundancies in %s", start_name)
        deps = tech[start_name][0]
        # for all permuations of dependenices
        for this in deps:
            for that in deps:
                if this <> that:
                    debug(" checking %s contains no %s", this, that)
                    assert not contains(this, that), \
                           "Redundant dependency:  %s depends on %s which depends on %s" % (start_name, this, that)                    
            
                                
import nose.tools as nt
def fail_dependencies(tech_string):
    tech = read_tech_from_string(tech_string)
    check_form(tech)
    check_unique(tech)
    nt.assert_raises(AssertionError, check_dependencies, tech)

def fail_unique(tech_string):
    tech = read_tech_from_string(tech_string)
    check_form(tech)
    nt.assert_raises(AssertionError, check_unique, tech)

def fail_redundancies(tech_string):
    tech = read_tech_from_string(tech_string)
    check_form(tech)
    check_unique(tech)
    check_dependencies(tech)
    nt.assert_raises(AssertionError, check_redundancies, tech)

def pass_all(tech_string):
    tech = read_tech_from_string(tech_string)
    check_form(tech)
    check_unique(tech)
    check_dependencies(tech)
    check_redundancies(tech)

def test_redundant_dependency():        
    fail_redundancies("""Lots of interleaved tech with C->G->H failure
TechX,"TechK, TechC"
TechK,"TechD, TechG"
TechC,"TechE, TechF"
TechD,"TechE, TechF"
TechE
TechF,TechG
TechG,TechH
TechH""")
    fail_redundancies("""Tech A shouln't depend on tech C since B already does
TechA,"TechB,TechC"
TechB,TechC
TechC""")
    

def test_circular_dependency():
    pass_all(""" ok for diamonds for a->b,c b->d c->d
TechA,"TechB, TechC"
TechB,TechD
TechC,TechD
TechD""")
    fail_dependencies(""" Bad cycle A->B->C->A
TechA,TechB
TechB,TechC
TechC,TechA""")
    fail_dependencies(""" a->b->c->a 
"TechD"
"TechE","TechD"
"TechC","TechA",,,,"Note redundant cycle" 
"TechB","TechC,TechD"
"TechA","TechB" """)


def test_missing_dependency():
    fail_dependencies(""" No techMissing
TechA,TechMissing
TechB,TechC
TechC,TechD
TechD""")

def test_identical_names():
    fail_unique('\nATech,,"plane, plane"')
    fail_unique('\nATech,,"TheTower, the_tower"')
    fail_unique('\nATech,,"The Tower, the_tower"')
    
def test_distinct_enough():
    pass_all('\nATech,,,"Bank One, bank - one, bank:one"')
    
def test_handles_civ_file():
    tech = read_tech_from_file("civtech.csv")
    check_form(tech)
    check_unique(tech)
    check_dependencies(tech)
    check_redundancies(tech)
        
def read_tech_from_file(file_name):
    return read_tech(open(file_name, "rb"))
    
def read_tech_from_string(entire_tree):
    return read_tech(StringIO.StringIO(entire_tree))  # so does this close on gc?
    
def read_tech(file_handle):
    """ Return technology tree hash.   
    Read tech tree from a csv file, with a line of headers, then one line per 
    technology in the form of name, ...  Multiple items, like two dependencies 
    are separated inside the value.
    
    For example, here's a file with one technology that has no units or special.
        Headers On First Line, Ignore this line
        The Technology Name, "First Technology Dependency, Second Dependency", "", "A building", "The Wonder"    
    """
    tech = {}  #  where we put the technologies as a hash of name and array of [depends, units, buildings]
    
    reader = csv.reader(file_handle)
    first = True
    for row in reader:
        if first:  # skip headers in first row
            first = False
            continue
        assert len(row)>= 1 and len(row) <= 6, "Lines need to have a name and up to six total fields"
        name = row[0]
        l = len(row)
        depends, units, buildings, wonders, specials = [], [], [], [], []
        if l > 1:
            depends = [s.strip() for s in row[1].split(",") if len(s.strip()) > 0]
        if l > 2:
            units = [s.strip() for s in row[2].split(",") if len(s.strip()) > 0]
        if l > 3:
            buildings = [s.strip() for s in row[3].split(",") if len(s.strip()) > 0]
        if l > 4:
            wonders = [s.strip() for s in row[4].split(",") if len(s.strip()) > 0]
        if l > 5:
            specials = [s.strip() for s in row[5].split(",") if len(s.strip()) > 0]
        assert not tech.has_key(name), "Duplicate technology %s" % name
        tech[name] = [depends, units, buildings, wonders, specials]
        
    return tech

if __name__ == "__main__":
#    test_redundant_dependency()
    test_handles_civ_file()
