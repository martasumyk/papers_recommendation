# 🧠 Paper Search

This is a Flask-based web application that allows users to:

- 🔍 Search for scientific papers via [arXiv.org](https://arxiv.org)
- 👤 Register and log in with an avatar and profile info
- 📝 Edit their profile (field of interest, position, academic level, LinkedIn)
- 🧾 Save secure user data with salted password hashing
- 📷 Upload and view a profile photo with a clean dropdown menu

---

## 🚀 Features

- Secure user registration and login system
- Passwords stored with SHA-256 + salt
- Avatar upload and circular display
- Paper search via arXiv API
- Editable profile with fields like:
  - Field of interest
  - Position
  - Academic level (Student, PhD, etc.)
  - LinkedIn profile
- Responsive and clean UI with toggling themes

---

## 🛠️ Technologies

- Python 3.10+
- Flask
- HTML + CSS
- arXiv API
- SHA-256 hashing

---

## 🗂️ Folder Structure
```
simple_project/
│
├── app.py                     # Main Flask application
├── database.txt               # Stores user data as JSON lines (one per user)
│
├── static/
│   ├── avatars/               # Uploaded profile photos
│   └── css/
│       ├── light.css          # Light theme
│       └── dracula.css        # Dracula (dark) theme
│   └── js/
│       └── theme-toggle.js    # JavaScript for switching themes
│
├── templates/
│   ├── index.html             # Main search + profile dropdown
│   ├── login.html             # Login form
│   ├── register.html          # Registration form
│   └── profile.html           # Profile viewer/editor
│
└── README.md                  # Instructions for running the app

```

---

## 🧪 Setup Instructions

### ✅ 1. Clone the repo

```bash
git clone https://github.com/your-username/paper-search-flask.git
cd paper-search-flask
```

### ✅ 2. Install dependencies
```bash
pip install flask arxiv
```

### ✅ 3. Run the app
```bash
python app.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🔐 Default Security
- Passwords are hashed with SHA-256 and salted (static salt; replace with unique salt per user in production).
- Avatars are stored locally under /static/avatars.

---

## 💡 Future Improvements
- ❗ Add to-read list and likes
- ❗ Fix the alignment of the registration page
- ✅ Toast notifications
- 🔐 Switch to per-user salt with bcrypt or passlib
- 🧠 Search history per user
- 📦 Move from flat file (database.txt) to SQLite or PostgreSQL
- 📱 Mobile-first responsive layout
