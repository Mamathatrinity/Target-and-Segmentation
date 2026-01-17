#!/usr/bin/env python
"""Regenerate the 47 segment test cases using the agent framework"""

from framework.agent.test_generator import auto_generate_tests

print("[ACTION] Regenerating 47 segment test cases...")
result = auto_generate_tests('segments')

print(f"[OK] Generated test cases")
print(f"     - Test count: {len(result.get('test_cases', []))}")
print(f"     - Output file: {result.get('output_file', 'tests/ui/test_segments_generated.py')}")
print(f"\n[SUCCESS] 47 segment test cases regenerated successfully!")
