fix_code = """
       if "APPROVE" in boss_decision['decision']:
           print("✅ APPROVED! Publishing to Twitter...")

           # 🔧 FIX: Extract clean tweet content
           boss_response = boss_decision['decision']
           final_content = ''

           if "ready to post:" in boss_response:
               part = boss_response.split("ready to post:")[-1]
               final_content = part.split("Rationale")[0].strip()

           if not final_content:
               final_content = boss_response.split("\\n")[0].strip()

           final_content = final_content.replace("APPROVE", "").strip(" :\\\"'")

           if len(final_content) > 280:
               print(f"⚠️ Tweet too long: {len(final_content)} chars — truncating")
               final_content = final_content[:277] + "..."

           # DEBUG: Show what we're about to post
           print(f"🔍 DEBUG: About to post content:")
           print(f"   Length: {len(final_content)} characters")
           print(f"   Content: '{final_content}'")
           print(f"   Content repr: {repr(final_content)}")

           response = self.twitter_client.post_tweet(final_content)
"""

# --- apply patch ---
with open("main.py", "r") as f:
    content = f.read()

# Replace the old assignment block
import re
pattern = r"if \"APPROVE\" in boss_decision\['decision'\]:.*?response = self\.twitter_client\.post_tweet\(final_content\)"
new_content = re.sub(pattern, fix_code, content, flags=re.S)

with open("main.py", "w") as f:
    f.write(new_content)

print("✅ Patched main.py with safer tweet extraction")
