from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_mysqldb import MySQL
from jira import JIRA
from datetime import datetime
import os
import re  # Import regex for email validation

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
app.config['MYSQL_HOST'] = 'put_your_host'
app.config['MYSQL_USER'] = '<your_user>'
app.config['MYSQL_PASSWORD'] = 'your_pass'
app.config['MYSQL_DB'] = '<database_name>'

mysql = MySQL(app)

# JIRA Configuration (YOUR ACTUAL CREDENTIALS)
JIRA_URL = "your_url_of_jira"
JIRA_USER = "your_jira_user_gmail"
JIRA_API_TOKEN = "put_your_api_token_here"

# YOUR ACTUAL JIRA PROJECT KEY (from your output)
ACTUAL_PROJECT_KEY = "SCRUM"

# YOUR ACTUAL ISSUE TYPES (from your output)
ISSUE_TYPES = ["Subtask", "Story", "Request", "Bug", "Task", "Feature", "Epic"]

# YOUR ACTUAL PRIORITIES (from your output)
PRIORITIES = ["Highest", "High", "Medium", "Low", "Lowest"]

# Map form values to JIRA values
PROJECT_MAPPING = {
    "IIP": "SCRUM",  # Map IIP to SCRUM
    "PP": "SCRUM",  # Map PP to SCRUM
    "Front-End Dev (SCRUM)": "SCRUM",  # Map to SCRUM
    "IIP-PP": "SCRUM",  # Map to SCRUM
    "Other": "SCRUM"  # Map to SCRUM
}

ISSUE_TYPE_MAPPING = {
    "Request": "Request",
    "Issue": "Bug",  # Map "Issue" to "Bug"
    "Task": "Task",
    "Story": "Story"
}

PRIORITY_MAPPING = {
    "Low": "Low",
    "Medium": "Medium",
    "High": "High",
    "Critical": "Highest"  # Map "Critical" to "Highest"
}


# Initialize JIRA connection
def get_jira_connection():
    try:
        jira = JIRA(
            server=JIRA_URL,
            basic_auth=(JIRA_USER, JIRA_API_TOKEN),
            options={'timeout': 30, 'verify': True}
        )
        print("JIRA Connection Successful!")
        return jira
    except Exception as e:
        print(f"JIRA Connection Error: {e}")
        return None


# ==================== HOME ROUTES ====================
@app.route("/")
def get_home():
    if 'logged_in' in session:
        return render_template("home.html", username=session['username'])
    return redirect(url_for('login_page'))


@app.route("/home")
def home():
    if 'logged_in' in session:
        return render_template("home.html", username=session['username'])
    return redirect(url_for('login_page'))


# ==================== JIRA ROUTES ====================
@app.route("/jira")
def jira():
    if 'logged_in' in session:
        return render_template("jira_page.html", username=session['username'])
    return redirect(url_for('login_page'))


@app.route("/jira_create", methods=["POST"])
def jira_create():
    if 'logged_in' in session:
        if request.method == "POST":
            try:
                # Get form data
                project_name = request.form.get("project")
                issue_type_name = request.form.get("issueType")
                reporter_name = request.form.get("reporter")
                summary = request.form.get("summary")
                description = request.form.get("description")
                priority_name = request.form.get("priority")

                print(f" Form Data Received:")
                print(f"   Project Selected: {project_name}")
                print(f"   Issue Type: {issue_type_name}")
                print(f"   Reporter: {reporter_name}")
                print(f"   Summary: {summary}")
                print(f"   Priority: {priority_name}")

                #  ALWAYS USE YOUR ACTUAL PROJECT KEY "SCRUM"
                project_key = "SCRUM"

                # Map form values to JIRA values
                jira_issue_type = ISSUE_TYPE_MAPPING.get(issue_type_name, "Task")
                jira_priority = PRIORITY_MAPPING.get(priority_name, "Medium")

                print(f"Using Project Key: {project_key}")
                print(f"JIRA Issue Type: {jira_issue_type}")
                print(f"JIRA Priority: {jira_priority}")

                # Connect to JIRA
                jira = get_jira_connection()
                if not jira:
                    flash("Cannot connect to JIRA. Check credentials.", "error")
                    return redirect(url_for('jira'))

                # Create issue with EXACT JIRA format
                issue_dict = {
                    'project': {'key': project_key},
                    'summary': summary,
                    'description': f"**Reporter:** {reporter_name}\n\n**Description:**\n{description}",
                    'issuetype': {'name': jira_issue_type},
                    'priority': {'name': jira_priority}
                }

                print(f" Creating JIRA issue in project: {project_key}")

                # Create the issue
                new_issue = jira.create_issue(fields=issue_dict)

                issue_key = new_issue.key  # Will be like SCRUM-123
                issue_url = f"{JIRA_URL}/browse/{issue_key}"

                print(f" JIRA Ticket Created: {issue_key}")
                print(f" URL: {issue_url}")

                # Success message
                success_message = f"""
                 JIRA Ticket Created Successfully!

                Ticket: {issue_key}
                Project: {project_name}
                Type: {issue_type_name}
                Priority: {priority_name}

                View Ticket: {issue_url}
                """

                flash(success_message, "success")
                return redirect(url_for('jira'))

            except Exception as e:
                error_msg = f" JIRA Creation Failed: {str(e)}"
                print(error_msg)
                flash(error_msg, "error")
                return redirect(url_for('jira'))
    return redirect(url_for('login_page'))


