import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

# Data directory
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

EXPENSES_FILE = DATA_DIR / "expenses.json"

def initialize_data():
    """Create expenses.json if it doesn't exist"""
    if not EXPENSES_FILE.exists():
        EXPENSES_FILE.write_text(json.dumps([], indent=2))
        print(f"✅ Created {EXPENSES_FILE}")

def load_expenses() -> List[Dict[str, Any]]:
    """Load all expenses from JSON file"""
    try:
        if EXPENSES_FILE.exists():
            return json.loads(EXPENSES_FILE.read_text())
    except:
        pass
    return []

def save_expenses(expenses: List[Dict[str, Any]]):
    """Save expenses to JSON file"""
    EXPENSES_FILE.write_text(json.dumps(expenses, indent=2, default=str))

def get_next_id(expenses: List[Dict]) -> int:
    """Get next expense ID"""
    if not expenses:
        return 1
    return max(e.get("id", 0) for e in expenses) + 1

def get_expense_by_id(expense_id: int) -> Dict[str, Any] | None:
    """Get single expense by ID"""
    expenses = load_expenses()
    for expense in expenses:
        if expense.get("id") == expense_id:
            return expense
    return None

def create_expense(expense_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create new expense"""
    expenses = load_expenses()
    
    new_expense = {
        "id": get_next_id(expenses),
        **expense_data,
        "created_at": datetime.utcnow().isoformat()
    }
    
    expenses.append(new_expense)
    save_expenses(expenses)
    return new_expense

def update_expense(expense_id: int, updates: Dict[str, Any]) -> Dict[str, Any] | None:
    """Update existing expense"""
    expenses = load_expenses()
    
    for i, expense in enumerate(expenses):
        if expense.get("id") == expense_id:
            # Update only provided fields
            for key, value in updates.items():
                if value is not None:
                    expense[key] = value
            expenses[i] = expense
            save_expenses(expenses)
            return expense
    
    return None

def delete_expense(expense_id: int) -> bool:
    """Delete expense"""
    expenses = load_expenses()
    
    for i, expense in enumerate(expenses):
        if expense.get("id") == expense_id:
            expenses.pop(i)
            save_expenses(expenses)
            return True
    
    return False

def get_all_expenses() -> List[Dict[str, Any]]:
    """Get all expenses"""
    return load_expenses()

def get_expenses_by_category(category: str) -> List[Dict[str, Any]]:
    """Get expenses by category"""
    expenses = load_expenses()
    return [e for e in expenses if e.get("category") == category]
