#!/usr/bin/env python
# Copyright 2013, Big Switch Networks, Inc.
#
# LoxiGen is licensed under the Eclipse Public License, version 1.0 (EPL), with
# the following special exception:
#
# LOXI Exception
#
# As a special exception to the terms of the EPL, you may distribute libraries
# generated by LoxiGen (LoxiGen Libraries) under the terms of your choice, provided
# that copyright and licensing notices generated by LoxiGen are not altered or removed
# from the LoxiGen Libraries and the notice provided below is (i) included in
# the LoxiGen Libraries, if distributed in source code form and (ii) included in any
# documentation for the LoxiGen Libraries, if distributed in binary form.
#
# Notice: "Copyright 2013, Big Switch Networks, Inc. This library was generated by the LoxiGen Compiler."
#
# You may not use this file except in compliance with the EPL or LOXI Exception. You may obtain
# a copy of the EPL at:
#
# http://www.eclipse.org/legal/epl-v10.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# EPL for the specific language governing permissions and limitations
# under the EPL.
import unittest
from testutil import add_datafiles_tests

try:
    import loxi.of12 as ofp
except ImportError:
    exit("loxi package not found. Try setting PYTHONPATH.")

class TestImports(unittest.TestCase):
    def test_toplevel(self):
        import loxi
        self.assertTrue(hasattr(loxi, "ProtocolError"))
        self.assertEquals(loxi.version_names[3], "1.2")
        ofp = loxi.protocol(3)
        self.assertEquals(ofp.OFP_VERSION, 3)
        self.assertTrue(hasattr(ofp, "action"))
        self.assertTrue(hasattr(ofp, "common"))
        self.assertTrue(hasattr(ofp, "const"))
        self.assertTrue(hasattr(ofp, "message"))
        self.assertTrue(hasattr(ofp, "oxm"))

    def test_version(self):
        import loxi
        self.assertTrue(hasattr(loxi.of12, "ProtocolError"))
        self.assertTrue(hasattr(loxi.of12, "OFP_VERSION"))
        self.assertEquals(loxi.of12.OFP_VERSION, 3)
        self.assertTrue(hasattr(loxi.of12, "action"))
        self.assertTrue(hasattr(loxi.of12, "common"))
        self.assertTrue(hasattr(loxi.of12, "const"))
        self.assertTrue(hasattr(loxi.of12, "message"))
        self.assertTrue(hasattr(loxi.of12, "oxm"))

# The majority of the serialization tests are created here using the files in
# the test_data directory.
class TestDataFiles(unittest.TestCase):
    pass
add_datafiles_tests(TestDataFiles, 'of12/', ofp)

class TestAllOF12(unittest.TestCase):
    """
    Round-trips every class through serialization/deserialization.
    Not a replacement for handcoded tests because it only uses the
    default member values.
    """

    def setUp(self):
        mods = [ofp.action,ofp.message,ofp.common,ofp.oxm]
        self.klasses = [klass for mod in mods
                              for klass in mod.__dict__.values()
                              if hasattr(klass, 'show')]
        self.klasses.sort(key=lambda x: str(x))

    def test_serialization(self):
        expected_failures = [
            ofp.action.set_field, # field defaults to None
        ]
        for klass in self.klasses:
            def fn():
                obj = klass()
                if hasattr(obj, "xid"): obj.xid = 42
                buf = obj.pack()
                obj2 = klass.unpack(buf)
                self.assertEquals(obj, obj2)
            if klass in expected_failures:
                self.assertRaises(Exception, fn)
            else:
                fn()

    def test_parse_message(self):
        expected_failures = []
        for klass in self.klasses:
            if not issubclass(klass, ofp.message.Message):
                continue
            def fn():
                obj = klass(xid=42)
                buf = obj.pack()
                obj2 = ofp.message.parse_message(buf)
                self.assertEquals(obj, obj2)
            if klass in expected_failures:
                self.assertRaises(Exception, fn)
            else:
                fn()

    def test_show(self):
        expected_failures = []
        for klass in self.klasses:
            def fn():
                obj = klass()
                if hasattr(obj, "xid"): obj.xid = 42
                obj.show()
            if klass in expected_failures:
                self.assertRaises(Exception, fn)
            else:
                fn()

if __name__ == '__main__':
    unittest.main()
