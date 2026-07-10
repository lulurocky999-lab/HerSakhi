from pathlib import Path
import re

path = Path('templates/ai_mentor/index.html')
text = path.read_text(encoding='utf-8')

start = text.index('function createAIBubble(text, actions = []) {')
end = text.index('function createAILoadingBubble(id) {', start)

replacement = '''function createAIBubble(text, actions = []) {
    const wrapper = document.createElement('div');
    wrapper.className = 'msg-row msg-ai';

    const avatar = document.createElement('div');
    avatar.className = 'msg-avatar';
    const avatarImg = document.createElement('img');
    avatarImg.src = '{% static "images/logo.png" %}';
    avatarImg.alt = 'AI';
    avatarImg.style.width = '20px';
    avatar.appendChild(avatarImg);

    const inner = document.createElement('div');
    const bubble = document.createElement('div');
    bubble.className = 'msg-bubble';
    bubble.innerHTML = text.replace(/\n/g, '<br/>');

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

'''

text = text[:start] + replacement + text[end:]
path.write_text(text, encoding='utf-8')
print('done')
