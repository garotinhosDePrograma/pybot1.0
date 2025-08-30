document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".sign-up form");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const nome = form.querySelector('input[placeholder="Name"]').value;
        const email = form.querySelector('input[type="email"]').value;
        const senha = form.querySelector('input[type="password"]').value;

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
                window.location.href = "index.html";
            } else {
                alert("Erro: " + (data.error || "Falha no cadastro"));
            }
        } catch (error) {
            alert("Erro de conexão com o servidor");
            console.error(error);
        }
    });
});
