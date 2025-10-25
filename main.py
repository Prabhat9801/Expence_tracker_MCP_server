from fastmcp import FastMCP
import os
import aiosqlite  # Changed: sqlite3 → aiosqlite
import tempfile
import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
# Use temporary directory which should be writable
TEMP_DIR = tempfile.gettempdir()
DB_PATH = os.path.join(TEMP_DIR, "expenses.db")
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

print(f"Database path: {DB_PATH}")

mcp = FastMCP("ExpenseTracker")

def init_db():  # Keep as sync for initialization
    try:
        # Use synchronous sqlite3 just for initialization
        import sqlite3
        with sqlite3.connect(DB_PATH) as c:
            c.execute("PRAGMA journal_mode=WAL")
            c.execute("""
                CREATE TABLE IF NOT EXISTS expenses(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    subcategory TEXT DEFAULT '',
                    note TEXT DEFAULT ''
                )
            """)
            
            # Create budgets table
            c.execute("""
                CREATE TABLE IF NOT EXISTS budgets(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    amount REAL NOT NULL,
                    period TEXT NOT NULL,  -- 'monthly', 'weekly', 'yearly'
                    start_date TEXT NOT NULL,
                    end_date TEXT,
                    created_date TEXT NOT NULL,
                    is_active INTEGER DEFAULT 1
                )
            """)
            
            # Create recurring_expenses table for tracking subscriptions/recurring payments
            c.execute("""
                CREATE TABLE IF NOT EXISTS recurring_expenses(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    subcategory TEXT DEFAULT '',
                    frequency TEXT NOT NULL,  -- 'weekly', 'monthly', 'yearly'
                    next_due_date TEXT NOT NULL,
                    is_active INTEGER DEFAULT 1,
                    created_date TEXT NOT NULL,
                    note TEXT DEFAULT ''
                )
            """)
            
            # Test write access
            c.execute("INSERT OR IGNORE INTO expenses(date, amount, category) VALUES ('2000-01-01', 0, 'test')")
            c.execute("DELETE FROM expenses WHERE category = 'test'")
            print("Database initialized successfully with write access")
    except Exception as e:
        print(f"Database initialization error: {e}")
        raise

# Initialize database synchronously at module load
init_db()

@mcp.tool()
async def add_expense(date, amount, category, subcategory="", note=""):  # Changed: added async
    '''Add a new expense entry to the database.'''
    try:
        async with aiosqlite.connect(DB_PATH) as c:  # Changed: added async
            cur = await c.execute(  # Changed: added await
                "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
                (date, amount, category, subcategory, note)
            )
            expense_id = cur.lastrowid
            await c.commit()  # Changed: added await
            return {"status": "success", "id": expense_id, "message": "Expense added successfully"}
    except Exception as e:  # Changed: simplified exception handling
        if "readonly" in str(e).lower():
            return {"status": "error", "message": "Database is in read-only mode. Check file permissions."}
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
@mcp.tool()
async def list_expenses(start_date, end_date):  # Changed: added async
    '''List expense entries within an inclusive date range.'''
    try:
        async with aiosqlite.connect(DB_PATH) as c:  # Changed: added async
            cur = await c.execute(  # Changed: added await
                """
                SELECT id, date, amount, category, subcategory, note
                FROM expenses
                WHERE date BETWEEN ? AND ?
                ORDER BY date DESC, id DESC
                """,
                (start_date, end_date)
            )
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, r)) for r in await cur.fetchall()]  # Changed: added await
    except Exception as e:
        return {"status": "error", "message": f"Error listing expenses: {str(e)}"}

@mcp.tool()
async def summarize(start_date, end_date, category=None):  # Changed: added async
    '''Summarize expenses by category within an inclusive date range.'''
    try:
        async with aiosqlite.connect(DB_PATH) as c:  # Changed: added async
            query = """
                SELECT category, SUM(amount) AS total_amount, COUNT(*) as count
                FROM expenses
                WHERE date BETWEEN ? AND ?
            """
            params = [start_date, end_date]

            if category:
                query += " AND category = ?"
                params.append(category)

            query += " GROUP BY category ORDER BY total_amount DESC"

            cur = await c.execute(query, params)  # Changed: added await
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, r)) for r in await cur.fetchall()]  # Changed: added await
    except Exception as e:
        return {"status": "error", "message": f"Error summarizing expenses: {str(e)}"}

