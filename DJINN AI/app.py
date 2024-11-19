from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('C:/Users/acer/Desktop/New folder/.env')

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load Wikipedia data
wikipedia_data = ""
try:
    with open("wikipedia_data.txt", "r") as file:
        wikipedia_data = file.read()
except FileNotFoundError:
    print("Error: file not found")
    exit(1)

# Flask app setup
app = Flask(__name__)

def get_wikipedia_response(user_input):
    for line in wikipedia_data.splitlines():
        if user_input.lower() in line.lower():
            return line
    return None  

def get_gemini_response(user_input):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(user_input)
        return response._result.candidates[0].content.parts[0].text
    except Exception as e:
        print("Error communicating with Gemini:", e)
        return "I am having trouble responding at the moment."

@app.route("/")
def index():
    return render_template("index(1).html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("user_input", "")
    if not user_input:
        return jsonify({"error": "No input provided"}), 400
    
    # Get responses
    gemini_response = get_gemini_response(user_input)
    wikipedia_response = get_wikipedia_response(user_input)
    
    return jsonify({
        "gemini_response": gemini_response,
        "wikipedia_response": wikipedia_response
    })

if __name__ == "__main__":
    app.run(debug=False)
