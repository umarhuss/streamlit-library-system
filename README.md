# 📚 Streamlit Library Management System

This is a simple **Library Management System** built with Python and **Streamlit**. The system supports two types of users — **Members** and **Librarians** — and allows them to browse, register, and manage books, magazines, and videos through a modern, interactive web interface.

---

## 🚀 Features

- 🔐 Role-based login system (Member or Librarian)
- 📖 Browse Books, Magazines, and Videos
- 👤 Member Portal – View borrowed items
- 🛠️ Librarian Portal – Register new library items (books, magazines, videos)
- 🔄 Session-based user management
- 🧪 Debug tools for development

---

## 🧰 Technologies Used

- [Streamlit](https://streamlit.io/)
- Python 3.9+
- Object-Oriented Programming

---

## ▶️ How to Run the App

# Clone the repository
git clone https://github.com/your-username/streamlit-library-system.git
cd streamlit-library-system

# Create and activate virtual environment
python -m venv .venv

# On macOS/Linux:
source .venv/bin/activate

# On Windows (Command Prompt):
.venv\Scripts\activate.bat

# On Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run streamlit_app.py

## 🧪 Preloaded Demo Content

On startup, the system loads:

- ✅ **3 Sample Books**  
- ✅ **3 Magazines**  
- ✅ **3 Videos**

These are available immediately via the “Browse” sections. Log in to access personalized features.

---

## 🔒 User Roles

### Member

- Can log in  
- View available books, magazines, and videos  
- Access Member Portal (to view borrowed items)

### Librarian

- Can log in  
- Has all Member privileges  
- Access Librarian Portal to register new items

---

## 🔧 Future Improvements

- Persistent storage (database or file-based)  
- Borrow/Return item logic  
- Admin dashboard  
- Password-based authentication  
- Improved accessibility & UI/UX

---

## 📄 License

This project is for educational and academic use.  
Feel free to fork, adapt, and build upon it for personal or non-commercial projects.