@mcp.tool()
async def delete_expense(expense_id):
    '''Delete an expense entry by ID.'''
    try:
        async with aiosqlite.connect(DB_PATH) as c:
            cur = await c.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
            expense = await cur.fetchone()
            
            if not expense:
                return {"status": "error", "message": f"Expense with ID {expense_id} not found"}
            
            await c.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
            await c.commit()
            return {"status": "success", "message": f"Expense {expense_id} deleted successfully"}
    except Exception as e:
        return {"status": "error", "message": f"Error deleting expense: {str(e)}"}

@mcp.tool()
async def update_expense(expense_id, date=None, amount=None, category=None, subcategory=None, note=None):
    '''Update an existing expense entry. Only provided fields will be updated.'''
    try:
        async with aiosqlite.connect(DB_PATH) as c:
            # First check if expense exists
            cur = await c.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
            existing = await cur.fetchone()
            
            if not existing:
                return {"status": "error", "message": f"Expense with ID {expense_id} not found"}
            
            # Build update query dynamically
            updates = []
            params = []
            
            if date is not None:
                updates.append("date = ?")
                params.append(date)
            if amount is not None:
                updates.append("amount = ?")
                params.append(amount)
            if category is not None:
                updates.append("category = ?")
                params.append(category)
            if subcategory is not None:
                updates.append("subcategory = ?")
                params.append(subcategory)
            if note is not None:
                updates.append("note = ?")
                params.append(note)
            
            if not updates:
                return {"status": "error", "message": "No fields provided to update"}
            
            query = f"UPDATE expenses SET {', '.join(updates)} WHERE id = ?"
            params.append(expense_id)
            
            await c.execute(query, params)
            await c.commit()
            
            # Return updated expense
            cur = await c.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
            updated = await cur.fetchone()
            cols = [d[0] for d in cur.description]
            return {"status": "success", "expense": dict(zip(cols, updated))}
    except Exception as e:
        return {"status": "error", "message": f"Error updating expense: {str(e)}"}

@mcp.tool()
async def get_expense_by_id(expense_id):
    '''Get a specific expense by its ID.'''
    try:
        async with aiosqlite.connect(DB_PATH) as c:
            cur = await c.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
            expense = await cur.fetchone()
            
            if not expense:
                return {"status": "error", "message": f"Expense with ID {expense_id} not found"}
            
            cols = [d[0] for d in cur.description]
            return {"status": "success", "expense": dict(zip(cols, expense))}
    except Exception as e:
        return {"status": "error", "message": f"Error retrieving expense: {str(e)}"}

