import os
import subprocess
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
PROCESSED_FOLDER = os.path.join(os.getcwd(), 'processed')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# Ensure the upload and processed folders exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

# Define your shell script path
SCRIPT_PATH = os.path.join(os.getcwd(), 'process_file.sh')

@app.route('/', methods=['GET', 'POST'])
def index():
    file_content = ''  # Initialize empty file content
    processed_file_content = ''  # Content for processed file
    delete_processed_file = False  # Flag to indicate if file should be deleted

    if request.method == 'POST':
        if 'view_analysis' in request.form:
            # Set flag to delete the processed file after reading it
            delete_processed_file = True

        else:
            file = request.files.get('file')
            notes = request.form.get('notes')

            # If textarea has text, create an error.log file and execute it
            if notes:
                error_log_path = os.path.join(app.config['UPLOAD_FOLDER'], 'error.log')
                with open(error_log_path, 'w') as f:
                    f.write(notes)  # Write textarea content to error.log

                # Run the shell script and pass the created error.log file as an argument
                try:
                    subprocess.run([SCRIPT_PATH, error_log_path], check=True)
                    return jsonify({'success': True, 'message': 'error.log created and executed successfully!'})
                except subprocess.CalledProcessError as e:
                    return jsonify({'success': False, 'message': f'Shell script execution failed: {str(e)}'})

            # If a file is uploaded, save it to uploads folder
            if file and (file.filename.endswith('.log') or file.filename.endswith('.txt')):
                # Save the uploaded file as error.log
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'error.log')
                file.save(file_path)

                # Run the shell script and pass the file as an argument
                try:
                    subprocess.run([SCRIPT_PATH, file_path,], check=True)
                    return jsonify({'success': True, 'message': 'File uploaded and shell script executed successfully!'})
                except subprocess.CalledProcessError as e:
                    return jsonify({'success': False, 'message': f'Shell script execution failed: {str(e)}'})

    # Serve the page with processed file content
    processed_file_path = os.path.join(app.config['PROCESSED_FOLDER'], 'processed_output.txt')
    if os.path.exists(processed_file_path):
        with open(processed_file_path, 'r') as f:
            processed_file_content = f.read()
    
    # Delete processed_output.txt if needed
    if delete_processed_file:
        if os.path.exists(processed_file_path):
            os.remove(processed_file_path)

    return render_template('index.html', processed_file_content=processed_file_content)


if __name__ == '__main__':
    app.run(debug=True)
