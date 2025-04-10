from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'insecure_secret_key_for_ctf'  # Intentionally insecure

# Ensure directories exist
os.makedirs('users', exist_ok=True)
os.makedirs('secrets', exist_ok=True)

@app.route('/')
def index():
    if 'email' in session:
        try:
            with open(f'secrets/{session["email"]}.txt', 'r') as f:
                secret = f.read()
        except FileNotFoundError:
            secret = "No secret stored yet"
        return render_template('dashboard.html', email=session['email'], secret=secret)
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        eye_color = request.form['eye_color']
        
        # Save user data in plain text
        with open(f'users/{email}.txt', 'w') as f:
            f.write(f"Password: {password}\n")
            f.write(f"Eye Color: {eye_color}\n")
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            with open(f'users/{email}.txt', 'r') as f:
                contents = f.read()
                if f"Password: {password}" in contents:
                    session['email'] = email
                    return redirect(url_for('index'))
        except FileNotFoundError:
            pass
        
        return "Login failed. Invalid email or password."
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/save_secret', methods=['POST'])
def save_secret():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    secret = request.form['secret']
    with open(f'secrets/{session["email"]}.txt', 'w') as f:
        f.write(secret)
    
    return redirect(url_for('index'))

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    if request.method == 'POST':
        email = request.form['email']
        eye_color = request.form['eye_color']
        new_password = request.form['new_password']
        
        try:
            with open(f'users/{email}.txt', 'r') as f:
                contents = f.read()
                if f"Eye Color: {eye_color}" in contents:
                    with open(f'users/{email}.txt', 'w') as f:
                        f.write(f"Password: {new_password}\n")
                        f.write(f"Eye Color: {eye_color}\n")
                    return "Password reset successful!"
        except FileNotFoundError:
            pass
        
        return "Password reset failed. Invalid email or eye color."
    
    return render_template('reset.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
