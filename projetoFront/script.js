const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const sendButton = document.getElementById('sendButton');
const typingIndicator = document.getElementById('typingIndicator');

// Auto-resize textarea
chatInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});

// Send message on Enter (but allow Shift+Enter for new line)
chatInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

function sendMessage() {
    const message = chatInput.value.trim();
    if (!message) return;

    // Add user message
    addMessage(message, 'user');
    chatInput.value = '';
    chatInput.style.height = 'auto';

    // Here you would send the message to your backend API
    // Example: fetch('/api/chat', { method: 'POST', body: JSON.stringify({message}) })
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

    // Remove welcome message if it exists
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
        window.location.href = 'login.html';
    }
}

// Focus on input when page loads
document.addEventListener('DOMContentLoaded', function() {
    chatInput.focus();
});