@mcp.tool()
async def search_expenses(keyword, start_date=None, end_date=None):
    '''Search expenses by keyword in category, subcategory, or note fields.'''
    try:
        async with aiosqlite.connect(DB_PATH) as c:
            query = """
                SELECT id, date, amount, category, subcategory, note
                FROM expenses
                WHERE (category LIKE ? OR subcategory LIKE ? OR note LIKE ?)
            """
            params = [f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"]
            
            if start_date and end_date:
                query += " AND date BETWEEN ? AND ?"
                params.extend([start_date, end_date])
            elif start_date:
                query += " AND date >= ?"
                params.append(start_date)
            elif end_date:
                query += " AND date <= ?"
                params.append(end_date)
            
            query += " ORDER BY date DESC, id DESC"
            
            cur = await c.execute(query, params)
            cols = [d[0] for d in cur.description]
            results = [dict(zip(cols, r)) for r in await cur.fetchall()]
            
            return {"status": "success", "results": results, "count": len(results)}
    except Exception as e:
        return {"status": "error", "message": f"Error searching expenses: {str(e)}"}

@mcp.tool()
async def get_monthly_summary(year, month=None):
    '''Get monthly summary of expenses. If month is not provided, returns summary for all months in the year.'''
    try:
        async with aiosqlite.connect(DB_PATH) as c:
            if month:
                # Specific month summary
                start_date = f"{year}-{month:02d}-01"
                if month == 12:
                    end_date = f"{year+1}-01-01"
                else:
                    end_date = f"{year}-{month+1:02d}-01"
                
                cur = await c.execute("""
                    SELECT 
                        category,
                        SUM(amount) as total_amount,
                        COUNT(*) as transaction_count,
                        AVG(amount) as avg_amount
                    FROM expenses
                    WHERE date >= ? AND date < ?
                    GROUP BY category
                    ORDER BY total_amount DESC
                """, (start_date, end_date))
                
                cols = [d[0] for d in cur.description]
                category_summary = [dict(zip(cols, r)) for r in await cur.fetchall()]
                
                # Get total for the month
                cur = await c.execute("""
                    SELECT 
                        SUM(amount) as total,
                        COUNT(*) as total_transactions
                    FROM expenses
                    WHERE date >= ? AND date < ?
                """, (start_date, end_date))
                
                total_data = await cur.fetchone()
                
                return {
                    "status": "success",
                    "year": year,
                    "month": month,
                    "total_amount": total_data[0] or 0,
                    "total_transactions": total_data[1] or 0,
                    "categories": category_summary
                }
            else:
                # Yearly summary by month
                cur = await c.execute("""
                    SELECT 
                        strftime('%m', date) as month,
                        SUM(amount) as total_amount,
                        COUNT(*) as transaction_count
                    FROM expenses
                    WHERE strftime('%Y', date) = ?
                    GROUP BY strftime('%m', date)
                    ORDER BY month
                """, (str(year),))
                
                cols = [d[0] for d in cur.description]
                monthly_data = [dict(zip(cols, r)) for r in await cur.fetchall()]
                
                # Convert month numbers to names
                month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                
                for item in monthly_data:
                    item['month_name'] = month_names[int(item['month']) - 1]
                
                return {
                    "status": "success",
                    "year": year,
                    "monthly_breakdown": monthly_data
                }
                
    except Exception as e:
        return {"status": "error", "message": f"Error getting monthly summary: {str(e)}"}

@mcp.tool()
async def get_top_expenses(start_date, end_date, limit=10):
    '''Get the top N highest expenses within a date range.'''
    try:
        async with aiosqlite.connect(DB_PATH) as c:
            cur = await c.execute("""
                SELECT id, date, amount, category, subcategory, note
                FROM expenses
                WHERE date BETWEEN ? AND ?
                ORDER BY amount DESC
                LIMIT ?
            """, (start_date, end_date, limit))
            
            cols = [d[0] for d in cur.description]
            results = [dict(zip(cols, r)) for r in await cur.fetchall()]
            
            return {"status": "success", "top_expenses": results, "count": len(results)}
    except Exception as e:
        return {"status": "error", "message": f"Error getting top expenses: {str(e)}"}

@mcp.tool()
async def get_expense_statistics(start_date, end_date):
    '''Get comprehensive statistics for expenses within a date range.'''
    try:
        async with aiosqlite.connect(DB_PATH) as c:
            # Basic statistics
            cur = await c.execute("""
                SELECT 
                    COUNT(*) as total_transactions,
                    SUM(amount) as total_amount,
                    AVG(amount) as average_amount,
                    MIN(amount) as min_amount,
                    MAX(amount) as max_amount
                FROM expenses
                WHERE date BETWEEN ? AND ?
            """, (start_date, end_date))
            
            basic_stats = await cur.fetchone()
            
            # Category breakdown
            cur = await c.execute("""
                SELECT 
                    category,
                    COUNT(*) as count,
                    SUM(amount) as total,
                    AVG(amount) as average
                FROM expenses
                WHERE date BETWEEN ? AND ?
                GROUP BY category
                ORDER BY total DESC
            """, (start_date, end_date))
            
            category_cols = [d[0] for d in cur.description]
            category_stats = [dict(zip(category_cols, r)) for r in await cur.fetchall()]
            
            # Daily average
            cur = await c.execute("""
                SELECT COUNT(DISTINCT date) as unique_days
                FROM expenses
                WHERE date BETWEEN ? AND ?
            """, (start_date, end_date))
            
            unique_days = (await cur.fetchone())[0]
            daily_average = (basic_stats[1] or 0) / max(unique_days, 1)
            
            return {
                "status": "success",
                "period": {"start_date": start_date, "end_date": end_date},
                "basic_statistics": {
                    "total_transactions": basic_stats[0] or 0,
                    "total_amount": basic_stats[1] or 0,
                    "average_amount": basic_stats[2] or 0,
                    "min_amount": basic_stats[3] or 0,
                    "max_amount": basic_stats[4] or 0,
                    "daily_average": daily_average
                },
                "category_breakdown": category_stats
            }
    except Exception as e:
        return {"status": "error", "message": f"Error getting statistics: {str(e)}"}

@mcp.tool()
async def bulk_add_expenses(expenses):
    '''Add multiple expenses at once. Expects a list of expense dictionaries.'''
    try:
        success_count = 0
        errors = []
        
        async with aiosqlite.connect(DB_PATH) as c:
            for i, expense in enumerate(expenses):
                try:
                    await c.execute(
                        "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
                        (
                            expense.get('date'),
                            expense.get('amount'),
                            expense.get('category'),
                            expense.get('subcategory', ''),
                            expense.get('note', '')
                        )
                    )
                    success_count += 1
                except Exception as e:
                    errors.append(f"Row {i+1}: {str(e)}")
            
            await c.commit()
        
        return {
            "status": "success" if not errors else "partial_success",
            "added_count": success_count,
            "total_count": len(expenses),
            "errors": errors
        }
    except Exception as e:
        return {"status": "error", "message": f"Error in bulk add: {str(e)}"}

@mcp.tool()
async def get_category_trends(category, start_date, end_date, group_by="month"):
    '''Get spending trends for a specific category over time. group_by can be "day", "week", or "month".'''
    try:
        async with aiosqlite.connect(DB_PATH) as c:
            if group_by == "day":
                date_format = "%Y-%m-%d"
                group_format = "date"
            elif group_by == "week":
                date_format = "%Y-W%W"
                group_format = "strftime('%Y-W%W', date)"
            else:  # month
                date_format = "%Y-%m"
                group_format = "strftime('%Y-%m', date)"
            
            query = f"""
                SELECT 
                    {group_format} as period,
                    SUM(amount) as total_amount,
                    COUNT(*) as transaction_count,
                    AVG(amount) as avg_amount
                FROM expenses
                WHERE category = ? AND date BETWEEN ? AND ?
                GROUP BY {group_format}
                ORDER BY period
            """
            
            cur = await c.execute(query, (category, start_date, end_date))
            cols = [d[0] for d in cur.description]
            trends = [dict(zip(cols, r)) for r in await cur.fetchall()]
            
            return {
                "status": "success",
                "category": category,
                "period": {"start_date": start_date, "end_date": end_date},
                "group_by": group_by,
                "trends": trends
            }
    except Exception as e:
        return {"status": "error", "message": f"Error getting category trends: {str(e)}"}

# Budget Management Tools
@mcp.tool()
async def create_budget(category, amount, period, start_date, end_date=None):
    '''Create a budget for a category. Period can be "monthly", "weekly", or "yearly".'''
    try:
        async with aiosqlite.connect(DB_PATH) as c:
            created_date = datetime.now().isoformat()
            
            await c.execute("""
                INSERT INTO budgets(category, amount, period, start_date, end_date, created_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (category, amount, period, start_date, end_date, created_date))
            
            budget_id = c.lastrowid
            await c.commit()
            
            return {
                "status": "success",
                "budget_id": budget_id,
                "message": f"Budget created for {category}: {amount} per {period}"
            }
    except Exception as e:
        return {"status": "error", "message": f"Error creating budget: {str(e)}"}

@mcp.tool()
async def get_budgets(active_only=True):
    '''Get all budgets, optionally filter to active budgets only.'''
    try:
        async with aiosqlite.connect(DB_PATH) as c:
            query = "SELECT * FROM budgets"
            if active_only:
                query += " WHERE is_active = 1"
            query += " ORDER BY created_date DESC"
            
            cur = await c.execute(query)
            cols = [d[0] for d in cur.description]
            budgets = [dict(zip(cols, r)) for r in await cur.fetchall()]
            
            return {"status": "success", "budgets": budgets}
    except Exception as e:
        return {"status": "error", "message": f"Error getting budgets: {str(e)}"}

@mcp.tool()
async def check_budget_status(start_date, end_date):
    '''Check budget vs actual spending for all active budgets in the given period.'''
    try:
        async with aiosqlite.connect(DB_PATH) as c:
            # Get active budgets
            cur = await c.execute("SELECT * FROM budgets WHERE is_active = 1")
            budgets = await cur.fetchall()
            budget_cols = [d[0] for d in cur.description]
            
            budget_status = []
            
            for budget_row in budgets:
                budget = dict(zip(budget_cols, budget_row))
                category = budget['category']
                budget_amount = budget['amount']
                
                # Get actual spending for this category
                cur = await c.execute("""
                    SELECT COALESCE(SUM(amount), 0) as total_spent
                    FROM expenses
                    WHERE category = ? AND date BETWEEN ? AND ?
                """, (category, start_date, end_date))
                
                total_spent = (await cur.fetchone())[0]
                remaining = budget_amount - total_spent
                percentage_used = (total_spent / budget_amount * 100) if budget_amount > 0 else 0
                
                status = "under_budget"
                if percentage_used >= 100:
                    status = "over_budget"
                elif percentage_used >= 80:
                    status = "near_limit"
                
                budget_status.append({
                    "budget_id": budget['id'],
                    "category": category,
                    "budget_amount": budget_amount,
                    "spent_amount": total_spent,
                    "remaining_amount": remaining,
                    "percentage_used": round(percentage_used, 2),
                    "status": status,
                    "period": budget['period']
                })
            
            return {
                "status": "success",
                "period": {"start_date": start_date, "end_date": end_date},
                "budget_status": budget_status
            }
    except Exception as e:
        return {"status": "error", "message": f"Error checking budget status: {str(e)}"}

@mcp.tool()
async def update_budget(budget_id, amount=None, is_active=None, end_date=None):
    '''Update an existing budget.'''
    try:
        async with aiosqlite.connect(DB_PATH) as c:
            # Check if budget exists
            cur = await c.execute("SELECT * FROM budgets WHERE id = ?", (budget_id,))
            budget = await cur.fetchone()
            
            if not budget:
                return {"status": "error", "message": f"Budget with ID {budget_id} not found"}
            
            # Build update query
            updates = []
            params = []
            
            if amount is not None:
                updates.append("amount = ?")
                params.append(amount)
            if is_active is not None:
                updates.append("is_active = ?")
                params.append(1 if is_active else 0)
            if end_date is not None:
                updates.append("end_date = ?")
                params.append(end_date)
            
            if not updates:
                return {"status": "error", "message": "No fields provided to update"}
            
            query = f"UPDATE budgets SET {', '.join(updates)} WHERE id = ?"
            params.append(budget_id)
            
            await c.execute(query, params)
            await c.commit()
            
            return {"status": "success", "message": "Budget updated successfully"}
    except Exception as e:
        return {"status": "error", "message": f"Error updating budget: {str(e)}"}

# Recurring Expenses Management
@mcp.tool()
async def add_recurring_expense(name, amount, category, frequency, next_due_date, subcategory="", note=""):
    '''Add a recurring expense (like subscriptions). Frequency can be "weekly", "monthly", "yearly".'''
    try:
        async with aiosqlite.connect(DB_PATH) as c:
            created_date = datetime.now().isoformat()
            
            cur = await c.execute("""
                INSERT INTO recurring_expenses(name, amount, category, subcategory, frequency, next_due_date, created_date, note)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, amount, category, subcategory, frequency, next_due_date, created_date, note))
            
            recurring_id = cur.lastrowid
            await c.commit()
            
            return {
                "status": "success",
                "recurring_id": recurring_id,
                "message": f"Recurring expense '{name}' added successfully"
            }
    except Exception as e:
        return {"status": "error", "message": f"Error adding recurring expense: {str(e)}"}

