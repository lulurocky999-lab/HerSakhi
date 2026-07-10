from pathlib import Path
import re
html = Path('templates/ai_mentor/index.html').read_text(encoding='utf-8')
script_match = re.search(r'<script>([\s\S]*?)</script>', html)
if not script_match:
    raise SystemExit('script block not found')
code = script_match.group(1)
code = re.sub(r"\{%[^%]*%\}", "'CHAT_ENDPOINT'", code)
code = re.sub(r"\{{2}[^}]*\}{2}", "'CSRF_TOKEN'", code)
Path('tmp_ai_script.js').write_text(code, encoding='utf-8')
print('wrote', len(code), 'chars')
