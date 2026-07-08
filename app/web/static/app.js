function appendMessage(type, text) {
  const chatBox = document.getElementById("chat-box");
  const messageEl = document.createElement("div");

  messageEl.className = `${type} message`;
  messageEl.textContent = text;

  chatBox.appendChild(messageEl);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
  const input = document.getElementById("message-input");

  const message = input.value.trim();
  if (!message) return;

  appendMessage("user", message);
  input.value = "";

  const response = await fetch("/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message })
  });

  const data = await response.json();

  appendMessage("bot", data.response);
  loadContext();
}

async function loadContext() {
  const contextList = document.getElementById("context-list");
  contextList.innerHTML = "";

  try {
    const response = await fetch("/context");
    const data = await response.json();
    const contextBlocks = data.context || [];

    if (!contextBlocks.length) {
      const emptyEl = document.createElement("div");
      emptyEl.className = "context-empty";
      emptyEl.textContent = "No MCP context loaded.";
      contextList.appendChild(emptyEl);
      return;
    }

    contextBlocks.forEach((block) => {
      const itemEl = document.createElement("article");
      const metaEl = document.createElement("div");
      const contentEl = document.createElement("pre");

      itemEl.className = "context-item";
      metaEl.className = "context-meta";
      contentEl.className = "context-content";

      metaEl.textContent = `${block.server} · ${block.uri}`;
      contentEl.textContent = block.content;

      itemEl.appendChild(metaEl);
      itemEl.appendChild(contentEl);
      contextList.appendChild(itemEl);
    });
  } catch (error) {
    const errorEl = document.createElement("div");
    errorEl.className = "context-empty";
    errorEl.textContent = "Unable to load MCP context.";
    contextList.appendChild(errorEl);
  }
}

document.getElementById("message-input").addEventListener("keydown", function(event) {
  if (event.key === "Enter") {
    sendMessage();
  }
});

document.getElementById("refresh-context").addEventListener("click", loadContext);

loadContext();
