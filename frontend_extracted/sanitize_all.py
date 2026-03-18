import os
import re

def sanitize_content(content):
    # Mapping of common non-ASCII characters to ASCII
    mapping = {
        '\u2014': '-', # em dash
        '\u2192': '->', # right arrow
        '\u2013': '-', # en dash
        '\u2022': '*', # bullet
        '\u21d2': '=>', # double right arrow
        '\u2705': '[OK]', # check mark
        '\u26a0': '[WARN]', # warning
        '\ud83d\udca1': '[IDEA]', # light bulb
        '\u23f1': '[TIME]', # stopwatch
        '\ud83d\udcca': '[STATS]', # bar chart
        '\ud83d\udd01': '[RETRY]', # repeat button
        '\u2b50': '[STAR]', # star
        '\u274c': '[X]', # cross mark
        '\ud83e\udde0': '[AI]', # brain
        '\ud83d\udc64': '[USER]', # silhouette
        '\u26a1': '[ENGINE]', # high voltage
        '\ud83d\udcb3': '[CARD]', # credit card
        '\ud83d\udcc8': '[TREND]', # chart up
        '\ud83d\udce6': '[BOX]', # package
        '\ud83c\udfaf': '[TARGET]', # direct hit
        '\ud83d\udea8': '[ALERT]', # siren
        '\ud83d\udcc1': '[FILE]', # file folder
        '\ud83d\udccb': '[LIST]', # clipboard
        '\ud83c\udfc6': '[TROPHY]', # trophy
        '\ud83e\udd47': '[1st]', # medal 1
        '\ud83e\udd48': '[2nd]', # medal 2
        '\ud83e\udd49': '[3rd]', # medal 3
        '\ud83d\udcb0': '[MONEY]', # money bag
        '\ud83d\udcd3': '[NOTE]', # notebook
        '\ud83d\udcc5': '[DATE]', # calendar
        '\ud83d\udd0d': '[SEARCH]', # search
        '\ud83d\udcac': '[CHAT]', # speech bubble
        '\ud83c\udf10': '[WEB]', # globe
        '\ud83d\uddfa': '[MAP]', # map
        '\ud83d\udca1': '[INSIGHT]', # light bulb (duplicate but safe)
        '\u20b9': 'INR', # rupee
        '\u2026': '...', # ellipsis
    }
    
    for char, replacement in mapping.items():
        content = content.replace(char, replacement)
    
    # Generic non-ASCII removal: replace any remaining non-ASCII with ? or space
    # (Optional: only if you want to be extremely aggressive)
    # content = ''.join([c if ord(c) < 128 else ' ' for c in content])
    
    return content

def walk_and_sanitize(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(('.py', '.json', '.txt', '.md')):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    sanitized = sanitize_content(content)
                    
                    if sanitized != content:
                        print(f"Sanitizing {path}...")
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(sanitized)
                except Exception as e:
                    print(f"Error processing {path}: {e}")

if __name__ == "__main__":
    target = r"c:\Users\Soumoditya Das\Downloads\GFG kolkata\InsightPulse_AI"
    walk_and_sanitize(target)
