from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv("SECRET_KEY", "default_secret")

# MySQL DB config
db = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),
    database=os.getenv("DB_NAME", "educhain")
)
cursor = db.cursor(dictionary=True)

# ---------------- ROUTES ----------------

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    if "user_id" in session:
        user_id = session["user_id"]
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        if user:
            return render_template("dashboard.html", user=user)
        else:
            return "User not found", 404
    return redirect(url_for("index"))


@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'GET':
        return render_template("chatbot.html")
    
    from chatbot.genai import get_genai_response
    user_message = request.json.get("message", "")
    response = get_genai_response(user_message)
    return jsonify({"reply": response})


@app.route('/recommend', methods=['POST'])
def recommend():
    from ml_model.recommender import get_recommendations
    user_id = session.get("user_id", 1)  # fallback to 1 for testing
    recommendations = get_recommendations(user_id)
    return jsonify(recommendations)


@app.route('/verify-certificate', methods=['POST'])
def verify_certificate():
    from blockchain.chain import verify_certificate
    cert_hash = request.json.get("hash")
    result = verify_certificate(cert_hash)
    return jsonify({"valid": result})


# ---------------- AUTH ----------------

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()
    
    if user and password == user['password']:  # Plain text; use hashing in production
        session['user_id'] = user['id']
        return redirect('/dashboard')
    return "Invalid credentials", 401


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# ---------------- ADMIN PAGE (Optional) ----------------

@app.route('/admin')
def admin():
    return render_template("admin.html")


# ---------------- MAIN ----------------

if __name__ == '__main__':
    app.run(debug=True)
