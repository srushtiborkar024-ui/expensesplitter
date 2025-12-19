from fastapi import APIRouter, HTTPException, status
from typing import List
from collections import defaultdict

from app.models import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseResponse,
    SettlementRecord,
    UserSummary,
)
from app.storage import (
    create_expense,
    get_all_expenses,
    get_expense_by_id,
    update_expense,
    delete_expense,
    get_expenses_by_category,
)

router = APIRouter(prefix="/expenses", tags=["expenses"])

# ==================== CREATE EXPENSE ====================
@router.post(
    "/",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new expense"
)
def create_new_expense(expense: ExpenseCreate):
    """
    Create a new expense entry.
    
    **Parameters:**
    - `description`: What was bought (e.g., "Dinner at restaurant")
    - `amount`: Total expense amount
    - `paid_by`: Who paid (e.g., "Alice")
    - `split_between`: Who shares it (comma-separated, e.g., "Alice,Bob,Charlie")
    - `category`: Expense type (default: "General")
    """
    db_expense = create_expense(expense.model_dump())
    return db_expense

# ==================== READ EXPENSES ====================
@router.get(
    "/",
    response_model=List[ExpenseResponse],
    summary="Get all expenses"
)
def get_expenses():
    """Get all recorded expenses."""
    expenses = get_all_expenses()
    return expenses

@router.get(
    "/{expense_id}",
    response_model=ExpenseResponse,
    summary="Get expense by ID"
)
def get_single_expense(expense_id: int):
    """Get a specific expense by ID."""
    expense = get_expense_by_id(expense_id)
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with id {expense_id} not found"
        )
    return expense

@router.get(
    "/category/{category}",
    response_model=List[ExpenseResponse],
    summary="Get expenses by category"
)
def get_category_expenses(category: str):
    """Get all expenses in a specific category."""
    expenses = get_expenses_by_category(category)
    return expenses

# ==================== UPDATE EXPENSE ====================
@router.put(
    "/{expense_id}",
    response_model=ExpenseResponse,
    summary="Update an expense"
)
def update_single_expense(expense_id: int, expense_update: ExpenseUpdate):
    """Update an existing expense (only provided fields are updated)."""
    # Get update data (only non-None fields)
    update_data = expense_update.model_dump(exclude_unset=True)
    
    expense = update_expense(expense_id, update_data)
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with id {expense_id} not found"
        )
    return expense

# ==================== DELETE EXPENSE ====================
@router.delete(
    "/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an expense"
)
def delete_single_expense(expense_id: int):
    """Delete a specific expense."""
    success = delete_expense(expense_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with id {expense_id} not found"
        )

# ==================== CALCULATIONS ====================
def calculate_who_owes_whom(expenses: List[dict]) -> List[SettlementRecord]:
    """
    Core algorithm: Calculate who owes whom based on expenses.
    
    Example:
    - Alice paid $100 for dinner (split between Alice, Bob, Charlie)
    - Each person owes $33.33
    - Bob owes Alice $33.33
    - Charlie owes Alice $33.33
    """
    # Track how much each person has paid
    paid_by_person = defaultdict(float)
    
    # Track how much each person should pay (their share)
    owed_by_person = defaultdict(float)
    
    # Process each expense
    for expense in expenses:
        # Person who paid gets credit
        paid_by_person[expense["paid_by"]] += expense["amount"]
        
        # Split the expense among people
        people = [p.strip() for p in expense["split_between"].split(",")]
        share_per_person = expense["amount"] / len(people)
        
        for person in people:
            owed_by_person[person] += share_per_person
    
    # Get all unique people
    all_people = set(paid_by_person.keys()) | set(owed_by_person.keys())
    
    # Calculate balance for each person
    # Positive balance = person is owed money
    # Negative balance = person owes money
    balances = {}
    for person in all_people:
        balances[person] = paid_by_person[person] - owed_by_person[person]
    
    # Greedy algorithm to settle debts
    settlements = []
    debtors = []  # People with negative balance (owe money)
    creditors = []  # People with positive balance (owed money)
    
    for person, balance in balances.items():
        if balance < -0.01:  # Small tolerance for floating point
            debtors.append((person, -balance))
        elif balance > 0.01:
            creditors.append((person, balance))
    
    # Match debtors with creditors
    for debtor_name, debtor_amount in debtors:
        for i, (creditor_name, creditor_amount) in enumerate(creditors):
            # Settle minimum of what debtor owes and creditor is owed
            settle_amount = min(debtor_amount, creditor_amount)
            
            if settle_amount > 0.01:
                settlements.append(
                    SettlementRecord(
                        debtor=debtor_name,
                        creditor=creditor_name,
                        amount=round(settle_amount, 2)
                    )
                )
                
                # Update remaining amounts
                debtor_amount -= settle_amount
                creditors[i] = (creditor_name, creditor_amount - settle_amount)
    
    return settlements

