from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# Serve static files
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Speech App</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .container { margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
            button { padding: 10px 15px; margin: 5px; cursor: pointer; }
            textarea { width: 100%; height: 100px; margin: 10px 0; }
            #status { color: #666; font-style: italic; }
        </style>
    </head>
    <body>
        <h1>Speech to Text & Text to Speech</h1>
        
        <div class="container">
            <h2>Speech to Text</h2>
            <button id="startBtn">Start Recording</button>
            <p id="status">Click the button to start recording</p>
            <textarea id="transcript" placeholder="Your speech will appear here..." readonly></textarea>
            <button id="copyBtn">Copy to Clipboard</button>
        </div>
        
        <div class="container">
            <h2>Text to Speech</h2>
            <textarea id="textToSpeak" placeholder="Enter text to speak..."></textarea>
            <div>
                <button id="speakBtn">Speak</button>
                <button id="stopBtn">Stop</button>
            </div>
        </div>

        <script>
            // Speech to Text
            const startBtn = document.getElementById('startBtn');
            const status = document.getElementById('status');
            const transcript = document.getElementById('transcript');
            const copyBtn = document.getElementById('copyBtn');
            
            // Text to Speech
            const speakBtn = document.getElementById('speakBtn');
            const stopBtn = document.getElementById('stopBtn');
            const textToSpeak = document.getElementById('textToSpeak');
            
            // Check for browser support
            if (!('webkitSpeechRecognition' in window) || !('speechSynthesis' in window)) {
                status.textContent = "This app requires a modern browser like Chrome or Edge.";
                startBtn.disabled = true;
                speakBtn.disabled = true;
                stopBtn.disabled = true;
            }
            
            // Speech Recognition
            if ('webkitSpeechRecognition' in window) {
                const recognition = new webkitSpeechRecognition();
                recognition.continuous = true;
                recognition.interimResults = true;
                recognition.lang = 'en-US';
                
                startBtn.onclick = function() {
                    if (startBtn.textContent === 'Start Recording') {
                        recognition.start();
                        startBtn.textContent = 'Stop Recording';
                        status.textContent = 'Listening...';
                        startBtn.style.backgroundColor = '#ff6b6b';
                    } else {
                        recognition.stop();
                        startBtn.textContent = 'Start Recording';
                        status.textContent = 'Click the button to start recording';
                        startBtn.style.backgroundColor = '';
                    }
                };
                
                recognition.onresult = function(event) {
                    let finalTranscript = '';
                    let interimTranscript = '';
                    
                    for (let i = event.resultIndex; i < event.results.length; i++) {
                        const transcript = event.results[i][0].transcript;
                        if (event.results[i].isFinal) {
                            finalTranscript += transcript;
                        } else {
                            interimTranscript += transcript;
                        }
                    }
                    
                    transcript.value = finalTranscript + interimTranscript;
                };
                
                recognition.onerror = function(event) {
                    console.error('Speech recognition error:', event.error);
                    status.textContent = 'Error: ' + event.error;
                    startBtn.textContent = 'Start Recording';
                    startBtn.style.backgroundColor = '';
                };
                
                // Text to Speech
                const synth = window.speechSynthesis;
                let utterance = null;
                
                speakBtn.onclick = function() {
                    if (!textToSpeak.value.trim()) {
                        alert('Please enter some text to speak');
                        return;
                    }
                    
                    // Stop any ongoing speech
                    synth.cancel();
                    
                    // Create new utterance
                    utterance = new SpeechSynthesisUtterance(textToSpeak.value);
                    
                    // Speak the text
                    synth.speak(utterance);
                    
                    // Update button states
                    speakBtn.disabled = true;
                    stopBtn.disabled = false;
                };
                
                stopBtn.onclick = function() {
                    synth.cancel();
                    speakBtn.disabled = false;
                    stopBtn.disabled = true;
                };
                
                // Re-enable buttons when speech ends
                utterance = new SpeechSynthesisUtterance();
                utterance.onend = function() {
                    speakBtn.disabled = false;
                    stopBtn.disabled = true;
                };
                
                // Copy to clipboard
                copyBtn.onclick = function() {
                    transcript.select();
                    document.execCommand('copy');
                    const originalText = copyBtn.textContent;
                    copyBtn.textContent = 'Copied!';
                    setTimeout(() => {
                        copyBtn.textContent = originalText;
                    }, 2000);
                };
            }
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    # Create static directory if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')
    
    # Run the app
    app.run(host='0.0.0.0', port=5000, debug=True)
