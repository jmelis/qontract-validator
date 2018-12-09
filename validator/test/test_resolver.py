import pytest

import validator.resolver as resolver
from .fixtures import Fixtures

fxt = Fixtures('resolver')


class TestSplitRef(object):
    def test_normal(self):
        ref = "path#ptr"
        path, ptr = resolver.split_ref(ref)

        assert path == "path"
        assert ptr == "ptr"

    def test_only_path(self):
        ref = "path"
        path, ptr = resolver.split_ref(ref)

        assert path == "path"
        assert ptr is None

    def test_ends_with_pound(self):
        ref = "path#"
        path, ptr = resolver.split_ref(ref)

        assert path == "path"
        assert ptr is None

    def test_many_pounds(self):
        ref = "path#a#b"
        path, ptr = resolver.split_ref(ref)

        assert path == "path"
        assert ptr == "a#b"

    def test_only_ptr(self):
        ref = "#ptr"
        path, ptr = resolver.split_ref(ref)

        assert path is None
        assert ptr == "ptr"

    def test_only_pound(self):
        ref = "#"

        with pytest.raises(resolver.InvalidRef):
            path, ptr = resolver.split_ref(ref)

    def test_empty(self):
        ref = ""

        with pytest.raises(resolver.InvalidRef):
            path, ptr = resolver.split_ref(ref)


class TestResolver(object):
    def do_fxt_test(self, fxt_path):
        fixture = fxt.get_anymarkup(fxt_path)
        bundle = fixture['bundle']
        expected = fixture['expected']

        bundle = resolver.resolve(bundle)
        assert bundle == expected

    def test_no_refs(self):
        self.do_fxt_test('test_no_refs.yml')

    def test_simple_ref(self):
        self.do_fxt_test('test_simple_ref.yml')

    def test_multiple_refs(self):
        self.do_fxt_test('test_multiple_refs.yml')

    def test_ignore_top_level_refs(self):
        self.do_fxt_test('test_ignore_top_level_refs.yml')

    def test_simple_recursive(self):
        self.do_fxt_test('test_simple_recursive.yml')

    def test_cycle(self):
        with pytest.raises(resolver.CyclicRefError):
            self.do_fxt_test('test_cycle.yml')

    def test_merge(self):
        self.do_fxt_test('test_merge.yml')

    def test_complex_deps(self):
        self.do_fxt_test('test_complex_deps.yml')

    def test_jsonpointer(self):
        self.do_fxt_test('test_jsonpointer.yml')

    def test_jsonpointer_self(self):
        self.do_fxt_test('test_jsonpointer_self.yml')
