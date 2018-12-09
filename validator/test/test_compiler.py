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
        self.do_fxt_test('test-00.yml')

    def test_simple_ref(self):
        self.do_fxt_test('test-01.yml')

    def test_multiple_refs(self):
        self.do_fxt_test('test-02.yml')

    def test_ignore_top_level_refs(self):
        self.do_fxt_test('test-03.yml')

    def test_simple_recursive(self):
        self.do_fxt_test('test-04.yml')

    def test_cycle(self):
        with pytest.raises(compiler.CyclicRefError):
            self.do_fxt_test('test-05.yml')

    def test_merge(self):
        self.do_fxt_test('test-06.yml')

    def test_complex_deps(self):
        self.do_fxt_test('test-07.yml')
