# pylint: skip-file
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt

# Load environment variables from the .env file
env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage")

# Define the HTML code for the speech recognition interface.
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = 'LANGUAGE_PLACEHOLDER';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            if (recognition) {
                recognition.stop();
            }
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

# Replace the language placeholder with the actual language
HtmlCode = HtmlCode.replace('LANGUAGE_PLACEHOLDER', InputLanguage)

# Use consistent file path
html_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Data", "Voice.html"))

# Write the modified HTML code to a file
with open(html_file_path, "w") as f:
    f.write(HtmlCode)

print(f"HTML file created at: {html_file_path}")

# Set chrome options for the WebDriver
chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")

# Initialize the Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Define the path for temporary files
TempDirPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Frontend", "Files"))

def SetAssistantStatus(Status):
    os.makedirs(TempDirPath, exist_ok=True)
    with open(os.path.join(TempDirPath, "Status.data"), "w", encoding='utf-8') as file:
        file.write(Status)

def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how","what","who","where","when","why","which","whose","whom","can you","what's","where's","how's"]

    if any(new_query.startswith(word + " ") for word in question_words):
        if query_words[-1][-1] in ['.','?','!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['.','?','!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."

    return new_query.capitalize()

def UniversalTranslator(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

def SpeechRecognition():
    # Open the HTML file in the browser
    driver.get(f"file:///{html_file_path}")

    # Wait for the page to load and the start button to be present
    wait = WebDriverWait(driver, 10)
    start_button = wait.until(EC.presence_of_element_located((By.ID, "start")))

    # Click the start button
    start_button.click()

    while True:
        try:
            # Get the recognized text from the HTML output element
            Text = driver.find_element(by=By.ID, value="output").text

            if Text:
                # Stop recognition by clicking the stop button
                driver.find_element(by=By.ID, value="end").click()

                # If the input language is English, return the modified query
                if InputLanguage and (InputLanguage.lower() == "en" or "en" in InputLanguage.lower()):
                    return QueryModifier(Text)
                else:
                    # If the input language is not English, translate the text and return it
                    SetAssistantStatus("Translating...")
                    return QueryModifier(UniversalTranslator(Text))

        except Exception as e:
            pass

# Main execution block
if __name__ == "__main__":
    try:
        while True:
            # Continuously perform speech recognition and print the recognized text
            Text = SpeechRecognition()
            print(Text)
    except KeyboardInterrupt:
        driver.quit()
        print("Script stopped by user")
    except Exception as e:
        print(f"Error: {e}")
        driver.quit()