from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import validate_pack as validator


class DocumentChecks(unittest.TestCase):
    def test_synthetic_private_values_are_flagged_without_echoing_them(self) -> None:
        samples = [
            "sk-" + "SYNTHETIC" * 4,
            "gho_" + "SYNTHETIC" * 4,
            "123456789" + ":" + "SYNTHETIC" * 5,
            "C:" + "/Users/" + "SyntheticPerson/private.txt",
            "C:" + "\\Users\\" + "SyntheticPerson\\private.txt",
            'app_secret = "' + "SYNTHETIC" * 3 + '"',
        ]
        for sample in samples:
            with self.subTest(kind=sample[:3]):
                errors: list[str] = []
                validator.validate_privacy(validator.ROOT / "sample.md", sample, errors)
                self.assertTrue(errors)
                self.assertNotIn(sample, "\n".join(errors))

    def test_placeholders_are_not_credentials(self) -> None:
        errors: list[str] = []
        validator.validate_privacy(
            validator.ROOT / "sample.md",
            'app_secret = "<local-secret>"; C:/Users/<user>/data; bot=<bot-token>',
            errors,
        )
        self.assertEqual(errors, [])

    def test_missing_and_escaping_links_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "exists.md").write_text("ok", encoding="utf-8")
            with patch.object(validator, "ROOT", root):
                errors: list[str] = []
                validator.validate_links(
                    root / "README.md",
                    "[ok](exists.md#part) [missing](missing.md) [outside](../outside.md)",
                    errors,
                )
                self.assertEqual(len(errors), 2)

    def test_bilingual_reference_coverage_without_wording_requirement(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            zh = root / "README.md"
            en = root / "README.en.md"
            zh.write_text("[English](README.en.md) [甲](references/topic.md)", encoding="utf-8")
            en.write_text("[中文](README.md) [Different wording](references/topic.en.md)", encoding="utf-8")
            with patch.object(validator, "ROOT", root), patch.object(validator, "CHINESE_PRIMARY", {"README.md"}):
                errors: list[str] = []
                validator.validate_bilingual_links(errors)
                self.assertEqual(errors, [])
                en.write_text("[中文](README.md)", encoding="utf-8")
                validator.validate_bilingual_links(errors)
                self.assertEqual(len(errors), 1)


if __name__ == "__main__":
    unittest.main()
