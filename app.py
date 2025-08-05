from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials, firestore
import os

app = Flask(__name__)
#------page1------
# --- Firebase Init ---
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'projectId': 'fit5238-d0074',
})

db = firestore.client()


# use session
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    """ Login/Register """
    return render_template('login_register.html')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    phone = data.get('phone')
    username = data.get('username')
    password = data.get('password')
    print("register:"+"phone"+phone+'username'+username+'password'+password);
    if not all([phone, username, password]):
        return "Data not full", 400

    users_ref = db.collection('users')
    # check if phone or username exists
    phone_query = users_ref.where('phone', '==', phone).limit(1).get()
    if len(phone_query) > 0:
        return "registerFailed"
    username_query = users_ref.where('username', '==', username).limit(1).get()
    if len(username_query) > 0:
        return "registerFailed"
    # add new user
    user_data = {
        'phone': phone,
        'username': username,
        'password': password
    }
    users_ref.add(user_data)
    return "registerSuccess"

@app.route('/api/login', methods=['POST'])
def login():
    """ process login """
    login_id = request.form.get('IdAccount')
    password = request.form.get('password')

    if not all([login_id, password]):
        return "data not full", 400

    users_ref = db.collection('users')

    # search user
    user_query_username = users_ref.where('username', '==', login_id).limit(1).get()
    user_query_phone = users_ref.where('phone', '==', login_id).limit(1).get()

    user_doc = None
    if len(user_query_username) > 0:
        user_doc = user_query_username[0]
    elif len(user_query_phone) > 0:
        user_doc = user_query_phone[0]

    if user_doc:
        user_data = user_doc.to_dict()
        if user_data.get('password') == password:
            # set up session
            session['user_id'] = user_doc.id
            session['username'] = user_data.get('username')
            return "main"

    return "login failure, please check your password or username"

@app.route('/api/logout')
def logout():
    """ logout """
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

#------page2------
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
import os
from flask import  render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from analysis_handler import process_uploaded_file


def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
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