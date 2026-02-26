/**
 * Smart Hospital Queue – Frontend JavaScript
 */

// Live clock
function updateClock() {
    const now = new Date();
    const timeStr = now.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
    const el = document.getElementById('live-clock');
    if (el) el.textContent = timeStr;
}

setInterval(updateClock, 1000);
updateClock();

// Auto-refresh queue page every 30 seconds
if (window.location.pathname.includes('/queue')) {
    setTimeout(() => {
        window.location.reload();
    }, 30000);
}

// Tooltips
document.addEventListener('DOMContentLoaded', function() {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipTriggerList.forEach(el => new bootstrap.Tooltip(el));
    
    // Initialize chatbot
    initChatbot();
});

// ===== Chatbot Functionality =====
function initChatbot() {
    const chatbotButton = document.getElementById('chatbot-button');
    const chatbotWindow = document.getElementById('chatbot-window');
    const chatbotClose = document.getElementById('chatbot-close');
    const chatbotInput = document.getElementById('chatbot-input');
    const chatbotSend = document.getElementById('chatbot-send');
    const chatbotMessages = document.getElementById('chatbot-messages');
    
    if (!chatbotButton) return;
    
    // Toggle chatbot window
    chatbotButton.addEventListener('click', () => {
        chatbotWindow.classList.toggle('active');
        if (chatbotWindow.classList.contains('active')) {
            chatbotInput.focus();
            // Send greeting if first time
            if (chatbotMessages.children.length === 0) {
                sendMessage('Hello');
            }
        }
    });
    
    chatbotClose.addEventListener('click', () => {
        chatbotWindow.classList.remove('active');
    });
    
    // Send message on button click
    chatbotSend.addEventListener('click', () => {
        const message = chatbotInput.value.trim();
        if (message) {
            sendMessage(message);
            chatbotInput.value = '';
        }
    });
    
    // Send message on Enter key
    chatbotInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const message = chatbotInput.value.trim();
            if (message) {
                sendMessage(message);
                chatbotInput.value = '';
            }
        }
    });
}

function sendMessage(message) {
    const chatbotMessages = document.getElementById('chatbot-messages');
    const chatbotSend = document.getElementById('chatbot-send');
    
    // Add user message
    addChatMessage(message, 'user');
    
    // Show typing indicator
    showTypingIndicator();
    
    // Disable send button
    chatbotSend.disabled = true;
    
    // Send to backend
    fetch('/chatbot/message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            message: message,
            context: {}
        })
    })
    .then(response => response.json())
    .then(data => {
        // Remove typing indicator
        hideTypingIndicator();
        
        // Add bot response
        addChatMessage(data.response, 'bot', data.suggestions);
        
        // Enable send button
        chatbotSend.disabled = false;
    })
    .catch(error => {
        console.error('Chatbot error:', error);
        hideTypingIndicator();
        addChatMessage('Sorry, I encountered an error. Please try again.', 'bot');
        chatbotSend.disabled = false;
    });
}

function addChatMessage(text, sender, suggestions = []) {
    const chatbotMessages = document.getElementById('chatbot-messages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${sender}`;
    
    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'message-bubble';
    bubbleDiv.textContent = text;
    
    messageDiv.appendChild(bubbleDiv);
    
    // Add suggestions if provided
    if (suggestions && suggestions.length > 0) {
        const suggestionsDiv = document.createElement('div');
        suggestionsDiv.className = 'chat-suggestions';
        
        suggestions.forEach(suggestion => {
            const btn = document.createElement('button');
            btn.className = 'suggestion-btn';
            btn.textContent = suggestion;
            btn.onclick = () => {
                sendMessage(suggestion);
            };
            suggestionsDiv.appendChild(btn);
        });
        
        messageDiv.appendChild(suggestionsDiv);
    }
    
    chatbotMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
}

function showTypingIndicator() {
    const chatbotMessages = document.getElementById('chatbot-messages');
    
    const typingDiv = document.createElement('div');
    typingDiv.className = 'chat-message bot';
    typingDiv.id = 'typing-indicator';
    
    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'message-bubble typing-indicator';
    bubbleDiv.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';
    
    typingDiv.appendChild(bubbleDiv);
    chatbotMessages.appendChild(typingDiv);
    
    // Scroll to bottom
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
}

function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}
