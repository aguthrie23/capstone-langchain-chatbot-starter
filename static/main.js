
function sendMessage() {
    let messageInput = document.getElementById('message-input');
    let message = messageInput.value.trim();
    if (!message) return;
    displayMessage('user', message);

    let functionSelect = document.getElementById('function-select');
    let selectedFunction = functionSelect.value;
    let xhr = new XMLHttpRequest();
    let url;
    switch (selectedFunction) {
        case 'search': url = '/search'; break;
        case 'kbanswer': url = '/kbanswer'; break;
        case 'answer': url = '/answer'; break;
        default: url = '/answer';
    }
    xhr.open('POST', url);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (xhr.status === 200) {
            let response = JSON.parse(xhr.responseText);
            displayMessage('assistant', response.message);
        }
    };
    xhr.send(JSON.stringify({message: message}));
    messageInput.value = '';
    messageInput.focus();
}

function displayMessage(sender, message) {
    let chatContainer = document.getElementById('chat-container');
    let messageDiv = document.createElement('div');
    messageDiv.classList.add(sender === 'assistant' ? 'assistant-message' : 'user-message');
    let label = sender === 'assistant' ? 'Chatbot' : 'You';
    let textDiv = document.createElement('div');
    textDiv.innerHTML = '<strong>' + label + ':</strong> ' + (sender === 'assistant' ? message : escapeHtml(message));
    messageDiv.appendChild(textDiv);
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function escapeHtml(text) {
    var map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}

function clearChat() {
    let chatContainer = document.getElementById('chat-container');
    chatContainer.innerHTML = '';
}

// Button and input event listeners
document.getElementById('send-btn').addEventListener('click', sendMessage);
document.getElementById('clear-btn').addEventListener('click', clearChat);
document.getElementById('message-input').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') sendMessage();
});
