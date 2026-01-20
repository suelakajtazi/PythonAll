"""
Library Tracker - Main Flask Application
Run with: python app.py
Access at: http://localhost:5000
"""
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_required, current_user
from database import db, init_db, User, ReadBook, ReadingListBook
from datetime import datetime
from sqlalchemy import func

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'  # localhost SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
init_db(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ============ AUTHENTICATION ROUTES ============
from flask_login import login_user, logout_user

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Validation
        if not email or not username or not password:
            flash('All fields are required', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already taken', 'error')
            return render_template('register.html')
        
        # Create user with hashed password
        user = User(email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Welcome back!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))


# ============ DASHBOARD ============
@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard with reading statistics"""
    user_id = current_user.id
    
    # Total hours spent reading
    total_hours = db.session.query(func.sum(ReadBook.hours_spent))\
        .filter(ReadBook.user_id == user_id).scalar() or 0
    
    # Number of books read
    books_count = ReadBook.query.filter_by(user_id=user_id).count()
    
    # Most liked book (highest rating)
    top_book = ReadBook.query.filter_by(user_id=user_id)\
        .order_by(ReadBook.rating.desc()).first()
    
    # Most liked genre (average rating per genre)
    genre_stats = db.session.query(
        ReadBook.genre,
        func.avg(ReadBook.rating).label('avg_rating'),
        func.count(ReadBook.id).label('count')
    ).filter(ReadBook.user_id == user_id)\
     .group_by(ReadBook.genre)\
     .order_by(func.avg(ReadBook.rating).desc())\
     .first()
    
    top_genre = genre_stats.genre if genre_stats else None
    
    # Recent books
    recent_books = ReadBook.query.filter_by(user_id=user_id)\
        .order_by(ReadBook.date_finished.desc()).limit(5).all()
    
    # Reading list counts by status
    reading_list_stats = db.session.query(
        ReadingListBook.status,
        func.count(ReadingListBook.id)
    ).filter(ReadingListBook.user_id == user_id)\
     .group_by(ReadingListBook.status).all()
    
    stats = {s: c for s, c in reading_list_stats}
    
    return render_template('dashboard.html',
        total_hours=round(total_hours, 1),
        books_count=books_count,
        top_book=top_book,
        top_genre=top_genre,
        recent_books=recent_books,
        want_to_read=stats.get('want_to_read', 0),
        currently_reading=stats.get('currently_reading', 0)
    )


# ============ READ BOOKS ============
@app.route('/read-books')
@login_required
def read_books():
    books = ReadBook.query.filter_by(user_id=current_user.id)\
        .order_by(ReadBook.date_finished.desc()).all()
    return render_template('read_books.html', books=books)


@app.route('/read-books/add', methods=['POST'])
@login_required
def add_read_book():
    try:
        book = ReadBook(
            user_id=current_user.id,
            title=request.form['title'].strip(),
            author=request.form['author'].strip(),
            genre=request.form['genre'].strip(),
            hours_spent=float(request.form['hours_spent']),
            rating=int(request.form['rating']),
            date_finished=datetime.strptime(request.form['date_finished'], '%Y-%m-%d').date()
        )
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding book: {str(e)}', 'error')
    
    return redirect(url_for('read_books'))


@app.route('/read-books/edit/<int:book_id>', methods=['POST'])
@login_required
def edit_read_book(book_id):
    book = ReadBook.query.filter_by(id=book_id, user_id=current_user.id).first_or_404()
    
    try:
        book.title = request.form['title'].strip()
        book.author = request.form['author'].strip()
        book.genre = request.form['genre'].strip()
        book.hours_spent = float(request.form['hours_spent'])
        book.rating = int(request.form['rating'])
        book.date_finished = datetime.strptime(request.form['date_finished'], '%Y-%m-%d').date()
        db.session.commit()
        flash('Book updated!', 'success')
    except Exception as e:
        flash(f'Error updating: {str(e)}', 'error')
    
    return redirect(url_for('read_books'))


@app.route('/read-books/delete/<int:book_id>', methods=['POST'])
@login_required
def delete_read_book(book_id):
    book = ReadBook.query.filter_by(id=book_id, user_id=current_user.id).first_or_404()
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted', 'info')
    return redirect(url_for('read_books'))


# ============ READING LIST ============
@app.route('/reading-list')
@login_required
def reading_list():
    books = ReadingListBook.query.filter_by(user_id=current_user.id)\
        .order_by(ReadingListBook.created_at.desc()).all()
    
    # Group by status
    grouped = {
        'want_to_read': [b for b in books if b.status == 'want_to_read'],
        'currently_reading': [b for b in books if b.status == 'currently_reading'],
        'read': [b for b in books if b.status == 'read']
    }
    return render_template('reading_list.html', grouped=grouped)


@app.route('/reading-list/add', methods=['POST'])
@login_required
def add_to_reading_list():
    try:
        book = ReadingListBook(
            user_id=current_user.id,
            title=request.form['title'].strip(),
            author=request.form['author'].strip(),
            genre=request.form.get('genre', '').strip(),
            status='want_to_read'
        )
        db.session.add(book)
        db.session.commit()
        flash('Book added to reading list!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('reading_list'))


@app.route('/reading-list/update-status/<int:book_id>', methods=['POST'])
@login_required
def update_book_status(book_id):
    book = ReadingListBook.query.filter_by(id=book_id, user_id=current_user.id).first_or_404()
    new_status = request.form['status']
    
    if new_status in ['want_to_read', 'currently_reading', 'read']:
        book.status = new_status
        db.session.commit()
        flash('Status updated!', 'success')
    
    return redirect(url_for('reading_list'))


@app.route('/reading-list/delete/<int:book_id>', methods=['POST'])
@login_required
def delete_from_reading_list(book_id):
    book = ReadingListBook.query.filter_by(id=book_id, user_id=current_user.id).first_or_404()
    db.session.delete(book)
    db.session.commit()
    flash('Book removed from list', 'info')
    return redirect(url_for('reading_list'))


if __name__ == '__main__':
    print("\n📚 Library Tracker")
    print("=" * 40)
    print("Server running at: http://localhost:5000")
    print("Database: library.db (SQLite)")
    print("=" * 40 + "\n")
    app.run(debug=True, host='localhost', port=5000)
