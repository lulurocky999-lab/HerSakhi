from pathlib import Path

path = Path("templates/ai_mentor/index.html")
text = path.read_text(encoding="utf-8")
old = """function createAIBubble(text, actions = []) {
    const wrapper = document.createElement('div');
    wrapper.className = 'msg-row msg-ai';
    
    const time = getCurrentTime();
    
    let html = `
        <div class=\"msg-avatar\">
            <img src=\"{% static 'images/logo.png' %}\" style=\"width: 20px;\" alt=\"AI\" />
        </div>
        <div>
            <div class=\"msg-bubble\">
                <p style=\"margin: 0;\">${text.replace(/\\n/g, '<br/>')}</p>
    `;
    
    if (actions && actions.length > 0) {
        html += `<div style=\"margin-top: 1rem; display: flex; flex-wrap: wrap; gap: 0.5rem;\">`;
        actions.forEach(action => {
            html += `<button class=\"chip\" onclick=\"setInput('${action}')\">${action}</button>`;
        });
        html += `</div>`;
    }
    
    html += `
            </div>
            <div class=\"msg-time\" style=\"justify-content: flex-start;\">${time}</div>
        </div>
    `;
    
    wrapper.innerHTML = html;
    return wrapper;
}
"""
new = """function createAIBubble(text, actions = []) {
    const wrapper = document.createElement('div');
    wrapper.className = 'msg-row msg-ai';

    const avatar = document.createElement('div');
    avatar.className = 'msg-avatar';
    const avatarImg = document.createElement('img');
    avatarImg.src = '{% static \"images/logo.png\" %}';
    avatarImg.alt = 'AI';
    avatarImg.style.width = '20px';
    avatar.appendChild(avatarImg);

    const inner = document.createElement('div');
    const bubble = document.createElement('div');
    bubble.className = 'msg-bubble';
    bubble.innerHTML = text.replace(/\\n/g, '<br/>');

    inner.appendChild(bubble);

    if (actions && actions.length > 0) {
        const actionWrap = document.createElement('div');
        actionWrap.style.marginTop = '1rem';
        actionWrap.style.display = 'flex';
        actionWrap.style.flexWrap = 'wrap';
        actionWrap.style.gap = '0.5rem';

        actions.forEach(action => {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'chip';
            button.textContent = action;
            button.addEventListener('click', () => setInput(action));
            actionWrap.appendChild(button);
        });

        inner.appendChild(actionWrap);
    }

    const timeRow = document.createElement('div');
    timeRow.className = 'msg-time';
    timeRow.style.justifyContent = 'flex-start';
    timeRow.textContent = getCurrentTime();

    inner.appendChild(timeRow);
    wrapper.appendChild(avatar);
    wrapper.appendChild(inner);
    return wrapper;
}
"""

if old not in text:
    start = text.index('function createAIBubble(text, actions = []) {')
    end = text.index('function createAILoadingBubble(id) {', start)
    print('old text not found')
    print(repr(text[start:end]))
    raise SystemExit(1)

text = text.replace(old, new, 1)
path.write_text(text, encoding='utf-8')
print('patched')
