from flask import Flask, render_template, request, jsonify, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Dummy user data
users = {
    "student": {"username": "user", "password": "user123"},
    "librarian": {"username": "librarian", "password": "lib@123"}
}

# Books data with PDF links
books = {
    "A Brief History of Time": "pdfs/brief-history-of-time.pdf",
    "Atomic Habits": "pdfs/atomic-habits.pdf",
    "Clean Code": "pdfs/clean-code.pdf",
    "Data Science from Scratch": "pdfs/data-science-from-scratch.pdf",
    "Deep Learning with Python": "pdfs/deep-learning-with-python.pdf",
    "Eloquent JavaScript": "pdfs/eloquent-javascript.pdf",
    "Introduction to Algorithms": "pdfs/introduction-to-algorithms.pdf",
    "JavaScript: The Good Parts": "pdfs/javascript-good-parts.pdf",
    "Machine Learning Yearning": "pdfs/machine-learning-yearning.pdf",
    "The Pragmatic Programmer": "pdfs/pragmatic-programmer.pdf"
}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form.get('role')
        username = request.form.get('username')
        password = request.form.get('password')

        if role in users:
            creds = users[role]
            if creds["username"] == username and creds["password"] == password:
                session['role'] = role
                return '', 200  # success

        return "Invalid username, password, or role", 401

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'role' in session:
        return render_template('dashboard.html', role=session['role'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('role', None)
    return redirect(url_for('login'))

@app.route('/books')
def books_page():
    if 'role' in session:
        return render_template('books.html')
    return redirect(url_for('login'))

@app.route('/search')
def search():
    query = request.args.get('query', '').lower()

    results = {
        book: url_for('static', filename=pdf_path)
        for book, pdf_path in books.items()
        if query in book.lower()
    }
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
