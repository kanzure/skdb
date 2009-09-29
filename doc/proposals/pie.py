#!/usr/bin/python
from skdb import Part, Unit, UnitError
from string import join, split
import unittest

bryan_message = "bryan hasnt got to this yet"

class Color(Unit):
    '''will eventually implement CIE 1931 XYZ color space'''
    yaml_tag = "!color"
    colors = {
             "red": Unit("700 nm"),
             "orange": Unit("620 nm"),
             "yellow": Unit("580 nm"),
             "green": Unit("530 nm"),
             "blue": Unit("470 nm"),
             "violet": Unit("420 nm"),
             }
    def __init__(self, color=None):
        if color is None:
            #FIXME: if it has no color it's white light?
            raise NotImplementedError, "white light is not yet implemented"
        elif isinstance(color, Color):
            self.color = color.color
            self.wavelength = color.wavelength
        elif isinstance(color, str):
            #first try treating it as a unit
            try:
                if color.replace(" ", "").isalnum(): #FIXME: what about "nm" (which should be interpreted as "1nm")?
                    color = Unit(color)
                    if color.compatible("nm"):
                        #then it is, in fact, a wavelength
                        self.wavelength = color
                        self.color = color
                        #return point
                    else: raise UnitError, "Color.__init__: supplied unit was not compatible with wavelength (nm)"
                else: raise UnitError, "was not alpha numeric and was likely not a unit" #return point
            except UnitError, ue:
                #first check if it looks like a unit
                if ue.message.count("was not compatible") == 1: raise UnitError, "Color.__init__: incompatible units on %s" % (color)
                #was not a valid unit, maybe it's "green"
                #try:
                if color in self.colors.keys():
                    color = self.colors[color]
                    self.wavelength = color
                    self.color = color
                    #return point
                else: raise ValueError, "Color.__init__: unable to parse color %s\n%s" % (color, ue) #return point
                #except UnitError, ue:
        elif isinstance(color, Unit):
            if color.compatible("nm"):
                self.wavelength = color
        else: raise NotImplementedError, bryan_message
        Unit.__init__(self, self.wavelength)
    def _get_name(self):
        #figure out the name of this color from self.wavelength
        items = self.colors.items()
        for item in items:
            if item[1] == self.wavelength:
                return item[0]
        #since we don't know a name, just give it
        return self.wavelength
    name = property(fget=_get_name, doc="figures out the name of the color")
    def __repr__(self):
        return "Color(\"%s\")" % (self.name)
    def __eq__(self, other):
        try:
            if other.wavelength == self.wavelength: return True
            return False
        except AttributeError, error:
            #maybe it's a color
            if other in self.colors:
                return (Color(other)==self)
            else: return Unit.__eq__(self, other)

class Apple(Part):
    yaml_tag = "!apple"
    def __init__(self, color=Color("green"), sliced=False):
        if not isinstance(color, Color): color = Color(color)
        self.color = color
        self.sliced = sliced
    def __eq__(self, other):
        if isinstance(other, Apple):
            if self.color == other.color: return True
            else: return False
        elif isinstance(other, Color) or isinstance(other, Unit):
            if self.color == other: return True
            else: return False
        else: return False
    def _get_name(self):
        return self.color.name
    name = property(fget=_get_name, doc="figures out the name of the apple")
    def __repr__(self):
        return "Apple(\"%s\")" % (self.name)

class Pumpkin(Part):
    yaml_tag = "!pumpkin"
    def __init__(self):
        Part.__init__(self)
        self.name = ""
    def __repr__(self):
        return "Pumpkin(\"%s\")" % (self.name)

class Pie(Part):
    yaml_tag = "!pie"
    #for parsing pie strings:
    pie_map = {
                "apple": Apple,
                "pumpkin": Pumpkin,
              }
    #well if this was a screw..
    build_depends = "(threading or thread rolling or thread milling or thread whirling) and (bar stock or (wire and cold heating))"
    def __init__(self, ingredients):
        if type(ingredients) == str:
            if ingredients.count(" ") > 0:
                ingredients = split(ingredients.lower(), " ")
            else: ingredients = ingredients.lower()
        if type(ingredients) is not type([]): ingredients = [ingredients]
        self.name = ""
        names = []
        real_ingredients = []
        
        ingredients = list(set(ingredients))
        for ingredient in ingredients:
            if hasattr(ingredient, "name"):
                if ingredient.name == "": names.append(ingredient.__class__.__name__)
                else: names.append(ingredient.name + " " + ingredient.__class__.__name__)
                real_ingredients.append(ingredient)
            elif hasattr(ingredient, "__repr__"):
                if ingredient in self.pie_map.keys():
                    inst = self.pie_map[ingredient]
                    real_ingredients.append(inst())
                    names.append(inst.__name__)
                else: names.append(ingredient)
        names = list(set(names))
        self.name = join(names)
        self.name = self.name.lower()

        self.name = self.name.lower()
        self.ingredients = real_ingredients
    def __eq__(self, other):
        if self.ingredients == other.ingredients: return True
        return False

