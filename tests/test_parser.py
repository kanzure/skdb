#!/usr/bin/python
from pyparsing import Word, alphas, operatorPrecedence, opAssoc, ParseException
from skdb import Package
import unittest
import functools

#thank you paul mcguire
#http://pyparsing.wikispaces.com/file/view/simpleBool.py

def check_package(package_name=None, data=None):
    if package_name == "True": return True
    elif package_name == "False": return False
    elif package_name == None: return False
    if data == None: raise ValueError, "check_package: data not given?"
    for package in data:
        if package.name == package_name:
            return True
    return False

class BoolOperand(object):
    def __init__(self,t):
        self.args = t[0][0::2]
        #self.vars = []
    def __str__(self):
        sep = " %s " % self.reprsymbol
        return "(" + sep.join(map(str,self.args)) + ")"
    @staticmethod
    def check_package(token):
        token = token[0]
        result = check_package(package_name=token, data=BoolOperand.vars)
        return result
    def check(self, name):
        if isinstance(name, bool): return name
        for package in self.vars:
            if package.name == name:
                return True
        return False

class BoolAnd(BoolOperand):
    reprsymbol = '&'
    def __nonzero__(self):
        for a in self.args:
            if a=="True": v = True
            elif a=="False": v = False
            elif isinstance(a,basestring):
                v = self.check(a)
            elif isinstance(a, bool):
                v = a
            elif isinstance(a, BoolOperand):
                v = a.__nonzero__()
            else: #you shouldn't get here
                v = self.check(a)
            if not v:
                return False
        return True

class BoolHave(BoolOperand):
    reprsymbol = 'have'
    def __init__(self,t):
        self.arg = t[0][1]
    def __str__(self):
        return "have " + str(self.arg)
    def __nonzero__(self):
        if isinstance(self.arg, basestring):
            v = self.check(self.arg)
            return v
        elif isinstance(self.arg, bool):
            return self.arg
        elif isinstance(a, BoolOperand):
            v = a.__nonzero__()
        else: return True

class BoolOr(BoolOperand):
    reprsymbol = '|'
    def __nonzero__(self):
        for a in self.args:
            if isinstance(a,basestring):
                v = self.check(a)
            elif isinstance(a, BoolOperand):
                v = a.__nonzero__()
            else:
                v = self.check(a)
            if v:
                return True
        return False

class BoolNot(BoolOperand):
    def __init__(self,t):
        self.arg = t[0][1]
    def __str__(self):
        return "~" + str(self.arg)
    def __nonzero__(self):
        if isinstance(self.arg,basestring):
            v = self.check(self.arg)
        elif isinstance(a, BoolOperand):
            v = a.__nonzero__()
        elif isinstance(self.arg, bool):
            return not self.arg
        else:
            v = self.check(self.arg)
        return not v

digits = "0123456789"
specials = "-_.+"
boolOperand = Word(alphas + digits + specials)
packageRef = boolOperand

boolExpr = operatorPrecedence( packageRef,
    [
    ("not", 1, opAssoc.RIGHT, BoolNot),
    ("have", 1, opAssoc.RIGHT, BoolHave),
    ("or",  2, opAssoc.LEFT,  BoolOr),
    ("and", 2, opAssoc.LEFT,  BoolAnd),
    ])

def parse(query, data=[]):
    BoolOperand.vars = data
    packageRef.setParseAction(BoolOperand.check_package)
    result = boolExpr.parseString(query, parseAll=True)
    return bool(result[0])

def parse2(query, data=[]):
    '''is exactly like parse() except it returns the result of the parsing (not the bool)'''
    BoolOperand.vars = data
    packageRef.setParseAction(BoolOperand.check_package)
    result = boolExpr.parseString(query, parseAll=True)
    #print "query: ", query
    #print "result: ", result
    #print "bool(result): ", bool(result[0])
    return result[0]

class TestParser(unittest.TestCase):
    def test_basic(self):
        packages = [Package("foo123"), Package("bar123"), Package("narf"), Package("foo123foo")]

        query_0 = "have foo123"
        self.assertTrue(parse(query_0, data=packages))

        query0 = "have foo1234"
        self.assertFalse(parse(query0, data=packages))
        
        query1 = "have foo123"
        self.assertTrue(parse(query1, data=packages))

        query2 = "foo123 and bar123"
        self.assertTrue(parse(query2, data=packages))

        query3 = "foo123 and bar123 and narf"
        self.assertTrue(parse(query3, data=packages))

        queryG = "narrrrf139401"
        self.assertFalse(parse(queryG, data=packages))

        query4 = "foo123 and nxarf123"
        self.assertFalse(parse(query4, data=packages))

        query5 = "foo123"
        self.assertFalse(parse2(query5, data=packages)==query5)
        self.assertTrue(parse(query5, data=packages))

        query6 = "foo1234"
        self.assertFalse(parse2(query6, data=packages)==query6)
        self.assertFalse(parse(query6, data=packages))

        query7 = "foo123foo"
        self.assertTrue(parse(query7, data=packages))

        query8 = "foo123foo1234"
        self.assertFalse(parse(query8, data=packages))

    def test_specials(self): #special characters like ._-
        packages=[]

        query9 = "bioperl-run"
        parse(query9, data=packages)
        
        query10 = "bioperl-1.0"
        parse(query10, data=packages)

        query_under = "some_package_name"
        parse(query_under, data=packages)
    
    def test_compound_statements(self):
        query1 = "True and True"
        self.assertTrue(parse2(query1))

    def test_errors(self):
        query1 = "and foo123"
        self.assertRaises(ParseException, parse, query1)

        query2 = "foo123 and"
        self.assertRaises(ParseException, parse, query2)
    
    def test_package_dependencies(self):
        fanpack = Package("fan")
        fanpack.dependencies = {}
        fanpack.dependencies["build"] = "(foo123 or foo123-2.0) and xyz"

        packages = [Package("foo123"), Package("xyz")]
        self.assertTrue(parse("(foo123 or foo123-2.0)", data=packages))
        self.assertTrue(parse(fanpack.dependencies["build"], data=packages))

if __name__ == "__main__":
    unittest.main()

