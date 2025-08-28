const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const sendButton = document.getElementById('sendButton');
const typingIndicator = document.getElementById('typingIndicator');
const historySidebar = document.getElementById('historySidebar');
const chatHistoryList = document.getElementById('chatHistoryList');

function generateChatId() {
    return 'chat_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

function loadMessages(chatId = null) {
    chatMessages.innerHTML = '<div class="welcome-message">👋 Olá! Sou o PyBot, seu assistente inteligente. Como posso ajudá-lo hoje?</div>';
    const token = localStorage.getItem('token');
    
    if (token && !chatId) {
        fetchUserLogs();
    } else {
        const allChats = JSON.parse(localStorage.getItem('chatSessions') || '{}');
        const messages = chatId ? allChats[chatId] || [] : [];
        messages.forEach(msg => addMessage(msg.content, msg.sender));
    }
    updateChatHistory();
}

async function fetchUserLogs() {
    const token = localStorage.getItem('token');
    try {
        const decoded = JSON.parse(atob(token.split('.')[1]));
        const userId = decoded.user_id;
        const response = await fetch(`http://localhost:5000/api/logs/${userId}?limite=50`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        const data = await response.json();
        if (response.ok) {
            const sessions = {};
            data.forEach(log => {
                const sessionId = log.criado_em.split('T')[0]; // Agrupar por data
                if (!sessions[sessionId]) sessions[sessionId] = [];
                sessions[sessionId].push({ content: log.pergunta, sender: 'user' });
                sessions[sessionId].push({ content: log.resposta, sender: 'bot' });
            });
            localStorage.setItem('chatSessions', JSON.stringify(sessions));
            loadMessages();
        } else {
            console.error('Erro ao carregar logs:', data.error);
        }
    } catch (error) {
        console.error('Erro ao recuperar logs:', error);
    }
}

function saveMessage(content, sender) {
    const token = localStorage.getItem('token');
    if (!token) {
        let allChats = JSON.parse(localStorage.getItem('chatSessions') || '{}');
        const currentChatId = localStorage.getItem('currentChatId') || generateChatId();
        if (!allChats[currentChatId]) allChats[currentChatId] = [];
        allChats[currentChatId].push({ content, sender, timestamp: new Date().toISOString() });
        if (allChats[currentChatId].length > 50) {
            allChats[currentChatId] = allChats[currentChatId].slice(-50);
        }
        localStorage.setItem('chatSessions', JSON.stringify(allChats));
        localStorage.setItem('currentChatId', currentChatId);
        updateChatHistory();
    }
}

function updateChatHistory() {
    chatHistoryList.innerHTML = '';
    const token = localStorage.getItem('token');
    let sessions = {};
    
    if (token) {
        sessions = JSON.parse(localStorage.getItem('chatSessions') || '{}');
    } else {
        sessions = JSON.parse(localStorage.getItem('chatSessions') || '{}');
    }

    Object.keys(sessions).forEach(sessionId => {
        const li = document.createElement('li');
        li.textContent = `Chat ${sessionId.split('_')[1] || sessionId}`;
        li.onclick = () => loadMessages(sessionId);
        chatHistoryList.appendChild(li);
    });
}

function newChat() {
    chatMessages.innerHTML = '<div class="welcome-message">👋 Olá! Sou o PyBot, seu assistente inteligente. Como posso ajudá-lo hoje?</div>';
    const token = localStorage.getItem('token');
    if (!token) {
        localStorage.setItem('currentChatId', generateChatId());
    }
    chatInput.value = '';
    chatInput.style.height = 'auto';
    updateChatHistory();
}

function toggleHistory() {
    historySidebar.style.display = historySidebar.style.display === 'none' ? 'block' : 'none';
}

chatInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});

chatInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

async function sendMessage() {
    const message = chatInput.value.trim();
    if (!message) return;

    addMessage(message, 'user');
    saveMessage(message, 'user');
    chatInput.value = '';
    chatInput.style.height = 'auto';

    showTypingIndicator();

    try {
        const token = localStorage.getItem('token');
        const headers = {
            'Content-Type': 'application/json'
        };
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch('http://localhost:5000/api/query', {
            method: 'POST',
            headers: headers,
            body: JSON.stringify({ query: message })
        });

        const data = await response.json();

        hideTypingIndicator();

        if (response.ok && data.status === 'success') {
            const botResponse = `${data.response}${data.source ? ` (Fonte: ${data.source})` : ''}`;
            addMessage(botResponse, 'bot');
            saveMessage(botResponse, 'bot');
        } else {
            addMessage(`Erro: ${data.message || 'Falha ao processar a pergunta'}`, 'bot');
            saveMessage(`Erro: ${data.message || 'Falha ao processar a pergunta'}`, 'bot');
        }
    } catch (error) {
        hideTypingIndicator();
        addMessage('Erro: Não foi possível conectar ao servidor', 'bot');
        saveMessage('Erro: Não foi possível conectar ao servidor', 'bot');
        console.error('Erro ao enviar mensagem:', error);
    }
}

function addMessage(content, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;

    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.textContent = content;

    const messageTime = document.createElement('div');
    messageTime.className = 'message-time';
    messageTime.textContent = new Date().toLocaleTimeString('pt-BR', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });

    messageContent.appendChild(messageTime);
    
    if (sender === 'bot') {
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar bot-avatar';
        avatar.innerHTML = '<i class="fab fa-python"></i>';
        messageDiv.appendChild(avatar);
    }
    
    messageDiv.appendChild(messageContent);

    const welcomeMessage = chatMessages.querySelector('.welcome-message');
    if (welcomeMessage) {
        welcomeMessage.remove();
    }

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTypingIndicator() {
    typingIndicator.style.display = 'flex';
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function hideTypingIndicator() {
    typingIndicator.style.display = 'none';
}

function logout() {
    if (confirm('Tem certeza que deseja sair?')) {
        localStorage.removeItem('token');
        localStorage.removeItem('chatSessions');
        localStorage.removeItem('currentChatId');
        window.location.href = 'index.html';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    chatInput.focus();
    sendButton.addEventListener('click', sendMessage);
    loadMessages();

});