class TestPie(unittest.TestCase):
    def test_color_init(self):
        #yay all of this passed on the first go :)
        green = Color("green")
        self.assertTrue(str(green) == "Color(\"green\")" or str(green)=="green")
        self.assertTrue(green.wavelength.compatible("m"))
        self.assertTrue(str(green.wavelength) == "530 nm")
        self.assertTrue(green.wavelength == "530 nm")
        self.assertTrue(green.wavelength == Unit("530 nm"))
        self.assertTrue(green == Color("green"))
        self.assertTrue(green == Color("530 nm"))
        self.assertTrue(green == Color(Unit("530 nm")))

        self.assertTrue(green.compatible("m"))
        self.assertTrue(green.compatible("500 m")) #compatibility doesn't care about magnitude
        self.assertTrue(green.compatible(Unit("m")))
        self.assertFalse(green.compatible(Unit("kg")))
        self.assertTrue(green == "530 nm")
        self.assertTrue(green == "green")
        self.assertTrue(green == Unit("530 nm"))

        green = Color(Color("green"))
        self.assertTrue(green == Color("530 nm"))

    def test_color_repr(self):
        #test a color that it doesn't have a name for (in Color.colors)
        self.assertTrue(str(Color("10 km")) == "Color(\"10 km\")")

    def test_additive_color(self):
        pass
    def test_subtractive_color(self):
        pass
    def test_apple_init(self):
        green_apple = Apple("green")
        self.assertTrue(green_apple.name == "green")

        green_apple = Apple("530 nm")
        self.assertTrue(green_apple.name == "green")

        green_apple = Apple(Color("green"))
        self.assertTrue(green_apple.name == "green")

        green_apple = Apple(Color("530 nm"))
        self.assertTrue(green_apple.name == "green")

        green_apple = Apple(Color(Unit("530 nm")))
        self.assertTrue(green_apple.name == "green")

        green_apple = Apple(Unit("530 nm"))
        self.assertTrue(green_apple.name == "green")

    def test_apple_eq(self):
        apple1 = Apple("530 nm")
        apple2 = Apple(Color(Unit("530 nm")))
        self.assertTrue(apple1 == apple2)

    def test_pie_init(self):
        apple_pie = Pie(Apple())
        self.assertTrue(apple_pie.name.count("apple") == 1) #name is "green apple"
        
        apple_pie = Pie([Apple()])
        self.assertTrue(apple_pie.name.count("apple") == 1) #name is "green apple"
        
        apple_pie = Pie([Apple(), Pumpkin()])
        self.assertTrue(apple_pie.name.count("apple") == 1)
        self.assertTrue(apple_pie.name.count("pumpkin") == 1)

        apple_pie = Pie([Apple(Color("green")), Pumpkin()])
        self.assertTrue(apple_pie.name.count("apple") == 1)
        
        apple_pie = Pie([Apple(), Pumpkin(), Apple()])
        self.assertTrue(apple_pie.name.count("apple") == 1)
        self.assertTrue(apple_pie.name.count("pumpkin") == 1)

        apple_pie = Pie("apple")
        self.assertTrue(apple_pie.name.count("apple") == 1)
        apple_pie = Pie("ApPlE")
        self.assertTrue(apple_pie.name.count("apple") == 1)
        apple_pie = Pie("aPpLe apple APPLE aPPLE Apple APple APPle APPLe applE appLE apPLE aPPLE")
        self.assertTrue(apple_pie.name.count("apple") == 1)
        self.assertTrue(len(apple_pie.ingredients) == 1)

        apple_pie = Pie("apple pumpkin")
        self.assertTrue(len(apple_pie.ingredients) == 2)

    def test_pie_map(self):
        apple_pie1 = Pie("apple")
        self.assertTrue(isinstance(apple_pie1.ingredients[0], Apple))

    def test_pie_eq(self):
        apple_pie1 = Pie("apple")
        apple_pie2 = Pie(Apple())
        self.assertTrue(apple_pie1 == apple_pie2)

        apple_pie1 = Pie("pumpkin")
        apple_pie2 = Pie(Apple())
        self.assertFalse(apple_pie1 == apple_pie2)

if __name__ == "__main__":
    unittest.main()

