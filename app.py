from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Load the neural network model
try:
    with open('laudato_memory.pkl', 'rb') as f:
        model_data = pickle.load(f)
    weights = model_data.get('weights', np.random.rand(3, 1))
    biases = model_data.get('biases', np.random.rand(1))
except:
    # Default model if no saved data exists
    weights = np.random.rand(3, 1)
    biases = np.random.rand(1)

# Laudato Si quotes
quotes = [
    "The Earth is our common home and we must care for it.",
    "Everything is connected. Concern for nature must be joined to justice for the poor.",
    "We need to hear both the cry of the earth and the cry of the poor.",
    "Many things have to change course, but it is we human beings above all who need to change.",
    "Nature cannot be regarded as something separate from ourselves or as a mere setting in which we live."
]

@app.route('/')
def index():
    return render_template('index.html', quote=quotes[np.random.randint(0, len(quotes))])

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    
    # Simple response logic (in a real app, this would use the AI model)
    if 'help' in user_input.lower() or 'planet' in user_input.lower():
        response = "Reduce waste, plant trees, conserve water 🌿"
    elif 'pollution' in user_input.lower():
        response = "Pollution harms creation 🌀 — urgent action is needed."
    elif 'nature' in user_input.lower() or 'care' in user_input.lower():
        response = "Because we are interconnected with all of creation 🌍"
    else:
        response = "I'm here to help with environmental and ethical questions. How can I assist you today?"
    
    return jsonify({'response': response})

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.json
    pollution = float(data.get('pollution', 0))
    water = float(data.get('water', 0))
    waste = float(data.get('waste', 0))
    
    # Neural network calculation
    inputs = np.array([[pollution, water, waste]])
    hidden = np.dot(inputs, weights) + biases
    output = 1 / (1 + np.exp(-hidden))  # Sigmoid activation
    urgency = float(output[0][0])
    
    # Determine message based on urgency
    if urgency <= 0.3:
        message = "You're doing well! Maintain simplicity 🌿"
    elif urgency <= 0.6:
        message = "Reduce. Rethink your impact. 🌀"
    else:
        message = "Urgent change needed. Act now. 🔥"
    
    return jsonify({
        'urgency': urgency,
        'message': message
    })

if __name__ == '__main__':
    app.run(debug=True)
