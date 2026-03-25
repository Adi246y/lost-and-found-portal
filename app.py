from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user,
    login_required, logout_user, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
import os, datetime

app = Flask(__name__)

# ================= CONFIG =================
app.config['SECRET_KEY'] = 'secret_lost_found_2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'uploads'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'landing'

# ================= MODELS =================
class User(UserMixin, db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(100))
    email         = db.Column(db.String(150), unique=True)
    password_hash = db.Column(db.String(200))
    avatar        = db.Column(db.String(50), default='👤')
    theme         = db.Column(db.String(20), default='dark')
    items         = db.relationship('Item', backref='owner', lazy=True)

class Item(db.Model):
    id             = db.Column(db.Integer, primary_key=True)
    item_type      = db.Column(db.String(10),  default='lost')   # 'lost' or 'found'
    category       = db.Column(db.String(50),  default='Other')
    title          = db.Column(db.String(100), nullable=False)
    description    = db.Column(db.String(500))
    # Where
    location       = db.Column(db.String(200))   # last seen / found place
    # When
    incident_date  = db.Column(db.String(30))    # date lost/found
    incident_time  = db.Column(db.String(20))    # time lost/found
    # Contact person
    contact_name   = db.Column(db.String(100))
    contact_phone  = db.Column(db.String(30))
    contact_email  = db.Column(db.String(150))
    # Image & status
    image          = db.Column(db.String(200), default='')
    status         = db.Column(db.String(20),  default='open')  # open / resolved
    created_at     = db.Column(db.DateTime,    default=datetime.datetime.utcnow)
    user_id        = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

CATEGORIES = [
    'Electronics', 'Keys', 'Wallet/Purse', 'Bag/Backpack', 'Documents', 
    'Clothing', 'Jewellery', 'Books/Stationery', 'ID/Access Cards', 
    'Watches', 'Glasses', 'Other'
]

# ================= ROUTES =================

@app.route('/')
def landing():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('landing.html')

@app.route('/login', methods=['POST'])
def login():
    email    = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        return redirect(url_for('dashboard'))
    flash('Invalid email or password.', 'error')
    return redirect(url_for('landing'))

@app.route('/register', methods=['POST'])
def register():
    name     = request.form.get('name', '').strip()
    email    = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    if not name or not email or not password:
        flash('All fields are required.', 'error')
        return redirect(url_for('landing'))
    if User.query.filter_by(email=email).first():
        flash('An account with that email already exists.', 'error')
        return redirect(url_for('landing'))
    user = User(
        name=name,
        email=email,
        password_hash=generate_password_hash(password)
    )
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return redirect(url_for('dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('landing'))

# ── Settings / Profile ──
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings_page():
    avatars = ['👤', '👨‍💻', '👩‍💻', '🦸‍♂️', '🦸‍♀️', '🥷', '🕵️‍♂️', '🕵️‍♀️', '🧑‍🚀', '😎', '🤖', '👻']
    if request.method == 'POST':
        name   = request.form.get('name', '').strip()
        avatar = request.form.get('avatar', '👤')
        theme  = request.form.get('theme', 'dark')
        
        if name: current_user.name = name
        current_user.avatar = avatar
        current_user.theme = theme
        db.session.commit()
        
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('settings_page'))
        
    return render_template('settings.html', avatars=avatars)

# ── Dashboard (user's own items) ──
@app.route('/dashboard')
@login_required
def dashboard():
    lost_items  = Item.query.filter_by(user_id=current_user.id, item_type='lost').order_by(Item.created_at.desc()).all()
    found_items = Item.query.filter_by(user_id=current_user.id, item_type='found').order_by(Item.created_at.desc()).all()
    return render_template('dashboard.html', lost_items=lost_items, found_items=found_items)

# ── Browse (all public found items) ──
@app.route('/browse')
@login_required
def browse():
    query    = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()
    items_q  = Item.query.order_by(Item.created_at.desc())
    if query:
        items_q = items_q.filter(
            Item.title.ilike(f'%{query}%') | Item.description.ilike(f'%{query}%')
        )
    if category:
        items_q = items_q.filter_by(category=category)
    items = items_q.all()
    return render_template('browse.html', items=items, query=query, sel_category=category, categories=CATEGORIES)

# ── Report Lost ──
@app.route('/report-lost', methods=['GET', 'POST'])
@login_required
def report_lost():
    if request.method == 'POST':
        file = request.files.get('image')
        filename = ''
        if file and file.filename:
            filename = file.filename
            try:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            except Exception:
                filename = ''
        new_item = Item(
            item_type     = 'lost',
            category      = request.form.get('category', 'Other'),
            title         = request.form.get('title', '').strip(),
            description   = request.form.get('description', '').strip(),
            location      = request.form.get('location', '').strip(),
            incident_date = request.form.get('incident_date', ''),
            incident_time = request.form.get('incident_time', ''),
            contact_name  = request.form.get('contact_name', current_user.name).strip(),
            contact_phone = request.form.get('contact_phone', '').strip(),
            contact_email = request.form.get('contact_email', current_user.email).strip(),
            image         = filename,
            user_id       = current_user.id
        )
        db.session.add(new_item)
        db.session.commit()
        flash('Lost item reported successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('report_lost.html', categories=CATEGORIES)

# ── Report Found ──
@app.route('/report-found', methods=['GET', 'POST'])
@login_required
def report_found():
    if request.method == 'POST':
        file = request.files.get('image')
        filename = ''
        if file and file.filename:
            filename = file.filename
            try:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            except Exception:
                filename = ''
        new_item = Item(
            item_type     = 'found',
            category      = request.form.get('category', 'Other'),
            title         = request.form.get('title', '').strip(),
            description   = request.form.get('description', '').strip(),
            location      = request.form.get('location', '').strip(),
            incident_date = request.form.get('incident_date', ''),
            incident_time = request.form.get('incident_time', ''),
            contact_name  = request.form.get('contact_name', current_user.name).strip(),
            contact_phone = request.form.get('contact_phone', '').strip(),
            contact_email = request.form.get('contact_email', current_user.email).strip(),
            image         = filename,
            user_id       = current_user.id
        )
        db.session.add(new_item)
        db.session.commit()
        flash('Found item reported successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('report_found.html', categories=CATEGORIES)

# ── Recovered Items (Public list of resolved items) ──
@app.route('/recovered')
def recovered():
    resolved_items = Item.query.filter_by(status='resolved').order_by(Item.updated_at.desc() if hasattr(Item, 'updated_at') else Item.created_at.desc()).all()
    return render_template('recovered.html', items=resolved_items)

# ── Mark resolved ──
@app.route('/resolve/<int:item_id>', methods=['POST'])
@login_required
def resolve_item(item_id):
    item = Item.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        flash('Not authorized.', 'error')
        return redirect(url_for('dashboard'))
    item.status = 'resolved'
    db.session.commit()
    flash('Item marked as resolved!', 'success')
    return redirect(url_for('dashboard'))

# ── Serve uploads ──
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ================= RUN =================
if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    with app.app_context():
        db.create_all()
    app.run(debug=True)