@app.route("/test_jira")
def test_jira():
    if 'logged_in' in session:
        try:
            jira = get_jira_connection()
            if jira:
                # Test creating a simple ticket
                test_issue_dict = {
                    'project': {'key': 'SCRUM'},
                    'summary': 'Test Ticket from Flask App',
                    'description': 'This is a test ticket created by the Flask JIRA integration.',
                    'issuetype': {'name': 'Task'},
                    'priority': {'name': 'Medium'}
                }

                test_issue = jira.create_issue(fields=test_issue_dict)

                result = f"""
                <h2> JIRA Connection & Creation Test Successful!</h2>
                <p><strong>Connected to:</strong> {JIRA_URL}</p>
                <p><strong>Your Project:</strong> SCRUM (Front-End Dev)</p>
                <p><strong>Test Ticket Created:</strong> {test_issue.key}</p>
                <p><strong>Ticket URL:</strong> <a href="{JIRA_URL}/browse/{test_issue.key}" target="_blank">{JIRA_URL}/browse/{test_issue.key}</a></p>
                """
                return result
            else:
                return "<h2> JIRA Connection Failed</h2><p>Check your API token and credentials</p>"
        except Exception as e:
            return f"<h2> Error</h2><pre>{str(e)}</pre>"
    return redirect(url_for('login_page'))


# ==================== AUTHENTICATION ROUTES ====================
@app.route("/login_page")
def login_page():
    # If already logged in, redirect to home
    if 'logged_in' in session:
        return redirect(url_for('home.html'))
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    # If already logged in, redirect to home
    if 'logged_in' in session:
        return redirect(url_for('home'))

    msg = ''
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s and password = %s', (username, password))
        account = cursor.fetchone()
        cursor.close()

        print(f"Account fetched: {account}")

        if account:
            session["logged_in"] = True
            session["id"] = account[0]
            session['username'] = account[1]
            session['email'] = account[3] if len(account) > 3 else ''
            return redirect(url_for('home'))
        else:
            msg = "Incorrect username or password"

    return render_template('login.html', msg=msg)


@app.route("/create_account_page")
def create_account_page():
    # If already logged in, redirect to home
    if 'logged_in' in session:
        return redirect(url_for('home.html'))
    return render_template("create_account.html")


@app.route("/create_account", methods=["POST"])
def create_account():
    if request.method == "POST":
        try:
            # Get form data
            username = request.form.get("username", "").strip()
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "").strip()
            confirm_password = request.form.get("confirm_password", "").strip()

            # Validation
            errors = []

            # Check required fields
            if not username:
                errors.append("Username is required")
            if not email:
                errors.append("Email is required")
            if not password:
                errors.append("Password is required")
            if not confirm_password:
                errors.append("Confirm password is required")

            # Check if passwords match
            if password and confirm_password and password != confirm_password:
                errors.append("Passwords do not match")

            # Validate email format
            if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                errors.append("Invalid email format")

            # Check password strength
            if password and len(password) < 6:
                errors.append("Password must be at least 6 characters")

            # Check if username already exists
            if username:
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
                existing_user = cursor.fetchone()
                cursor.close()

                if existing_user:
                    errors.append("Username already exists")

            # Check if email already exists
            if email:
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
                existing_email = cursor.fetchone()
                cursor.close()

                if existing_email:
                    errors.append("Email already registered")

            # If there are errors, return to form
            if errors:
                return render_template("create_account.html", errors=errors,
                                       username=username, email=email)

            # Insert new user into database
            cursor = mysql.connection.cursor()
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, password)
            )
            mysql.connection.commit()
            cursor.close()

            # SUCCESS: AUTOMATICALLY LOGIN AND REDIRECT TO HOME
            # Auto login after successful registration
            session["logged_in"] = True
            session["id"] = username  # Temporary ID
            session['username'] = username
            session['email'] = email

            # Redirect to home page
            return redirect(url_for('home'))

        except Exception as e:
            error_msg = f"Account creation failed: {str(e)}"
            return render_template("create_account.html", errors=[error_msg])

    return redirect(url_for('create_account_page'))


@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect(url_for('login_page'))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")