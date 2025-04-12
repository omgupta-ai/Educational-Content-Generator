import groq
import os
from flask import Flask, render_template_string, request
from dotenv import load_dotenv

load_dotenv()

groq.api_key = os.environ["GROQ_API_KEY"]

def generate_roadmap(course_title):
    response = groq.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": f"Generate comprehensive educational content for the course titled '{course_title}'. Ensure to include an engaging introduction, covering the history, significance, and applications of the topic, followed by detailed information about course objectives, sample syllabus, measurable learning outcomes, assessment methods, and recommended readings. Utilize a variety of examples and visuals to enhance understanding."}
        ]
    )
    return response["choices"][0]["message"]["content"]


app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])

# This code defines a function that generates a roadmap based on user input obtained through a POST request.
def hello():
  output = ""
  if request.method == 'POST':
    components = request.form['components']
    output = generate_roadmap(components)
  return render_template_string('''

<!DOCTYPE html>
<html>
<head>
    <title>Educational Content Generator</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-image: linear-gradient(to right, #f6d365 0%, #fda085 100%);
            background-color: #f8f9fa; /* Light gray background */
            font-family: Arial, sans-serif;
        }
        .container {
            margin-top: 50px;
            border: 1px solid #000000;
            padding: 20px 20px 20px  20px;
        }
        .card {
            border: 1px solid #ced4da; 
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Shadow */
        }
        .card-header {
            background-color: #007bff; /* Primary color */
            color: white; /* Text color */
        }
        .btn {
            transition: all 0.3s ease-in-out; /* Smooth button transition */
        }
        .btn:hover {
            transform: translateY(-2px); /* Move button up on hover */
        }
    </style>
    <script>
        async function generate_roadmap() {
            const components = document.querySelector('#components').value;
            const output = document.querySelector('#output');
            output.textContent = 'Generating roadmap for you...';
            const response = await fetch('/generate', {
                method: 'POST',
                body: new FormData(document.querySelector('#tutorial-form'))
            });
            const newOutput = await response.text();
            output.textContent = newOutput;
        }
        function copyToClipboard() {
            const output = document.querySelector('#output');
            const textarea = document.createElement('textarea');
            textarea.value = output.textContent;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);
            alert('Copied to clipboard');
        }
    </script>
</head>
<body>
<div class="container">
    <h1 class="my-4">Educational Content Generator</h1>
    <form id="tutorial-form" onsubmit="event.preventDefault(); generate_roadmap();" class="mb-3">
        <div class="mb-3">
            <label for="components" class="form-label">Titles/Topics:</label>
            <input type="text" class="form-control" id="components" name="components" placeholder="Enter the topics or titles e.g. Machine Learning, Computer Networks etc." required>
        </div>
        <button type="submit" class="btn btn-primary">Show me a roadmap</button>
    </form>
    <div class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
            Output:
            <button class="btn btn-secondary btn-sm" onclick="copyToClipboard()">Copy</button>
        </div>
        <div class="card-body">
            <pre id="output" class="mb-0" style="white-space: pre-wrap;">{{ output }}</pre>
        </div>
    </div>
</div>
</body>
</html>


 ''',
                                output=output)


@app.route('/generate', methods=['POST'])

def generate():
  components = request.form['components']
  return generate_roadmap(components)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)
