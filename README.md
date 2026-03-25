# 🔍 3D Lost & Found Portal

A premium, highly interactive **Lost and Found Web Application** built with Python (Flask) and SQLite. Designed with modern aesthetics, an interactive 3D particle landing page, and a robust user-centric dashboard.

## ✨ Features
* **Premium UI/UX:** Built with Glassmorphism, CSS gradients, dynamic micro-animations, and the geometric `Outfit` typography.
* **Global Light/Dark Theme:** Real-time theme toggling with robust CSS architecture.
* **3D Landing Page:** Implements `Three.js` (Icosahedron, Torus, Particles) and a floating glass authentication card.
* **Cinematic 3D Modals:** Click on any lost/found item to see its detailed description emerge via advanced 3D perspective transforms.
* **Client-Side Form Guard:** Fully live input-validation before hitting the backend.
* **Success Stories:** Track when items are matched and properly recovered by their owners!
* **Categorization & Filtering:** Browse public lost/found feeds securely.

## 🛠 Tech Stack
* **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Login, Werkzeug Security
* **Frontend:** HTML5, Vanilla JS, Vanilla CSS3, Three.js
* **Database:** SQLite

## 🚀 How to Run Locally

1. **Install dependencies:**  
Make sure you have `flask`, `flask_sqlalchemy`, and `flask_login` installed.
```bash
pip install flask flask-sqlalchemy flask-login
```

2. **Initialize Database & Demo data:**  
This script drops any old tables, sets up the schema, and populates the DB with dummy data (dummy users and 4 active items).
```bash
python seed.py
```

3. **Start the Development Server:**
```bash
python app.py
```

4. **Testing:**
Visit `http://127.0.0.1:5000` in your browser.
**Demo Credentials:**
* **Email:** rahul@lostandfound.in
* **Password:** password123

## 📁 Project Structure
* `app.py` - Core server routes, models, configuration.
* `seed.py` - Database script for testing and previewing data.
* `static/style.css` - All custom styling, modal logic, responsive media queries, and themes.
* `templates/` - HTML layout featuring `base.html` inheritance structure.

---
_Built for college campuses, offices, or community spaces to help track lost belongings with style._
