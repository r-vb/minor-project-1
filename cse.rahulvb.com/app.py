from flask import Flask, render_template, request, send_file, redirect, url_for, session
from gtts import gTTS
import os
from datetime import datetime
import requests
import json

app = Flask(__name__)
app.secret_key = '2z3fbosz7d952futyiyi'  # A secure secret key

# Yser credentials for demonstration purposes
valid_users = {
    "sdm": "sdm@cet",
    "rahul": "rahul071",
    "sairohitha": "sairohitha077",
    "sumedha": "sumedha107",
    "vaishnavi": "vaishnavi114",
    }

# Function to check user credentials
def check_credentials(username, password):
    return valid_users.get(username) == password

# Configuration for PDF to Text API
pdf_api_key = "YOUR_API_KEY"
pdf_api_host = "pdf-to-text-converter.p.rapidapi.com"
pdf_api_url = "https://pdf-to-text-converter.p.rapidapi.com/api/pdf-to-text/convert"

def convert_pdf_to_text(file_data, page):
    headers = {
        "X-RapidAPI-Key": pdf_api_key,
        "X-RapidAPI-Host": pdf_api_host,
    }

    payload = {"page": page}
    
    response = requests.post(pdf_api_url, headers=headers, data=payload, files=file_data)

    if response.status_code == 200:
        try:
            # Try to parse the response as JSON
            parsed_response = response.json()
            # If successful, format as JSON
            formatted_response = json.dumps(parsed_response, indent=2)
            print(formatted_response)
            return formatted_response
        except ValueError:
            # If parsing as JSON fails, treat it as plain text
            return response.text
    else:
        return render_template('index.html', error = 'Failed to convert PDF. Our servers are down!')
        # return {"error": f"Failed to convert PDF. Status code: {response.status_code}, Response: {response.text}"}

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if 'username' in session:
        return redirect(url_for('index'))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if check_credentials(username, password):
            session['username'] = username  # Store username in session
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html", error=None)

# Logout route
@app.route("/logout")
def logout():
    session.pop('username', None)  # Remove the username from the session
    return redirect(url_for('login'))

# Main index route
@app.route("/", methods=["GET", "POST"])
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == "POST":
        if "file" in request.files:
            # PDF file is chosen
            file = request.files["file"]
            page = request.form.get("page", 1)

            file_data = {"file": (file.filename, file.read())}
            result = convert_pdf_to_text(file_data, page)
            return render_template("index.html", result=result)
        else:
            # Non-PDF file is chosen, perform text-to-speech conversion
            text = request.form['text']
            language = request.form['language']

            # Check if the text indicates a failed PDF conversion
            if "Failed to convert PDF. Select a valid PDF!" not in text:
                # Perform text-to-speech conversion
                tts = gTTS(text=text, lang=language, slow=False)
            else:
                # Handle the case where the text indicates a failed PDF conversion
                return "Failed to convert PDF. Select a valid PDF!"
            
            # Generate a unique filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            file_path = f'static/converted-file-{timestamp}.mp3'

            tts.save(file_path)

            return render_template('index.html', audio_path=file_path, os=os)

    return render_template("index.html", result=None)

# Route to display generated audio files
@app.route('/show_files')
def show_files():
    if 'username' not in session:
        return redirect(url_for('login'))

    static_folder = 'static'
    audio_files = [f for f in os.listdir(static_folder) if f.endswith('.mp3')]
    return render_template('show_files.html', audio_files=audio_files)

# Route to play an audio file
@app.route('/play/<filename>')
def play_file(filename):
    if 'username' not in session:
        return redirect(url_for('login'))

    file_path = os.path.join('static', filename)
    return send_file(file_path, mimetype='audio/mp3')

# Route to download an audio file
@app.route('/download/<filename>')
def download_file(filename):
    if 'username' not in session:
        return redirect(url_for('login'))

    file_path = os.path.join('static', filename)
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
