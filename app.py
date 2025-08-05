import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from analysis_handler import process_uploaded_file

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
REPORTS_FOLDER = 'reports'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['REPORTS_FOLDER'] = REPORTS_FOLDER
app.config['SECRET_KEY'] = 'a_very_secret_key_for_production'

# Ensure directories exist upon startup
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['REPORTS_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            # This is the correctly indented block
            flash('No file part in the request.', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No file selected.', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(upload_filepath)

            try:
                # Unpack the new return tuple from the handler
                (display_predictions, display_alerts, summary, 
                 full_report_filename, alert_report_filename) = process_uploaded_file(
                    upload_filepath=upload_filepath,
                    report_dir=app.config['REPORTS_FOLDER'],
                    original_filename=filename
                )
                
                # Pass all new data to the template
                return render_template(
                    'results.html', 
                    predictions=display_predictions, 
                    alert_predictions=display_alerts,
                    summary=summary, 
                    filename=filename, 
                    report_filename=full_report_filename,
                    alert_report_filename=alert_report_filename
                )
            except Exception as e:
                return render_template('error.html', error=str(e))
        else:
            flash('Invalid file type. Please upload a CSV file.', 'error')
            return redirect(request.url)

    return render_template('index.html')

@app.route('/download/<filename>')
def download_report(filename):
    """Serve generated reports for downloading."""
    return send_from_directory(
        app.config['REPORTS_FOLDER'], 
        filename, 
        as_attachment=True
    )

if __name__ == '__main__':
    app.run(debug=True)