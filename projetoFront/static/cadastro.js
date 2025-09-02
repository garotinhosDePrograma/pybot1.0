document.addEventListener("DOMContentLoaded", () => {
    const bootScreen = document.getElementById('bootScreen');
    const bootMessagesContainer = document.getElementById('bootMessages');
    const successScreen = document.getElementById('successScreen');
    const container = document.getElementById('container');
    const progressBar = document.getElementById('progressBar');

    const bootMessages = [
        "Verificando integridade do PyBot...",
        "Carregando módulos de autenticação...",
        "Inicializando conexão com o backend...",
        "Conectando ao servidor https://pygre.onrender.com...",
        "Validando credenciais do usuário...",
        "Sincronizando configurações do sistema...",
        "Otimizando performance do login...",
        "Finalizando autenticação..."
    ];

    function startBootSequence(nome, email, senha, callback) {
        bootScreen.style.display = 'flex';
        container.style.display = 'none';
        
        displayBootMessages(nome, email, senha, callback);
    }

    function displayBootMessages(nome, email, senha, callback) {
        let messageIndex = 0;
        
        function showNextMessage() {
            if (messageIndex < bootMessages.length) {
                const messageDiv = document.createElement('div');
                messageDiv.className = 'message';
                messageDiv.textContent = `[${new Date().toLocaleTimeString()}] ${bootMessages[messageIndex]}`;
                bootMessagesContainer.appendChild(messageDiv);
                
                bootMessagesContainer.scrollTop = bootMessagesContainer.scrollHeight;
                
                messageIndex++;
                setTimeout(showNextMessage, 400);
            } else {
                setTimeout(() => showSuccessScreen(nome, email, senha, callback), 1000);
            }
        }
        
        showNextMessage();
    }

    function showSuccessScreen(nome, email, senha, callback) {
        const bootText = document.querySelector('.boot-text');
        const progressContainer = document.querySelector('.progress-container');
        
        bootMessagesContainer.style.display = 'none';
        bootText.style.display = 'none';
        progressContainer.style.display = 'none';
        
        successScreen.style.display = 'block';
        
        setTimeout(() => callback(nome, email, senha), 2000);
    }

    async function processLogin(nome, email, senha) {
        try {
            const response = await fetch("https://pygre.onrender.com/api/cadastro", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ nome, email, senha })
            });

            const data = await response.json();

            if (response.ok) {
                alert("Cadastro realizado com sucesso!");
                localStorage.setItem("token", data.token);
                window.location.href = "bot.html";
            } else {
                alert("Erro: " + (data.error || "Falha no cadastro"));
                resetToLogin();
            }
        } catch (error) {
            alert("Erro de conexão com o servidor");
            console.error(error);
            resetToLogin();
        }
    }

    function resetToLogin() {
        bootScreen.style.display = 'none';
        container.style.display = 'block';
        
        bootMessagesContainer.innerHTML = '';
        bootMessagesContainer.style.display = 'block';
        document.querySelector('.boot-text').style.display = 'block';
        document.querySelector('.progress-container').style.display = 'block';
        successScreen.style.display = 'none';
        progressBar.style.animation = 'none';
        progressBar.offsetHeight;
        progressBar.style.animation = '';
    }

    const form = document.getElementById("cadastroForm");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const nome = form.querySelector('input[placeholder="Name"]').value;
        const email = form.querySelector('input[type="email"]').value;
        const senha = form.querySelector('input[type="password"]').value;

        startBootSequence(nome, email, senha, processLogin);
    });
});
