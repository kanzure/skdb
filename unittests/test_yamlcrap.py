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
        data='!foo 123'
        print self.preamble+data
        test = skdb.load(self.preamble+data) #why does this fail?
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

if __name__ == '__main__':
    unittest.main()

