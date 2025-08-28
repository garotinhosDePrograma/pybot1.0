document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".sign-in form");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = form.querySelector('input[type="email"]').value;
        const senha = form.querySelector('input[type="password"]').value;

        try {
            const response = await fetch("http://127.0.0.1:5000/api/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email, senha })
            });

            const data = await response.json();

            if (response.ok) {
                alert("Login realizado com sucesso!");
                localStorage.setItem("token", data.token);
                window.location.href = "bot.html";
            } else {
                alert("Erro: " + (data.error || "Falha no login"));
            }
        } catch (error) {
            alert("Erro de conexão com o servidor");
            console.error(error);
        }
    });

});