@mcp.tool()
async def get_recurring_expenses(active_only=True):
    '''Get all recurring expenses.'''
    try:
        async with aiosqlite.connect(DB_PATH) as c:
            query = "SELECT * FROM recurring_expenses"
            if active_only:
                query += " WHERE is_active = 1"
            query += " ORDER BY next_due_date ASC"
            
            cur = await c.execute(query)
            cols = [d[0] for d in cur.description]
            recurring = [dict(zip(cols, r)) for r in await cur.fetchall()]
            
            return {"status": "success", "recurring_expenses": recurring}
    except Exception as e:
        return {"status": "error", "message": f"Error getting recurring expenses: {str(e)}"}

@mcp.tool()
async def get_due_recurring_expenses(days_ahead=7):
    '''Get recurring expenses that are due within the specified number of days.'''
    try:
        from datetime import datetime, timedelta
        
        today = datetime.now().date()
        cutoff_date = today + timedelta(days=days_ahead)
        
        async with aiosqlite.connect(DB_PATH) as c:
            cur = await c.execute("""
                SELECT * FROM recurring_expenses
                WHERE is_active = 1 AND date(next_due_date) <= ?
                ORDER BY next_due_date ASC
            """, (cutoff_date.isoformat(),))
            
            cols = [d[0] for d in cur.description]
            due_expenses = [dict(zip(cols, r)) for r in await cur.fetchall()]
            
            return {
                "status": "success",
                "due_expenses": due_expenses,
                "days_ahead": days_ahead,
                "cutoff_date": cutoff_date.isoformat()
            }
    except Exception as e:
        return {"status": "error", "message": f"Error getting due recurring expenses: {str(e)}"}

