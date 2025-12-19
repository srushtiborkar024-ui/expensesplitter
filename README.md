# 💰 Expense Splitter

> A beautiful, full-stack web application to split expenses fairly among friends. Know exactly who owes whom instantly!

![Python](https://img.shields.io/badge/Python-3.7+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green?style=flat-square&logo=fastapi)
![HTML5](https://img.shields.io/badge/HTML5-E34C26?style=flat-square&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## ✨ Features

- ✅ **Add Expenses** - Record expenses with descriptions and amounts
- ✅ **Split Bills Fairly** - Automatically split costs among friends
- ✅ **Settlement Calculator** - See who owes whom at a glance
- ✅ **User Summaries** - Track total paid and owed per person
- ✅ **Statistics Dashboard** - View expense trends and categories
- ✅ **Category Tracking** - Organize expenses by type (Food, Transport, etc.)
- ✅ **Real-time Updates** - Instant calculations and UI refresh
- ✅ **Mobile Responsive** - Works perfectly on phones, tablets, desktops
- ✅ **Beautiful UI** - Modern interface with smooth animations
- ✅ **JSON-based Storage** - Simple, portable data storage
- ✅ **REST API** - Full API documentation with Swagger UI

---

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/expense-splitter.git
cd expense-splitter
```

2. **Create virtual environment**
```bash
python -m venv venv
```

3. **Activate virtual environment**
```bash
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Run the application**
```bash
python -m uvicorn app.main:app --reload
```

6. **Open in browser**
```
http://localhost:8000
```

---

## 📖 Usage

### Adding an Expense

1. Fill in the form:
   - **Description**: What was the expense for? (e.g., "Dinner at restaurant")
   - **Amount**: How much? (e.g., 90.00)
   - **Paid By**: Who paid? (e.g., "Alice")
   - **Split Between**: Who should split it? (e.g., "Alice,Bob,Charlie")
   - **Category**: What type? (Food, Transport, Entertainment, etc.)

2. Click **"✅ Add Expense"**
3. Watch the calculations update automatically!

### Viewing Data

- **All Expenses** - See all recorded expenses with details
- **Settlements** - See who owes whom and amounts
- **Summary** - View each person's balance
- **Statistics** - See total expenses and breakdowns

### Deleting an Expense

Click the **🗑️ Delete** button on any expense card to remove it.

---

## 📁 Project Structure

```
expense-splitter/
│
├── app/                              # Backend code
│   ├── __init__.py                  # Package marker
│   ├── main.py                      # FastAPI server entry point
│   ├── models.py                    # Pydantic data models
│   ├── storage.py                   # JSON file operations
│   └── routers/
│       ├── __init__.py              # Package marker
│       └── expenses.py              # API endpoints
│
├── data/                             # Data directory
│   └── expenses.json               # JSON database (auto-created)
│
├── venv/                             # Virtual environment (auto-created)
│
├── index.html                        # Frontend (HTML + CSS + JS)
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── ARCHITECTURE-FLOW.md             # Detailed architecture guide
├── SETUP-GUIDE.md                   # Quick setup instructions
└── .gitignore                       # Git ignore rules
```

---

## 🔧 API Endpoints

### Expenses
- `GET /expenses/` - Get all expenses
- `POST /expenses/` - Add new expense
- `DELETE /expenses/{id}` - Delete expense

### Settlements
- `GET /expenses/settle/who-owes-whom` - Calculate settlements
- `GET /expenses/settle/final-balances` - Get final balances

### Summary
- `GET /expenses/summary/all` - Get all user summaries
- `GET /expenses/summary/{name}` - Get specific user summary

### Statistics
- `GET /expenses/stats/total` - Get overall statistics
- `GET /expenses/stats/by-category` - Get stats by category

### Documentation
- `GET /api/docs` - Interactive API documentation (Swagger UI)
- `GET /health` - Health check endpoint

---

## 📊 Data Format

### Expense Object
```json
{
  "id": 1,
  "description": "Pizza",
  "amount": 30.0,
  "paid_by": "Alice",
  "split_between": "Alice,Bob",
  "category": "Food",
  "created_at": "2025-12-15T11:00:00"
}
```

### Settlement Object
```json
{
  "debtor": "Bob",
  "creditor": "Alice",
  "amount": 15.00
}
```

### User Summary Object
```json
{
  "name": "Alice",
  "total_paid": 100.0,
  "total_owed": 50.0,
  "balance": 50.0
}
```

---

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern web framework for building APIs
- **Python 3.7+** - Programming language
- **Pydantic** - Data validation using Python type annotations
- **Uvicorn** - ASGI web server

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling and animations
- **JavaScript (ES6+)** - Interactivity and API calls

### Storage
- **JSON** - Simple, portable data storage
- **File-based** - No database required

---

## 📚 Architecture

The application follows a clean **3-tier architecture**:

```
┌─────────────────────────────────────────┐
│         Frontend (index.html)           │
│    HTML + CSS + JavaScript              │
│  Beautiful UI with form and display     │
└────────────┬────────────────────────────┘
             │ REST API (HTTP)
┌────────────▼────────────────────────────┐
│         Backend (FastAPI)               │
│  main.py + routers/expenses.py          │
│  models.py + storage.py                 │
└────────────┬────────────────────────────┘
             │ File I/O
┌────────────▼────────────────────────────┐
│         Storage (JSON)                  │
│  data/expenses.json                     │
└─────────────────────────────────────────┘
```

For detailed architecture information, see [ARCHITECTURE-FLOW.md](ARCHITECTURE-FLOW.md)

---

## 🔄 Data Flow

1. **User opens app** → `index.html` loads
2. **JavaScript initializes** → Fetches all data via API
3. **UI displays data** → Shows expenses, settlements, summaries
4. **User adds expense** → Form submission → POST /expenses/
5. **Backend processes** → Validates data → Saves to JSON
6. **Response returned** → JavaScript updates UI
7. **Data persists** → Everything saved in `data/expenses.json`

---

## 🐛 Troubleshooting

### ModuleNotFoundError: No module named 'fastapi'

**Solution:**
```bash
# Make sure venv is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### Port 8000 already in use

**Solution:**
```bash
# Use a different port
python -m uvicorn app.main:app --reload --port 8001

# Visit http://localhost:8001
```

### UI not loading or showing HTML code

**Solution:**
```bash
# Restart the server
# Press Ctrl+C to stop
python -m uvicorn app.main:app --reload

# Visit http://localhost:8000 (not /index.html)
# Clear browser cache (Ctrl+Shift+Delete)
```

### Data not saving

**Solution:**
```bash
# Check if data folder exists
ls data/  # macOS/Linux
dir data  # Windows

# Restart server
# Refresh browser
```

---

## 📦 Dependencies

```
fastapi       # Web framework
uvicorn       # ASGI server
pydantic      # Data validation
python-multipart # Form data handling
```

All dependencies are listed in `requirements.txt` and installed via `pip install -r requirements.txt`

---

## 🎓 Learning Outcomes

This project demonstrates:

- ✅ **Full-Stack Development** - Frontend, backend, and data storage
- ✅ **REST API Design** - Proper endpoint structure and HTTP methods
- ✅ **Data Validation** - Using Pydantic for type-safe data handling
- ✅ **Frontend Development** - HTML, CSS, and JavaScript
- ✅ **Asynchronous Programming** - Async/await in Python
- ✅ **File I/O Operations** - Reading and writing JSON
- ✅ **CORS Handling** - Cross-origin resource sharing
- ✅ **Error Handling** - Graceful error management
- ✅ **Responsive Design** - Mobile-friendly UI
- ✅ **Mathematical Calculations** - Settlement algorithms

---

## 💡 Future Enhancements

Potential features to add:

- [ ] Database support (SQLite, PostgreSQL)
- [ ] User authentication and multi-user support
- [ ] Expense categories with color coding
- [ ] Export to PDF/Excel
- [ ] Expense history and filtering
- [ ] Monthly/yearly reports
- [ ] Dark mode theme
- [ ] Multi-language support
- [ ] Email notifications
- [ ] Recurring expenses

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Author

Created as a full-stack web development project.

- 💻 **Full-Stack Implementation**
- 🎨 **UI/UX Design**
- 📱 **Responsive Design**
- 🔧 **API Architecture**

---

## 📞 Support

If you encounter any issues:

1. Check the **Troubleshooting** section above
2. Review the detailed [ARCHITECTURE-FLOW.md](ARCHITECTURE-FLOW.md)
3. Check [SETUP-GUIDE.md](SETUP-GUIDE.md) for setup help
4. Open an issue on GitHub

---

## ⭐ Show Your Support

If you found this project helpful, please consider giving it a star! ⭐

```bash
# Clone and enjoy!
git clone https://github.com/yourusername/expense-splitter.git
```

---

## 📊 Project Stats

- **Lines of Code**: ~2,500+
- **Backend Code**: ~300 lines
- **Frontend Code**: ~1,200 lines
- **API Endpoints**: 10+
- **Features**: 10+
- **Development Time**: Professional-grade application

---

## 🎯 Getting Started Now

```bash
# 1. Clone
git clone https://github.com/yourusername/expense-splitter.git
cd expense-splitter

# 2. Setup
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# 3. Run
python -m uvicorn app.main:app --reload

# 4. Visit
# Open http://localhost:8000 in your browser

# 5. Enjoy!
# Add expenses and split them fairly!
```

---

**Made with ❤️ for clean, maintainable code**

---

## 📖 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Python Documentation](https://docs.python.org/3/)
- [MDN Web Docs](https://developer.mozilla.org/)
- [Architecture Guide](ARCHITECTURE-FLOW.md)
- [Setup Guide](SETUP-GUIDE.md)

---

<div align="center">

### Enjoy fair expense splitting! 💰

✨ Simple • Elegant • Functional ✨

</div>
#   e x p e n s e s p l i t t e r  
 #   e x p e n s e s p l i t t e r  
 