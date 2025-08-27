document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".sign-up form");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const nome = form.querySelector('input[placeholder="Name"]').value;
        const email = form.querySelector('input[type="email"]').value;
        const senha = form.querySelector('input[placeholder="Senha"]').value;

        try {
            const response = await fetch("http://localhost:5000/api/users/create", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ nome, email, senha })
            });

            const data = await response.json();

            if (response.ok) {
                alert("✅ Cadastro realizado com sucesso!");
                window.location.href = "login.html"; // redireciona pro login
            } else {
                alert("❌ Erro: " + (data.erro || "Falha no cadastro"));
            }
        } catch (error) {
            alert("Erro de conexão com o servidor");
            console.error(error);
        }
    });
});
