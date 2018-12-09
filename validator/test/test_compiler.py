import pytest

import validator.compiler as compiler
from .fixtures import Fixtures

fxt = Fixtures('compiler')


class TestCompiler(object):
    def do_fxt_test(self, fxt_path):
        fixture = fxt.get_anymarkup(fxt_path)
        bundle = fixture['bundle']
        expected = fixture['expected']

        bundle = compiler.compile(bundle)
        assert bundle == expected

    def test_no_refs(self):
        self.do_fxt_test('test-0.yml')

    def test_simple_ref(self):
        self.do_fxt_test('test-1.yml')

    def test_multiple_refs(self):
        self.do_fxt_test('test-2.yml')

    def test_ignore_top_level_refs(self):
        self.do_fxt_test('test-3.yml')

    def test_simple_recursive(self):
        self.do_fxt_test('test-4.yml')

    def test_cycle(self):
        with pytest.raises(compiler.CyclicRefError):
            self.do_fxt_test('test-5.yml')

    def test_merge(self):
        self.do_fxt_test('test-6.yml')
