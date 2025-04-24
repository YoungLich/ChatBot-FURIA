function enviarMensagem() {
  const input = document.getElementById("userInput");
  const mensagem = input.value.trim();

  if (!mensagem) return;

  // Adiciona a mensagem do usuário ao histórico
  adicionarMensagem('user', mensagem);

  fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ mensagem })
  })
  .then(res => res.json())
  .then(data => {
    adicionarMensagem('bot', data.resposta);
    input.value = "";
  })
  .catch(err => {
    adicionarMensagem('bot', "Erro ao se comunicar com a IA.");
    console.error(err);
  });
}

function adicionarMensagem(tipo, texto) {
  const chatHistory = document.getElementById("chatHistory");

  const message = document.createElement("div");
  message.classList.add("message", tipo);

  const avatar = document.createElement("img");
  avatar.src = tipo === "user"
    ? "/static/image/user-icon.png"
    : "/static/image/mini-logo.png";
  avatar.alt = tipo === "user" ? "Usuário" : "FURIA";

  const textDiv = document.createElement("div");
  textDiv.classList.add("text");

  // Usando innerHTML para permitir que os links sejam clicáveis
  textDiv.innerHTML = texto;

  message.appendChild(avatar);
  message.appendChild(textDiv);
  chatHistory.appendChild(message);

  chatHistory.scrollTop = chatHistory.scrollHeight; // Scroll automático para o final
}
