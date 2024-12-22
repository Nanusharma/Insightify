// DOM Elements
const elements = {
    url: document.getElementById('url'),
    analyze: document.getElementById('analyze'),
    summary: document.getElementById('summary'),
    summaryText: document.getElementById('summaryText'),
    chatSection: document.getElementById('chatSection'),
    chatContainer: document.getElementById('chatContainer'),
    userInput: document.getElementById('userInput'),
    sendMessage: document.getElementById('sendMessage'),
    status: document.getElementById('status')
};

// Event Listeners
elements.analyze.addEventListener('click', analyzeWebsite);
elements.sendMessage.addEventListener('click', sendMessage);
elements.userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

// Utility Functions
function setStatus(message, isError = false) {
    elements.status.textContent = message;
    elements.status.style.color = isError ? 'red' : 'var(--gray-700)';
}

function addMessage(message, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    messageDiv.textContent = message;
    elements.chatContainer.appendChild(messageDiv);
    elements.chatContainer.scrollTop = elements.chatContainer.scrollHeight;
}

// Main Functions
async function analyzeWebsite() {
    try {
        const url = elements.url.value.trim();

        if (!url) {
            throw new Error('Please enter a website URL');
        }

        setStatus('Analyzing website...');
        elements.analyze.disabled = true;

        const response = await fetch('/analyze-website', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to analyze website');
        }

        elements.summaryText.textContent = data.summary;
        elements.summary.style.display = 'block';
        elements.chatSection.style.display = 'block';
        
        setStatus('Ready for questions');
    } catch (error) {
        setStatus(error.message, true);
    } finally {
        elements.analyze.disabled = false;
    }
}

async function sendMessage() {
    try {
        const userMessage = elements.userInput.value.trim();
        if (!userMessage) return;

        elements.userInput.value = '';
        elements.sendMessage.disabled = true;
        addMessage(userMessage, true);

        const response = await fetch('/chat-message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: userMessage,
                url: elements.url.value.trim()
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to get response');
        }

        addMessage(data.response);
    } catch (error) {
        setStatus(error.message, true);
    } finally {
        elements.sendMessage.disabled = false;
    }
}