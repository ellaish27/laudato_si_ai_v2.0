document.addEventListener('DOMContentLoaded', function() {
    // Chat functionality
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    
    // Impact calculator functionality
    const pollutionSlider = document.getElementById('pollution');
    const waterSlider = document.getElementById('water');
    const wasteSlider = document.getElementById('waste');
    const pollutionValue = document.getElementById('pollution-value');
    const waterValue = document.getElementById('water-value');
    const wasteValue = document.getElementById('waste-value');
    const evaluateBtn = document.getElementById('evaluate-btn');
    const resultContainer = document.getElementById('result');
    
    // Update slider values
    pollutionSlider.addEventListener('input', function() {
        pollutionValue.textContent = this.value;
    });
    
    waterSlider.addEventListener('input', function() {
        waterValue.textContent = this.value;
    });
    
    wasteSlider.addEventListener('input', function() {
        wasteValue.textContent = this.value;
    });
    
    // Send message on button click
    sendBtn.addEventListener('click', sendMessage);
    
    // Send message on Enter key
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Evaluate impact
    evaluateBtn.addEventListener('click', evaluateImpact);
    
    function sendMessage() {
        const message = userInput.value.trim();
        if (message === '') return;
        
        // Add user message to chat
        addMessage(message, 'user-message');
        userInput.value = '';
        
        // Send to server and get response
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            addMessage(data.response, 'bot-message');
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('Sorry, there was an error processing your request.', 'bot-message');
        });
    }
    
    function addMessage(text, className) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${className}`;
        messageDiv.innerHTML = `<p>${text}</p>`;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function evaluateImpact() {
        const pollution = parseFloat(pollutionSlider.value);
        const water = parseFloat(waterSlider.value);
        const waste = parseFloat(wasteSlider.value);
        
        // Send to server for evaluation
        fetch('/evaluate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                pollution: pollution,
                water: water,
                waste: waste
            })
        })
        .then(response => response.json())
        .then(data => {
            displayResult(data.urgency, data.message);
        })
        .catch(error => {
            console.error('Error:', error);
            resultContainer.textContent = 'Error evaluating impact. Please try again.';
            resultContainer.style.backgroundColor = '#ff6b6b';
            resultContainer.style.color = 'white';
        });
    }
    
    function displayResult(urgency, message) {
        resultContainer.textContent = message;
        
        // Set color based on urgency level
        if (urgency <= 0.3) {
            resultContainer.style.backgroundColor = '#90ee90';
            resultContainer.style.color = '#1a5c38';
        } else if (urgency <= 0.6) {
            resultContainer.style.backgroundColor = '#ffcc00';
            resultContainer.style.color = '#333333';
        } else {
            resultContainer.style.backgroundColor = '#ff6b6b';
            resultContainer.style.color = 'white';
        }
        
        // Add animation
        resultContainer.style.transform = 'scale(0.95)';
        setTimeout(() => {
            resultContainer.style.transform = 'scale(1)';
        }, 200);
    }
});
