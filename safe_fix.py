# Read the file
with open('main.py', 'r') as f:
    lines = f.readlines()

# Find the problematic section and replace it
new_lines = []
skip_until_response = False

for i, line in enumerate(lines):
    if 'if "APPROVE" in boss_decision[\'decision\']:' in line:
        # Found the start - add our fixed version
        indent = line[:len(line) - len(line.lstrip())]  # Get the indentation
        new_lines.append(line)  # Keep the if statement
        new_lines.extend([
            f'{indent}    print("✅ APPROVED! Publishing to Twitter...")\n',
            f'{indent}\n',
            f'{indent}    # 🔧 FIX: Extract clean tweet content\n',
            f'{indent}    boss_response = boss_decision["decision"]\n',
            f'{indent}    final_content = ""\n',
            f'{indent}\n',
            f'{indent}    if "ready to post:" in boss_response:\n',
            f'{indent}        part = boss_response.split("ready to post:")[-1]\n',
            f'{indent}        final_content = part.split("Rationale")[0].strip()\n',
            f'{indent}\n',
            f'{indent}    if not final_content:\n',
            f'{indent}        final_content = boss_response.split("\\n")[0].strip()\n',
            f'{indent}\n',
            f'{indent}    final_content = final_content.replace("APPROVE", "").strip(" :\\"\'")\n',
            f'{indent}\n',
            f'{indent}    if len(final_content) > 280:\n',
            f'{indent}        print(f"⚠️ Tweet too long: {{len(final_content)}} chars — truncating")\n',
            f'{indent}        final_content = final_content[:277] + "..."\n',
            f'{indent}\n',
            f'{indent}    # DEBUG: Show what we\'re about to post\n',
            f'{indent}    print(f"🔍 DEBUG: About to post content:")\n',
            f'{indent}    print(f"   Length: {{len(final_content)}} characters")\n',
            f'{indent}    print(f"   Content: \'{{final_content}}\'")\n',
            f'{indent}    print(f"   Content repr: {{repr(final_content)}}")\n',
            f'{indent}\n',
        ])
        skip_until_response = True
        continue
    elif skip_until_response and 'response = self.twitter_client.post_tweet(final_content)' in line:
        # Found the end - add this line and stop skipping
        new_lines.append(line)
        skip_until_response = False
        continue
    elif not skip_until_response:
        # Normal line - keep it
        new_lines.append(line)
    # If skip_until_response is True, we skip the line (it's part of the old code)

# Write back
with open('main.py', 'w') as f:
    f.writelines(new_lines)

print('✅ Fixed main.py with proper indentation')
