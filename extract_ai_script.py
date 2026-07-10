from pathlib import Path
import re
html = Path('templates/ai_mentor/index.html').read_text(encoding='utf-8')
script = re.search(r'<script>([\s\S]*?)</script>', html)
if not script:
    raise SystemExit('script block not found')
code = script.group(1)
code = re.sub(r"\{%[^%]*%\}", '"DjangoTag"', code)
code = re.sub(r"\{{2}[^}]*\}{2}", '"DjangoExpr"', code)
Path('tmp_ai_script.js').write_text(code, encoding='utf-8')
print('wrote', len(code), 'chars to tmp_ai_script.js')
