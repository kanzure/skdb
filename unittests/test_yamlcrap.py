#!/usr/bin/python
import unittest
import yaml
import skdb

class TestTagHack(unittest.TestCase):
    def test_tag_hack(self):
        yaml_string = "!tag_hack\n tags:\n - first_fake_class\n - second_fake_class\n--- #doc2\ntest1: !first_fake_class\ntest2: !second_fake_class"
        loader = yaml.load_all(yaml_string)
        self.assertTrue(loader.next())
        self.assertTrue(loader.next())
        #for some reason the following doesn't work
        #self.assertRaises(loader.next(), StopIteration)
        try: loader.next()
        except StopIteration:
            #ok it passed
            ""
        else:
            self.assertFalse(True, message="hello")

if __name__ == "__main__":
    unittest.main()
