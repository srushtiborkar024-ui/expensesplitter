# Expense Splitter

Expense Splitter is a full-stack web application that helps users split shared expenses and clearly understand who owes whom. It calculates expenses fairly, shows per-user summaries, and produces final settlements based on net balances.

The project focuses on clarity, correctness, and clean system design rather than unnecessary complexity.

## Features

* Add expenses with description, amount, payer, participants, and category
* Automatically split expenses equally among participants
* View all expenses in a clean card-based layout
* See final settlements showing who should pay whom
* View per-user summaries (total paid, total owed, net balance)
* Categorize expenses (Food, Shopping, Utilities, etc.)
* Responsive UI for desktop and mobile
* REST API built using FastAPI
* JSON-based storage (no database required)

## Technology Stack

### Backend

* Python 3.7+
* FastAPI
* Pydantic
* Uvicorn

### Frontend

* HTML
* CSS
* JavaScript (ES6)

### Storage

* JSON file-based storage

## Project Structure

```
expense-splitter/
│
├── app/
│   ├── main.py            # FastAPI application entry point
│   ├── models.py          # Pydantic models
│   ├── storage.py         # JSON read/write logic
│   └── routers/
│       └── expenses.py    # Expense, summary, and settlement APIs
│
├── data/
│   └── expenses.json      # Stored expense data
│
├── index.html             # Frontend UI
├── requirements.txt       # Python dependencies
├── README.md
└── .gitignore
```

## Installation and Setup

### Prerequisites

* Python 3.7 or higher
* pip

### Steps

1. Clone the repository

```bash
git clone https://github.com/yourusername/expense-splitter.git
cd expense-splitter
```

2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Run the application

```bash
python -m uvicorn app.main:app --reload
```

5. Open in browser

```
http://localhost:8000
```

## How the Application Works

### Adding an Expense

Each expense includes:

* Description
* Amount
* Paid by (person who paid)
* Split between (comma-separated names)
* Category

The total amount is divided equally among all listed participants.

### User Summary

For each person, the system calculates:

* Total amount paid
* Total amount owed
* Net balance (paid − owed)

## Settlement Design (Important)

This application calculates **global net settlements across all recorded expenses**.

A person may appear in multiple expense sets, and their final balance is calculated by netting all amounts paid and owed across the entire dataset.

The settlement algorithm does not restrict payments to only those people who directly shared an individual expense. Instead, it minimizes the number of transactions by allowing any debtor to pay any creditor, as long as the final balances are settled correctly.

This approach is similar to **Splitwise’s overall balance view**, where settlements are based on net balances rather than individual expense relationships.

## API Endpoints

### Expenses

* `GET /expenses/` – Fetch all expenses
* `POST /expenses/` – Add a new expense
* `DELETE /expenses/{id}` – Delete an expense

### Settlements

* `GET /expenses/settle/who-owes-whom` – Calculate final settlements

### Summary

* `GET /expenses/summary/all` – Summary for all users
* `GET /expenses/summary/{name}` – Summary for a specific user

### Statistics

* `GET /expenses/stats/total` – Overall expense statistics

## Limitations

* No user authentication
* All expenses are stored in a single JSON file
* No group-based separation (all users share one global ledger)
* Only equal splits are supported

## Future Enhancements

* Group-based expenses (separate trips or friend circles)
* Database support (SQLite or PostgreSQL)
* User authentication
* Unequal expense splits
* Expense filtering and reports
* Export to CSV or PDF

## Learning Outcomes

This project demonstrates:

* Full-stack application development
* REST API design with FastAPI
* Backend–frontend integration
* File-based data persistence
* Settlement and balance calculation logic
* Clean project structure and maintainable code

## License

This project is licensed under the MIT License.

## Author

Developed as part of the **Introduction to Python** course to apply Python programming concepts, data handling, and logical problem-solving to a real-world expense-splitting scenario.


If you paste this into GitHub, it will look **properly documented, clean, and academic**.
You’re completely done now.
