import unittest, yaml, skdb

class Test_dummy_tags(unittest.TestCase):
    def init_tags(self):
        self.preamble='!!python/object:skdb.tag_hack \n tags: "!hello"\n---\n' #init dummy tags
        #self.preamble='!tag_hack \n tags: "hello"\n---\n' #init dummy tags
    def test_default(self):
        test = skdb.load('!!python/object:skdb.tag_hack \n tags: "!hello"\n---\n'+'!hello 1234')
        self.assertEqual(type(test), skdb.Dummy)
    def test_scalar_node(self):
        self.init_tags()
        data='!hello 1234'
        test = skdb.load(self.preamble+data)
        self.assertEqual(type(test), skdb.Dummy)
    def test_run_again(self): #same as above
        self.init_tags()
        data='!hello 1234'
        test = skdb.load(self.preamble+data)
        self.assertEqual(type(test), skdb.Dummy)
    def test_bad_tag(self):
        self.init_tags()
        data='!sometag 123'
        self.assertRaises(yaml.constructor.ConstructorError, skdb.load, self.preamble+data)
    def test_only_dummy_tags_affected(self):
        self.init_tags()
        self.assertEqual(type(skdb.load('!!int 123')), int)
        class Foo(yaml.YAMLObject):
            yaml_tag='!foo'
            def __init__(self, val): pass
        data='!foo\nbar: 123'
        test = skdb.load(self.preamble+data)
        self.assertEqual(type(test), Foo)
    def test_scalar_attrib(self):
        self.init_tags()
        data='!hello\n test: 1234'
        test = skdb.load(self.preamble+data)
        self.assertEqual(type(test), skdb.Dummy)
        
    def test_mapping_attrib(self):
        self.init_tags()
        data='!hello\ntest:\n  test:\n  zonk: 1234'
        test = skdb.load(self.preamble+data)
        self.assertEqual(type(test), skdb.Dummy)
    def init_multiple(self):
        self.preamble='!!python/object:skdb.tag_hack \n tags: ["!hello", "!hi", "!hola"]\n---\n'
    def test_multiple_tags(self):
        self.init_multiple()
        data='- !hello 1234\n- !hi 5678'
        test = skdb.load(self.preamble+data)
        self.assertEqual(type(test[0]), skdb.Dummy)
        self.assertEqual(type(test[1]), skdb.Dummy)
    def test_nested_tags(self):
        self.init_multiple()
        data='!hello\ntest: !hi 5678'
        test = skdb.load(self.preamble+data)
        self.assertEqual(type(test), skdb.Dummy)
        self.assertEqual(type(test.test), skdb.Dummy)

class TestYaml(unittest.TestCase):
    
    def test_implicit(self):
        testrange = skdb.load('1..2')
        self.assertEqual(testrange.min, 1)
        self.assertEqual(testrange.max, 2)
    def test_equals(self):
        self.assertEqual(skdb.load('1..2'), skdb.load('1..2'))
    def test_implicit_equals(self):
        self.assertEqual(skdb.load('1..2'), skdb.Range(1, 2))
    def test_spaces(self):
        testrange = skdb.load('1..2')
        self.assertEqual(testrange, skdb.load('1   ..2'))
        self.assertEqual(testrange, skdb.load('1..   2'))
        self.assertEqual(testrange, skdb.load('1   ..   2'))
        self.assertEqual(testrange, skdb.load('1..2   '))
        self.assertEqual(testrange, skdb.load('   1..2'))
    def test_units(self):
        testrange = skdb.load('1..2m')
        self.assertEqual(testrange.min, skdb.Unit('1m'))
        self.assertEqual(testrange.max, skdb.Unit('2m'))
    def test_both_labeled(self):
        self.assertEqual(skdb.load('1..2m'), skdb.load('1m .. 2m'))
    def test_one_labeled_equal(self):
        self.assertEqual(skdb.load('1..2m'), skdb.Range(skdb.Unit('1m'), skdb.Unit('2m')))
    def test_negative(self):
        testrange = skdb.load('-2.345..1.234')
        self.assertEqual(testrange.min, -2.345)
        self.assertEqual(testrange.max, 1.234)
    def test_ordering(self):
        testrange = skdb.load('1.234 .. -2.345')
        self.assertEqual(testrange.min, -2.345)
        self.assertEqual(testrange.max, 1.234)
    def test_scientific(self):
        testrange = skdb.load('2.345e234 .. 2.345e-1')
        self.assertEqual(testrange.min, 2.345e-1)
        self.assertEqual(testrange.max, 2.345e234)
    def test_yaml_units(self): 
        import yaml
        try: yaml.dump(skdb.Unit('1')) #this blew up once for some reason
        except skdb.UnitError: return False
    def test_uncertainty(self):
        self.assertEqual(skdb.load('+-5e-2m'), skdb.Uncertainty('+-50mm'))

if __name__ == '__main__':
    unittest.main()

