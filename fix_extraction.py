import re

# Read the current main.py
with open('main.py', 'r') as f:
    content = f.read()

# Find the problematic content extraction section and replace it
old_pattern = r'# Extract just the tweet content from boss response.*?final_content = final_content\[:277\] \+ \'\.\.\.\'.*?'

new_extraction = '''# Extract just the tweet content from boss response
                    boss_response = boss_decision['decision']
                    final_content = ''
                    
                    import re
                    
                    # 1. Look for "ready to post:" and grab everything after
                    if "ready to post:" in boss_response:
                        candidate = boss_response.split("ready to post:")[-1].strip()
                        final_content = candidate.split("Rationale")[0].strip()
                    
                    # 2. Otherwise, look for "Tweet 1:" style threads
                    elif "Tweet 1:" in boss_response:
                        tweets = re.findall(r"Tweet \\d+:(.*?)(?=Tweet \\d+:|$)", boss_response, flags=re.S)
                        if tweets:
                            final_content = tweets[0].strip()
                    
                    # 3. Otherwise, fallback: find the longest quoted string <= 280 chars
                    if not final_content:
                        quoted = re.findall(r'"([^"]+)"', boss_response)
                        short_candidates = [q for q in quoted if len(q) <= 280]
                        if short_candidates:
                            final_content = short_candidates[0].strip()
                    
                    # Clean up
                    final_content = final_content.replace("APPROVE", "").strip()
                    if len(final_content) > 280:
                        print(f"⚠️ Tweet too long ({len(final_content)} chars) – truncating to 280.")
                        final_content = final_content[:277] + "..." '''

# Apply the fix
updated_content = re.sub(old_pattern, new_extraction, content, flags=re.DOTALL)

# Write back to main.py
with open('main.py', 'w') as f:
    f.write(updated_content)

print('✅ Fixed content extraction in main.py')
