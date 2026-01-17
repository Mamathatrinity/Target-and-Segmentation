"""
Fix selectors in test_segments_generated.py
Replace [role="article"] with .home__card (correct Material-UI selector)
"""

content = open('tests/ui/test_segments_generated.py', 'r', encoding='utf-8').read()

# Count original occurrences
original_count = content.count('[role="article"]')
print(f"Found {original_count} instances of incorrect selector [role=\"article\"]")

# Replace the selector
content = content.replace('[role="article"]', '.home__card')
content = content.replace("[role='article']", '.home__card')

# Write back
open('tests/ui/test_segments_generated.py', 'w', encoding='utf-8').write(content)

new_count = content.count('.home__card')
print(f"Replaced with .home__card - now has {new_count} instances")
print("[OK] Selectors updated successfully!")
