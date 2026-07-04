"""
Test suite: form_engine output validity.
Run: python -m pytest tests/test_form_engine.py -v
"""

import json
import re
import tempfile
from pathlib import Path

import pytest

sys_path_inserted = False
if not sys_path_inserted:
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "infrastructure"))
    sys_path_inserted = True

from ui.form_engine import FormEngine, FormField, FormDefinition


class TestFormOutputValidity:
    """Generated HTML forms must be valid and functional."""

    def test_form_has_all_fields(self):
        """Generated form must contain all defined fields."""
        engine = FormEngine()
        form = FormDefinition(
            title="Test Form",
            description="A test form",
            fields=[
                FormField("name", "text", required=True, label="Name"),
                FormField("email", "email", required=True, label="Email"),
                FormField("tier", "select", options=["A", "B", "C"], label="Tier"),
                FormField("notes", "textarea", label="Notes"),
            ],
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.html"
            engine.create_form(form, path)
            html = path.read_text(encoding="utf-8")

            assert 'name="name"' in html
            assert 'name="email"' in html
            assert 'name="tier"' in html
            assert 'name="notes"' in html
            assert '<form id="agent-form">' in html

    def test_conditional_field_rendered_with_deps(self):
        """Conditional fields must have data-depends-on attributes."""
        engine = FormEngine()
        form = FormDefinition(
            title="Conditional Test",
            fields=[
                FormField("has_wp", "checkbox", options=["Yes"], label="Has WP?"),
                FormField("wp_url", "url", label="WP URL", depends_on="has_wp", depends_value="Yes"),
            ],
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "cond.html"
            engine.create_form(form, path)
            html = path.read_text(encoding="utf-8")

            assert 'data-depends-on="has_wp"' in html
            assert 'data-depends-value="Yes"' in html
            assert 'id="field-wp_url"' in html

    def test_form_has_submit_handler(self):
        """Form must have JavaScript submit handler that exports JSON."""
        engine = FormEngine()
        form = FormDefinition(
            title="Handler Test",
            fields=[FormField("x", "text", label="X")],
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "handler.html"
            engine.create_form(form, path)
            html = path.read_text(encoding="utf-8")

            assert 'form.addEventListener("submit"' in html
            assert 'JSON.stringify(result' in html
            assert 'application/json' in html

    def test_required_fields_have_required_attr(self):
        """Required fields must have HTML required attribute."""
        engine = FormEngine()
        form = FormDefinition(
            title="Required Test",
            fields=[
                FormField("req", "text", required=True, label="Required"),
                FormField("opt", "text", label="Optional"),
            ],
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "req.html"
            engine.create_form(form, path)
            html = path.read_text(encoding="utf-8")

            # The required field should have required attribute
            req_match = re.search(r'name="req"[^>]*required', html)
            assert req_match is not None, "Required field missing 'required' attribute"

    def test_read_response_valid_json(self):
        """read_response must parse valid JSON responses."""
        engine = FormEngine()
        with tempfile.TemporaryDirectory() as tmpdir:
            resp_path = Path(tmpdir) / "response.json"
            test_data = {"client_name": "Acme", "tier": "Growth"}
            resp_path.write_text(json.dumps(test_data), encoding="utf-8")

            result = engine.read_response(resp_path)
            assert result == test_data

    def test_read_response_invalid_json(self):
        """read_response must gracefully handle invalid JSON."""
        engine = FormEngine()
        with tempfile.TemporaryDirectory() as tmpdir:
            resp_path = Path(tmpdir) / "bad.json"
            resp_path.write_text("not json", encoding="utf-8")

            result = engine.read_response(resp_path)
            assert result == {}

    def test_read_response_missing_file(self):
        """read_response must return empty dict for missing files."""
        engine = FormEngine()
        result = engine.read_response(Path("/nonexistent/response.json"))
        assert result == {}


class TestFormFieldTypes:
    """All field types must render correctly."""

    @pytest.mark.parametrize("field_type,expected_tag", [
        ("text", 'type="text"'),
        ("email", 'type="email"'),
        ("url", 'type="url"'),
        ("number", 'type="number"'),
        ("password", 'type="password"'),
        ("date", 'type="date"'),
    ])
    def test_input_types(self, field_type, expected_tag):
        engine = FormEngine()
        form = FormDefinition(
            title="Types Test",
            fields=[FormField("f", field_type, label="F")],
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "types.html"
            engine.create_form(form, path)
            html = path.read_text(encoding="utf-8")
            assert expected_tag in html

    def test_select_field_options(self):
        engine = FormEngine()
        form = FormDefinition(
            title="Select Test",
            fields=[FormField("tier", "select", options=["A", "B", "C"], label="Tier")],
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "select.html"
            engine.create_form(form, path)
            html = path.read_text(encoding="utf-8")
            assert '<option value="A">A</option>' in html
            assert '<option value="B">B</option>' in html
            assert '<option value="C">C</option>' in html

    def test_checkbox_field_options(self):
        engine = FormEngine()
        form = FormDefinition(
            title="Checkbox Test",
            fields=[FormField("opts", "checkbox", options=["X", "Y"], label="Opts")],
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "cb.html"
            engine.create_form(form, path)
            html = path.read_text(encoding="utf-8")
            assert 'type="checkbox"' in html
            assert 'value="X"' in html
            assert 'value="Y"' in html


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
