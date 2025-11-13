"""Validate generated question payloads against JSON Schema."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from jsonschema import Draft7Validator

SCHEMA_PATH = Path(__file__).resolve().parent.parent / 'schemas' / 'question.schema.json'


def load_schema() -> dict:
    with SCHEMA_PATH.open('r', encoding='utf-8') as f:
        return json.load(f)


def validate_payloads(files: Iterable[Path]) -> None:
    schema = load_schema()
    validator = Draft7Validator(schema)
    for path in files:
        payload = json.loads(path.read_text(encoding='utf-8'))
        errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
        if errors:
            print(f"❌ {path.name} validation failed")
            for error in errors:
                location = '/'.join(map(str, error.path)) or '<root>'
                print(f"  - {location}: {error.message}")
        else:
            print(f"✅ {path.name} valid")


def main() -> None:
    samples_dir = Path(__file__).resolve().parent.parent / 'samples'
    json_files = samples_dir.glob('*.json')
    validate_payloads(json_files)


if __name__ == '__main__':
    main()
