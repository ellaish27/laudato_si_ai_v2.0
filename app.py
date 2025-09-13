from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import os
import requests

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

def huggingface_chat(user_input):
    # Use your Hugging Face API key stored in an environment variable
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {
        "Authorization": f"Bearer {os.getenv('HF_API_KEY')}"
    }
    payload = {
        "inputs": f"User: {user_input}\nAssistant:",
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.7,
            "return_full_text": False  # don't echo the prompt
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        # Debug log
        print("HuggingFace raw response:", data)

        # Extract reply
        if isinstance(data, list) and len(data) > 0 and 'generated_text' in data[0]:
            reply = data[0]['generated_text'].strip()
            # Remove leftover "Assistant:" tags if present
            reply = reply.replace("Assistant:", "").strip()
            return reply
        else:
            return "The AI did not return a valid response."
    except Exception as e:
        print(f"HuggingFace API error: {str(e)}")
        return "Error connecting to the AI service."


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    response = huggingface_chat(user_input)
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
