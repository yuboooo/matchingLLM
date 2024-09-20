import os
import sys
from flask import Flask, flash, request, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import logging
import json
import redis

from algorithms.stable_matching import gale_shapley
from algorithms.profile import generate_random_preference_profile, profile_formatting
from algorithms.LLMs import generate_prompt, gpt4_matching, claude_matching



logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('HELLO WORLD')

app = Flask(__name__, static_folder='static')
CORS(app)
cache = redis.Redis(host='localhost', port=6379, db=0)





directory = 'uploads/test_docs'

UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

@app.route('/home', methods=['GET'])
def home():
    return "Hello World"


@app.route('/upload', methods=['POST'])
def file_upload():
    # Step 1: Inspect the file existence and name
    if 'file' not in request.files:
        print("No file part")
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        print("No selected file")
        return "No selected file", 400

    # Step 2: Store the file
    if file:
        filename = secure_filename(file.filename)
        upload_folder = './uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        # Step 3: Save the content for later use
        file_content = file.read()  # This reads the file content into a variable
        print(file_content)
        
        # Save the file to disk
        file_path = os.path.join(upload_folder, filename)
        with open(file_path, 'wb') as f:
            f.write(file_content)

        # Step 4: Return the content
        print(f"File {filename} uploaded successfully, and content stored in variable")
        return file_content.decode('utf-8'), 200  # Return the content (converted to string)
    


@app.route('/generate-profile', methods=['GET'])
def generate_profile():
    # This could be dynamically generated or fetched from a database in a real application
    profile = generate_random_preference_profile(5)
    cache.set('current_profile', json.dumps(profile))
    formatted_profile = profile_formatting(profile)
    return jsonify(profile=formatted_profile), 200


@app.route('/matching-solution', methods=['GET'])
def generate_solution():
    # This could be dynamically generated or fetched from a database in a real application
    profile_data = "this is the matching solution x"
    raw_data = cache.get('current_profile')  # Let's say this comes from Redis
    if raw_data is None:
        return "Preferences not found", 404

    # Ensure data is decoded to string and loaded to dictionary
    try:
        preferences = json.loads(raw_data.decode('utf-8'))  # Decode bytes to str and load to dict
    except (ValueError, TypeError) as e:
        app.logger.error(f"Failed to decode or parse preferences: {e}")
        return "Invalid preferences format", 400
    print(preferences)
    n = len(preferences['mpref'])
    man_optimal_result, man_process = gale_shapley(preferences['mpref'], preferences['wpref'], n, False)
    solution = [man_optimal_result, "\n\n   ", man_process]
    cache.set('current_solution', json.dumps(man_optimal_result))
    cache.set('current_process', json.dumps(man_process))
    return jsonify(matchingSolution=solution), 200

@app.route('/llm-explanation', methods=['GET'])
def llm_explanation():


    raw_data = cache.get('current_profile')  # Let's say this comes from Redis
    if raw_data is None:
        return "Preferences not found", 404

    # Ensure data is decoded to string and loaded to dictionary
    try:
        preferences = json.loads(raw_data.decode('utf-8'))  # Decode bytes to str and load to dict
    except (ValueError, TypeError) as e:
        app.logger.error(f"Failed to decode or parse preferences: {e}")
        return "Invalid preferences format", 400
    
    solution = cache.get('current_solution')
    process = cache.get('current_process')

    prompt = generate_prompt(preferences, solution, process)
    response = gpt4_matching(prompt)
    return jsonify(explanation=response), 200




if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True)

CORS(app, expose_headers='Authorization')