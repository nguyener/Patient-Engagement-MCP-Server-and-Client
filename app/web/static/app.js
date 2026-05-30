async function sendMessage() {
  const input = document.getElementById("message-input");
  const chatBox = document.getElementById("chat-box");

  const message = input.value.trim();
  if (!message) return;

  chatBox.innerHTML += `<div class="user message">${message}</div>`;
  input.value = "";

  const response = await fetch("/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message })
  });

  const data = await response.json();

  chatBox.innerHTML += `<div class="bot message">${data.response}</div>`;
  chatBox.scrollTop = chatBox.scrollHeight;
}


document.getElementById("message-input").addEventListener("keydown", function(event) {
  if (event.key === "Enter") {
    sendMessage();
  }
});