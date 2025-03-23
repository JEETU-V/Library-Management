from flask import Flask, render_template, request, jsonify, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Dummy user database
users = {
    "student": {"username": "user", "password": "user123"},
    "librarian": {"username": "librarian", "password": "lib@123"}
}

# Books data with correct PDF links
books = {
    "A Brief History of Time": "/static/pdfs/brief-history-of-time.pdf",
    "Atomic Habits": "/static/pdfs/atomic-habits.pdf",
    "Clean Code": "/static/pdfs/clean-code.pdf",
    "Data Science from Scratch": "/static/pdfs/data-science-from-scratch.pdf",
    "Deep Learning with Python": "/static/pdfs/deep-learning-with-python.pdf",
    "Eloquent JavaScript": "/static/pdfs/eloquent-javascript.pdf",
    "Introduction to Algorithms": "/static/pdfs/introduction-to-algorithms.pdf",
    "JavaScript: The Good Parts": "/static/pdfs/javascript-good-parts.pdf",
    "Machine Learning Yearning": "/static/pdfs/machine-learning-yearning.pdf",
    "The Pragmatic Programmer": "/static/pdfs/pragmatic-programmer.pdf"
}

@app.route('/')
def home():
    return redirect(url_for('login'))  # Redirect to login page

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form.get('role')
        username = request.form.get('username')
        password = request.form.get('password')

        if role in users and users[role]["username"] == username and users[role]["password"] == password:
            session['role'] = role
            return redirect(url_for('dashboard'))  # Redirect to dashboard

        return "Invalid username or password", 401 

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'role' in session:  # Check if logged in
        return render_template('dashboard.html')
    return redirect(url_for('login'))  # Redirect to login if not authenticated

@app.route('/logout')
def logout():
    session.pop('role', None)  # Remove session
    return redirect(url_for('login'))

@app.route('/books')
def books_page():
    if 'role' in session:  # Ensure user is logged in
        return render_template('books.html')
    return redirect(url_for('login'))  # Redirect to login if not authenticated

@app.route('/search')
def search():
    query = request.args.get('query', '').lower()
    results = {book: url_for('static', filename=pdf_path) for book, pdf_path in books.items() if query in book.lower()}
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