@mcp.tool()
async def process_recurring_expense(recurring_id, process_date=None):
    '''Process a recurring expense by adding it to expenses and updating the next due date.'''
    try:
        from datetime import datetime, timedelta
        
        if process_date is None:
            process_date = datetime.now().date().isoformat()
        
        async with aiosqlite.connect(DB_PATH) as c:
            # Get the recurring expense
            cur = await c.execute("SELECT * FROM recurring_expenses WHERE id = ? AND is_active = 1", (recurring_id,))
            recurring = await cur.fetchone()
            
            if not recurring:
                return {"status": "error", "message": f"Active recurring expense with ID {recurring_id} not found"}
            
            cols = [d[0] for d in cur.description]
            recurring_dict = dict(zip(cols, recurring))
            
            # Add expense entry
            await c.execute("""
                INSERT INTO expenses(date, amount, category, subcategory, note)
                VALUES (?, ?, ?, ?, ?)
            """, (
                process_date,
                recurring_dict['amount'],
                recurring_dict['category'],
                recurring_dict['subcategory'],
                f"Recurring: {recurring_dict['name']} - {recurring_dict['note']}"
            ))
            
            # Calculate next due date
            current_due = datetime.fromisoformat(recurring_dict['next_due_date']).date()
            
            if recurring_dict['frequency'] == 'weekly':
                next_due = current_due + timedelta(weeks=1)
            elif recurring_dict['frequency'] == 'monthly':
                # Add one month (approximate)
                if current_due.month == 12:
                    next_due = current_due.replace(year=current_due.year + 1, month=1)
                else:
                    next_due = current_due.replace(month=current_due.month + 1)
            elif recurring_dict['frequency'] == 'yearly':
                next_due = current_due.replace(year=current_due.year + 1)
            else:
                return {"status": "error", "message": f"Unknown frequency: {recurring_dict['frequency']}"}
            
            # Update next due date
            await c.execute("""
                UPDATE recurring_expenses
                SET next_due_date = ?
                WHERE id = ?
            """, (next_due.isoformat(), recurring_id))
            
            await c.commit()
            
            return {
                "status": "success",
                "message": f"Processed recurring expense '{recurring_dict['name']}'",
                "expense_added": {
                    "date": process_date,
                    "amount": recurring_dict['amount'],
                    "category": recurring_dict['category']
                },
                "next_due_date": next_due.isoformat()
            }
    except Exception as e:
        return {"status": "error", "message": f"Error processing recurring expense: {str(e)}"}

