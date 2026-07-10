
function setInput(text) {
    document.getElementById('chatInput').value = text;
    document.getElementById('chatInput').focus();
}

function handleKeyPress(e) {
    if (e.key === 'Enter') sendMessage();
}

function triggerAttachment() {
    document.getElementById('attachmentInput').click();
}

function handleAttachment(event) {
    const file = event.target.files[0];
    if (!file) return;
    const supportedTypes = ['text/plain', 'application/pdf'];
    if (!supportedTypes.includes(file.type)) {
        const chatHistory = document.getElementById('chatHistory');
        chatHistory.appendChild(createAIBubble('This file type is not supported. Please upload a .txt or .pdf file.', []));
        scrollToBottom();
        return;
    }

    if (file.type === 'text/plain') {
        const reader = new FileReader();
        reader.onload = () => {
            const content = reader.result;
            sendMessage(content, { fileName: file.name, fileType: file.type });
        };
        reader.onerror = () => {
            const chatHistory = document.getElementById('chatHistory');
            chatHistory.appendChild(createAIBubble('Unable to read the selected file. Please try again.', []));
            scrollToBottom();
        };
        reader.readAsText(file);
    } else {
        sendMessage(null, { fileName: file.name, fileType: file.type, fileContent: null });
    }
}

async function sendMessage(attachmentText = null, attachmentMeta = null) {
    const input = document.getElementById('chatInput');
    const msg = input.value.trim();
    if (!msg && !attachmentMeta) return;
    
    let displayText = msg;
    if (attachmentMeta && attachmentMeta.fileName) {
        displayText = msg ? `${msg} (attached ${attachmentMeta.fileName})` : `Attached file: ${attachmentMeta.fileName}`;
    }

    input.value = '';
    
    const chatHistory = document.getElementById('chatHistory');
    chatHistory.appendChild(createUserBubble(displayText));
    scrollToBottom();
    
    const loadingId = 'loading-' + Date.now();
    chatHistory.appendChild(createAILoadingBubble(loadingId));
    scrollToBottom();
    
    try {
        const payload = { message: msg };
        if (attachmentMeta) {
            payload.attachment = {
                file_name: attachmentMeta.fileName,
                file_type: attachmentMeta.fileType,
                content: attachmentText || attachmentMeta.fileContent || ''
            };
        }
        const response = await fetch("/fake-url", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': 'fake-csrf'
            },
            credentials: 'same-origin',
            body: JSON.stringify(payload)
        });
        
        const data = await response.json();
        const loader = document.getElementById(loadingId);
        if (loader) loader.remove();
        
        if (data.success && data.reply) {
            chatHistory.appendChild(createAIBubble(data.reply, data.suggested_actions));
        } else {
            chatHistory.appendChild(createAIBubble(data.message || 'AI is not available right now. Please try again later.', []));
        }
    } catch (e) {
        const loader = document.getElementById(loadingId);
        if (loader) loader.remove();
        chatHistory.appendChild(createAIBubble('A network error occurred. Please try again.', []));
    }
    
    scrollToBottom();
}

function getCurrentTime() {
    return new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
}

function createUserBubble(text) {
    const wrapper = document.createElement('div');
    wrapper.className = 'msg-row msg-user';

    const inner = document.createElement('div');
    const bubble = document.createElement('div');
    bubble.className = 'msg-bubble';
    bubble.textContent = text;

    const timeRow = document.createElement('div');
    timeRow.className = 'msg-time';
    timeRow.innerHTML = `${getCurrentTime()}<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>`;

    inner.appendChild(bubble);
    inner.appendChild(timeRow);
    wrapper.appendChild(inner);
    return wrapper;
}

function createAIBubble(text, actions = []) {
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

function createAILoadingBubble(id) {
    const wrapper = document.createElement('div');
    wrapper.id = id;
    wrapper.className = 'msg-row msg-ai';
    
    wrapper.innerHTML = \`
        <div class="msg-avatar">
            <img src="{% static 'images/logo.png' %}" style="width: 20px;" alt="AI" />
        </div>
        <div>
            <div class="msg-bubble" style="display: flex; gap: 4px; align-items: center; min-height: 44px;">
                <div style="width: 6px; height: 6px; border-radius: 50%; background: var(--text-light); animation: blink 1.4s infinite both;"></div>
                <div style="width: 6px; height: 6px; border-radius: 50%; background: var(--text-light); animation: blink 1.4s infinite both; animation-delay: 0.2s;"></div>
                <div style="width: 6px; height: 6px; border-radius: 50%; background: var(--text-light); animation: blink 1.4s infinite both; animation-delay: 0.4s;"></div>
                <style>@keyframes blink { 0% { opacity: 0.2; } 20% { opacity: 1; } 100% { opacity: 0.2; } }</style>
            </div>
        </div>
    \`;
    return wrapper;
}

function scrollToBottom() {
    const chatHistory = document.getElementById('chatHistory');
    if (chatHistory) {
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
}

function bindMentorEvents() {
    const sendButton = document.getElementById('sendButton');
    const attachmentButton = document.getElementById('attachmentButton');
    const attachmentInput = document.getElementById('attachmentInput');
    const chatInput = document.getElementById('chatInput');

    if (sendButton) {
        sendButton.addEventListener('click', () => sendMessage());
    }
    if (attachmentButton && attachmentInput) {
        attachmentButton.addEventListener('click', () => attachmentInput.click());
        attachmentInput.addEventListener('change', handleAttachment);
    }
    if (chatInput) {
        chatInput.addEventListener('keydown', (event) => {
            if (event.key === 'Enter') {
                event.preventDefault();
                sendMessage();
            }
        });
    }
}

// Load Chat History on mount
document.addEventListener('DOMContentLoaded', async () => {
    bindMentorEvents();

    try {
        const response = await fetch("/fake-url");
        const data = await response.json();
        
        if (data.success && data.history && data.history.length > 0) {
            const chatHistory = document.getElementById('chatHistory');
            // Clear default greeting if we have history
            chatHistory.innerHTML = ''; 
            
            data.history.forEach(msg => {
                if (msg.role === 'user') {
                    chatHistory.appendChild(createUserBubble(msg.content));
                } else {
                    chatHistory.appendChild(createAIBubble(msg.content));
                }
            });
            scrollToBottom();
        }
    } catch (e) {
        console.error("Failed to load history", e);
    }
});