@router.get(
    "/settle/who-owes-whom",
    response_model=List[SettlementRecord],
    summary="Calculate who owes whom"
)
def settle_up():
    """
    Calculate final settlements: who needs to pay whom and how much.
    
    This uses an optimal algorithm to minimize the number of transactions needed.
    """
    expenses = get_all_expenses()
    settlements = calculate_who_owes_whom(expenses)
    return settlements

@router.get(
    "/summary/user/{username}",
    response_model=UserSummary,
    summary="Get user's financial summary"
)
def get_user_summary(username: str):
    """Get financial summary for a specific user."""
    expenses = get_all_expenses()
    
    total_paid = 0.0
    total_owed = 0.0
    
    for expense in expenses:
        # Check if user paid
        if expense["paid_by"] == username:
            total_paid += expense["amount"]
        
        # Check if user is in the split
        people = [p.strip() for p in expense["split_between"].split(",")]
        if username in people:
            share = expense["amount"] / len(people)
            total_owed += share
    
    balance = total_paid - total_owed
    
    return UserSummary(
        name=username,
        total_paid=round(total_paid, 2),
        total_owed=round(total_owed, 2),
        balance=round(balance, 2)
    )

@router.get(
    "/summary/all",
    response_model=List[UserSummary],
    summary="Get all users' financial summary"
)
def get_all_summaries():
    """Get financial summary for all users in the expenses."""
    expenses = get_all_expenses()
    
    # Extract all unique people
    all_people = set()
    for expense in expenses:
        all_people.add(expense["paid_by"])
        people = [p.strip() for p in expense["split_between"].split(",")]
        all_people.update(people)
    
    # Calculate summary for each person
    summaries = []
    for person in sorted(all_people):
        total_paid = 0.0
        total_owed = 0.0
        
        for expense in expenses:
            if expense["paid_by"] == person:
                total_paid += expense["amount"]
            
            people = [p.strip() for p in expense["split_between"].split(",")]
            if person in people:
                share = expense["amount"] / len(people)
                total_owed += share
        
        balance = total_paid - total_owed
        
        summaries.append(
            UserSummary(
                name=person,
                total_paid=round(total_paid, 2),
                total_owed=round(total_owed, 2),
                balance=round(balance, 2)
            )
        )
    
    return summaries

@router.get(
    "/stats/total",
    summary="Get total expense statistics"
)
def get_statistics():
    """Get overall statistics about expenses."""
    expenses = get_all_expenses()
    
    if not expenses:
        return {
            "total_expenses": 0,
            "total_amount": 0.0,
            "unique_people": 0,
            "categories": [],
            "people": []
        }
    
    total_amount = sum(e["amount"] for e in expenses)
    categories = list(set(e["category"] for e in expenses))
    
    # Get unique people
    all_people = set()
    for expense in expenses:
        all_people.add(expense["paid_by"])
        people = [p.strip() for p in expense["split_between"].split(",")]
        all_people.update(people)
    
    return {
        "total_expenses": len(expenses),
        "total_amount": round(total_amount, 2),
        "unique_people": len(all_people),
        "categories": categories,
        "people": sorted(list(all_people))
    }
