# -*- coding: utf-8 -*-
"""
Logic & Data Verification Test
"""
import json

with open(r"C:\Users\vanh\.gemini\antigravity\scratch\lexiup\vocab-dataset.json", "r", encoding="utf-8") as f:
    vocab = json.load(f)

# Verify count
assert len(vocab) == 90, f"Expected 90 words, got {len(vocab)}"

# Verify schema for all items
schema_keys = ["id", "word", "ipa", "pos", "meaningVi", "definitionEn", "example", "exampleVi", "level", "topic"]
for i, item in enumerate(vocab):
    for key in schema_keys:
        assert key in item, f"Word {i} ({item.get('word')}) missing key: {key}"
        assert item[key], f"Word {i} ({item.get('word')}) empty value for key: {key}"

# Verify levels
levels = {w["level"] for w in vocab}
assert levels == {"B1", "B2", "C1"}, f"Unexpected levels: {levels}"

# Verify uniqueness
words = [w["word"].lower() for w in vocab]
assert len(words) == len(set(words)), "Duplicate words found!"

print("PASS: Schema and uniqueness verification passed!")