@mcp.tool()
async def export_expenses_csv(start_date, end_date):
    '''Export expenses to CSV format for the given date range.'''
    try:
        async with aiosqlite.connect(DB_PATH) as c:
            cur = await c.execute("""
                SELECT date, amount, category, subcategory, note
                FROM expenses
                WHERE date BETWEEN ? AND ?
                ORDER BY date DESC
            """, (start_date, end_date))
            
            expenses = await cur.fetchall()
            
            # Create CSV content
            csv_lines = ["Date,Amount,Category,Subcategory,Note"]
            for expense in expenses:
                # Escape commas and quotes in text fields
                row = []
                for field in expense:
                    if isinstance(field, str) and (',' in field or '"' in field):
                        field = f'"{field.replace(chr(34), chr(34)+chr(34))}"'
                    row.append(str(field))
                csv_lines.append(','.join(row))
            
            csv_content = '\n'.join(csv_lines)
            
            return {
                "status": "success",
                "csv_content": csv_content,
                "record_count": len(expenses),
                "date_range": {"start_date": start_date, "end_date": end_date}
            }
    except Exception as e:
        return {"status": "error", "message": f"Error exporting to CSV: {str(e)}"}

@mcp.resource("expense:///categories", mime_type="application/json")  # Changed: expense:// → expense:///
def categories():
    try:
        # Provide default categories if file doesn't exist
        default_categories = {
            "categories": [
                "Food & Dining",
                "Transportation",
                "Shopping",
                "Entertainment",
                "Bills & Utilities",
                "Healthcare",
                "Travel",
                "Education",
                "Business",
                "Other"
            ]
        }
        
        try:
            with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            import json
            return json.dumps(default_categories, indent=2)
    except Exception as e:
        return f'{{"error": "Could not load categories: {str(e)}"}}'

# Start the server
if __name__ == "__main__":
    # When running directly (not through fastmcp), start HTTP server
    mcp.run(transport="http", host="0.0.0.0", port=8000)
    # When running through fastmcp dev, this block won't execute