import google.generativeai as genai
import os


from dotenv import load_dotenv

# Load environment variables
load_dotenv('C:/Users/acer/Desktop/New folder/.env')

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
print(os.getenv("GEMINI_API_KEY"))
# Load Wikipedia data
wikipedia_data = ""
try:
    with open("wikipedia_data.txt", "r") as file:
        wikipedia_data = file.read()
except FileNotFoundError:
    print("Error: file not found")
    exit(1)

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
        return "I am having trouble."

def chat():
    print("Hello! I am your AI Chatbot DJINN. Type 'exit' to end.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break
        
        # First, use Gemini API
        gemini_response = get_gemini_response(user_input)
        print("DJINN:", gemini_response)
        
        # Then, check Wikipedia data
        wikipedia_response = get_wikipedia_response(user_input)
        if wikipedia_response:
            print("Chatbot (Wikipedia):", wikipedia_response)

if __name__ == "__main__":
    chat()