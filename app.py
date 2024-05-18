from flask import Flask, render_template, request
from functions import return_results
import pandas as pd
import os
import glob


app = Flask(__name__)

@app.route('/')
def index():
    csv_files = glob.glob('*.csv')
    csv_data = {}
    for file in csv_files:
        try:
            filename = os.path.basename(file)
            csv_data[filename] = pd.read_csv(file)
        except Exception as e:
            csv_data[filename] = f"Error reading CSV file: {e}"
    
    return render_template('index.html', csv_data=csv_data)

@app.route('/execute', methods=['POST'])
def execute():
    command = request.form['command']
    csv_files = glob.glob('*.csv')
    csv_data = {}
    for file in csv_files:
        try:
            filename = os.path.basename(file)
            csv_data[filename] = pd.read_csv(file)
        except Exception as e:
            csv_data[filename] = f"Error reading CSV file: {e}"

    try:
        results = return_results(command)
        return render_template('index.html', results=results, csv_data=csv_data)
    
    except Exception as e:
        error_message = f"Error executing query: {e}"
        return render_template('index.html', error_message=error_message, csv_data=csv_data)

if __name__ == '__main__':
    app.run(debug=True)
