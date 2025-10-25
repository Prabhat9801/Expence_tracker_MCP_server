# 💰 Advanced Expense Tracker MCP Server

A comprehensive Model Context Protocol (MCP) server for tracking and analyzing personal expenses with advanced analytics and insights.

🌐 **Live Server:** https://prabhatmcp.fastmcp.app/mcp  
📁 **GitHub Repository:** https://github.com/Prabhat9801/Expence_tracker_MCP_server

## 🌟 Features

### 💳 Core Expense Management
- ✅ **Add Expense** - Record new expenses with date, amount, category, subcategory, and notes
- ✅ **Update Expense** - Modify existing expense entries
- ✅ **Delete Expense** - Remove expense entries by ID
- ✅ **Get Expense** - Retrieve specific expense details
- ✅ **List Expenses** - View expenses within date ranges
- ✅ **Bulk Add** - Add multiple expenses at once
- ✅ **Search Expenses** - Find expenses by keywords across all fields

### 📊 Analytics & Insights
- � **Spending Statistics** - Comprehensive stats with min/max/average analysis
- � **Monthly Analysis** - Detailed monthly spending breakdowns by category
- � **Category Trends** - Track spending patterns over time (daily/weekly/monthly)
- 🔝 **Top Expenses** - Identify highest spending transactions
- 📅 **Date Range Analysis** - Flexible period-based expense analysis
- � **Category Summaries** - Spending summaries grouped by categories

### 💰 Budget Management
- 🎯 **Create Budgets** - Set spending limits by category (monthly/weekly/yearly)
- � **Budget Tracking** - Monitor actual spending vs budgets
- ⚠️ **Budget Alerts** - Get status warnings when approaching limits
- 📈 **Budget Analysis** - Percentage usage and remaining amounts
- ✏️ **Update Budgets** - Modify existing budget parameters

### 🔄 Recurring Expenses
- 📅 **Add Recurring** - Track subscriptions and recurring payments
- 🔔 **Due Notifications** - Get upcoming payment reminders
- ⚡ **Auto Processing** - Convert recurring expenses to actual expenses
- 📝 **Manage Subscriptions** - Full lifecycle management of recurring costs

### 📥 Data Management
- 📤 **CSV Export** - Export expense data for external analysis
- 📋 **Category Management** - Comprehensive predefined expense categories
- 🏥 **Health Monitoring** - Server health check and status monitoring
- 💾 **Cloud Storage** - Secure cloud database with persistence
- 🔄 **Real-time Updates** - Instant expense tracking and retrieval

## 🚀 Quick Start

### Access the Live Server
The server is already deployed and accessible at:
**https://prabhatmcp.fastmcp.app/mcp**

### Using with MCP Clients
Connect your MCP client to the server URL above to start tracking expenses immediately.

### Local Development
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Prabhat9801/Expence_tracker_MCP_server.git
   cd Expence_tracker_MCP_server
   ```

2. **Install dependencies:**
   ```bash
   pip install fastmcp aiosqlite
   ```

3. **Run locally:**
   ```bash
   uv run fastmcp dev main.py
   ```

## 📚 Available Tools

### 🎯 Core Operations

#### `add_expense`
Add a new expense entry to the database.
```json
{
  "date": "2024-10-25",
  "amount": 25.50,
  "category": "Food & Dining",
  "subcategory": "Coffee",
  "note": "Morning coffee at Starbucks"
}
```

#### `list_expenses`
List expenses within a date range.
```json
{
  "start_date": "2024-10-01",
  "end_date": "2024-10-31"
}
```

#### `update_expense`
Update an existing expense entry.
```json
{
  "expense_id": 123,
  "amount": 30.00,
  "note": "Updated amount"
}
```

#### `delete_expense`
Remove an expense by ID.
```json
{
  "expense_id": 123
}
```

#### `get_expense_by_id`
Get a specific expense by its ID.
```json
{
  "expense_id": 123
}
```

### 🔍 Search & Analysis Tools

#### `search_expenses`
Search expenses by keyword across categories, subcategories, and notes.
```json
{
  "keyword": "coffee",
  "start_date": "2024-10-01",
  "end_date": "2024-10-31"
}
```

#### `get_top_expenses`
Get the highest expenses within a date range.
```json
{
  "start_date": "2024-10-01",
  "end_date": "2024-10-31",
  "limit": 10
}
```

#### `get_expense_statistics`
Comprehensive spending statistics and category breakdowns.
```json
{
  "start_date": "2024-01-01",
  "end_date": "2024-12-31"
}
```

#### `get_category_trends`
Track spending trends for a specific category over time.
```json
{
  "category": "Food & Dining",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "group_by": "month"
}
```

### 📊 Summary & Analytics

#### `summarize`
Get expense summaries by category for a date range.
```json
{
  "start_date": "2024-10-01",
  "end_date": "2024-10-31",
  "category": "Food & Dining"
}
```

#### `get_monthly_summary`
Get detailed monthly expense analysis.
```json
{
  "year": 2024,
  "month": 10
}
```

### 💰 Budget Management

#### `create_budget`
Create a budget for a specific category.
```json
{
  "category": "Food & Dining",
  "amount": 500.00,
  "period": "monthly",
  "start_date": "2024-10-01"
}
```

#### `get_budgets`
List all budgets (active or all).
```json
{
  "active_only": true
}
```

#### `check_budget_status`
Check budget vs actual spending.
```json
{
  "start_date": "2024-10-01",
  "end_date": "2024-10-31"
}
```

#### `update_budget`
Update an existing budget.
```json
{
  "budget_id": 1,
  "amount": 600.00,
  "is_active": true
}
```

### 🔄 Recurring Expenses

#### `add_recurring_expense`
Add a recurring expense (subscriptions, etc.).
```json
{
  "name": "Netflix Subscription",
  "amount": 15.99,
  "category": "Entertainment",
  "frequency": "monthly",
  "next_due_date": "2024-11-01"
}
```

#### `get_recurring_expenses`
List all recurring expenses.
```json
{
  "active_only": true
}
```

#### `get_due_recurring_expenses`
Get recurring expenses due within specified days.
```json
{
  "days_ahead": 7
}
```

#### `process_recurring_expense`
Process a recurring expense (add to expenses and update next due date).
```json
{
  "recurring_id": 1,
  "process_date": "2024-10-25"
}
```

### 📥 Bulk Operations

#### `bulk_add_expenses`
Add multiple expenses at once.
```json
{
  "expenses": [
    {
      "date": "2024-10-25",
      "amount": 12.99,
      "category": "Food & Dining",
      "note": "Lunch"
    },
    {
      "date": "2024-10-25",
      "amount": 3.50,
      "category": "Transportation",
      "note": "Bus fare"
    }
  ]
}
```

#### `export_expenses_csv`
Export expenses to CSV format.
```json
{
  "start_date": "2024-01-01",
  "end_date": "2024-12-31"
}
```

## 📊 Expense Categories

The system includes comprehensive expense categories:

### Main Categories:
- 🍽️ **Food & Dining** - Restaurants, groceries, delivery
- 🚗 **Transportation** - Gas, public transport, rideshare
- 🛒 **Shopping** - Clothing, electronics, retail
- 🎬 **Entertainment** - Movies, games, subscriptions
- 💡 **Bills & Utilities** - Rent, electricity, internet
- 🏥 **Healthcare** - Medical, pharmacy, insurance
- ✈️ **Travel** - Flights, hotels, vacation
- 📚 **Education** - Courses, books, training
- 💼 **Business** - Office supplies, software
- ❓ **Other** - Miscellaneous expenses

## 🌐 Cloud Deployment

### Server Information
- **Hosting:** FastMCP Cloud
- **URL:** https://prabhatmcp.fastmcp.app/mcp
- **Database:** Cloud SQLite with persistent storage
- **Uptime:** 24/7 availability
- **Version:** 1.0.0

### Features
- ✅ Auto-scaling cloud infrastructure
- ✅ Persistent data storage
- ✅ Real-time expense tracking
- ✅ RESTful MCP interface
- ✅ Health monitoring
- ✅ Error handling and logging

## 📝 Usage Examples

### 💰 Basic Expense Operations

**Adding Your First Expense:**
```json
{
  "date": "2025-10-25",
  "amount": 12.99,
  "category": "food",
  "subcategory": "dining_out",
  "note": "Subway sandwich for lunch"
}
```

**Updating an Expense:**
```json
{
  "expense_id": 123,
  "amount": 15.99,
  "note": "Updated: Actually got a combo meal"
}
```

**Searching for Expenses:**
```json
{
  "keyword": "coffee",
  "start_date": "2025-10-01",
  "end_date": "2025-10-31"
}
```

### 📊 Analytics & Reporting

**Monthly Spending Analysis:**
```json
{
  "year": 2025,
  "month": 10
}
```

**Category Spending Trends:**
```json
{
  "category": "food",
  "start_date": "2025-01-01",
  "end_date": "2025-12-31",
  "group_by": "month"
}
```

**Get Top Expenses:**
```json
{
  "start_date": "2025-10-01",
  "end_date": "2025-10-31",
  "limit": 5
}
```

**Overall Statistics:**
```json
{
  "start_date": "2025-01-01",
  "end_date": "2025-12-31"
}
```

### 💰 Budget Management

**Create a Monthly Budget:**
```json
{
  "category": "food",
  "amount": 500.00,
  "period": "monthly",
  "start_date": "2025-10-01"
}
```

**Check Budget Status:**
```json
{
  "start_date": "2025-10-01",
  "end_date": "2025-10-31"
}
```

### 🔄 Recurring Expenses

**Add a Subscription:**
```json
{
  "name": "Netflix Subscription",
  "amount": 15.99,
  "category": "entertainment",
  "subcategory": "streaming_subscriptions",
  "frequency": "monthly",
  "next_due_date": "2025-11-01"
}
```

**Check Upcoming Bills:**
```json
{
  "days_ahead": 7
}
```

### 📤 Bulk Operations

**Add Multiple Expenses:**
```json
{
  "expenses": [
    {
      "date": "2025-10-25",
      "amount": 4.50,
      "category": "food",
      "subcategory": "coffee_tea",
      "note": "Morning coffee"
    },
    {
      "date": "2025-10-25",
      "amount": 12.99,
      "category": "food",
      "subcategory": "dining_out",
      "note": "Lunch"
    },
    {
      "date": "2025-10-25",
      "amount": 2.50,
      "category": "transport",
      "subcategory": "public_transport",
      "note": "Bus fare"
    }
  ]
}
```

**Export to CSV:**
```json
{
  "start_date": "2025-01-01",
  "end_date": "2025-12-31"
}
```

### 💬 Claude Desktop Commands

Once integrated with Claude Desktop, you can use natural language:

**Adding Expenses:**
- "Add a $25 expense for groceries today"
- "Record $4.50 for coffee this morning under food category"
- "I spent $89.99 on a new shirt yesterday, put it under shopping"

**Budget Management:**
- "Set a $500 monthly budget for food expenses"
- "How am I doing against my budget this month?"
- "Show me budget status for all categories"

**Analytics:**
- "What's my total spending this month?"
- "Show me my top 10 expenses from last month"
- "How much did I spend on food in 2025?"
- "What are my spending trends for transportation?"

**Recurring Expenses:**
- "Add Netflix subscription for $15.99 monthly due on the 1st"
- "What bills are due this week?"
- "Process my Netflix payment for this month"

**Search & Analysis:**
- "Find all coffee-related expenses from October"
- "Search for any Uber or taxi expenses"
- "Show me restaurant expenses over $50"

## 🔧 Integration

### 🤖 Claude AI Desktop Integration

#### Step-by-Step Setup

1. **Install Claude Desktop**
   - Download from [Claude.ai](https://claude.ai/download)
   - Complete the installation process

2. **Locate Configuration File**
   
   **Windows:**
   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```
   
   **macOS:**
   ```
   ~/Library/Application Support/Claude/claude_desktop_config.json
   ```
   
   **Linux:**
   ```
   ~/.config/Claude/claude_desktop_config.json
   ```

3. **Add MCP Server Configuration**
   
   Open the `claude_desktop_config.json` file and add:
   
   ```json
   {
     "mcpServers": {
       "expense-tracker": {
         "command": "fastmcp",
         "args": ["run", "main.py"],
         "cwd": "/path/to/your/Expence_tracker_MCP_server"
       }
     }
   }
   ```
   
   **For HTTP connection (using deployed server):**
   ```json
   {
     "mcpServers": {
       "expense-tracker-cloud": {
         "command": "curl",
         "args": ["-X", "POST", "https://prabhatmcp.fastmcp.app/mcp"]
       }
     }
   }
   ```

4. **Restart Claude Desktop**
   - Close Claude Desktop completely
   - Restart the application
   - The expense tracker should appear in the MCP servers list

#### Using with Claude Desktop

Once configured, you can:

**Add Expenses:**
```
Claude, add an expense for $15.99 for lunch at McDonald's today under Food & Dining category.
```

**View Monthly Summary:**
```
Claude, show me my expense summary for October 2025.
```

**Search Expenses:**
```
Claude, find all my coffee-related expenses from last month.
```

**Get Statistics:**
```
Claude, what are my spending statistics for this year?
```

### 🛠️ Alternative MCP Clients

#### Continue.dev Integration

1. **Install Continue Extension** in VS Code
2. **Configure in settings.json:**
   ```json
   {
     "continue.mcpServers": [
       {
         "name": "expense-tracker",
         "serverPath": "/path/to/fastmcp",
         "args": ["run", "main.py"],
         "cwd": "/path/to/Expence_tracker_MCP_server"
       }
     ]
   }
   ```

#### Custom MCP Client

For custom implementations:

```python
from mcp import Client
import asyncio

async def connect_to_expense_tracker():
    client = Client()
    await client.connect("https://prabhatmcp.fastmcp.app/mcp")
    
    # Add an expense
    result = await client.call_tool("add_expense", {
        "date": "2025-10-25",
        "amount": 25.99,
        "category": "Food & Dining",
        "note": "Dinner"
    })
    print(result)

asyncio.run(connect_to_expense_tracker())
```

### 🌐 HTTP API Integration

You can also integrate directly via HTTP:

```bash
curl -X POST https://prabhatmcp.fastmcp.app/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "add_expense",
    "parameters": {
      "date": "2025-10-25",
      "amount": 25.99,
      "category": "Food & Dining",
      "note": "Dinner"
    }
  }'
```

### 📱 Third-Party Integrations

#### Zapier Integration
Connect with Zapier to automatically track expenses from:
- 💳 Bank transactions
- 📧 Email receipts
- 📊 Spreadsheet updates

#### IFTTT Integration
Set up triggers for:
- 📱 Location-based expense tracking
- 📧 Receipt email processing
- 📅 Scheduled recurring expenses

### ✅ Verification Steps

After setup, verify integration:

1. **Test Connection:**
   - Ask Claude: "Check the health of the expense tracker"
   - Should receive server status

2. **Add Test Expense:**
   - "Add a $5 test expense for today"
   - Verify successful addition

3. **List Expenses:**
   - "Show me expenses from today"
   - Should see the test expense

### 🚨 Troubleshooting Integration

#### Common Claude Desktop Issues:

**Server Not Appearing:**
- Check JSON syntax in config file
- Verify file path is correct
- Restart Claude Desktop

**Connection Errors:**
- Ensure server is running
- Check network connectivity
- Verify URL accessibility

**Tool Not Working:**
- Test with health_check tool first
- Check parameter formats
- Review error messages

#### Debug Commands:

```bash
# Test local server
uv run python main.py

# Test with fastmcp
uv run fastmcp dev main.py

# Verify server health
curl https://prabhatmcp.fastmcp.app/mcp/health
```

## 📈 Data Analysis Capabilities

The expense tracker provides:

- **Statistical Analysis:** Automatic calculation of totals, averages, min/max values
- **Category Analysis:** Spending breakdown by category with counts and totals
- **Time-based Analysis:** Monthly and date range summaries
- **Search Capabilities:** Full-text search across all expense fields
- **Data Aggregation:** Automatic grouping and summarization

## 🔒 Security & Privacy

- 🔐 **Secure Cloud Hosting** - Data stored on FastMCP's secure infrastructure
- 🛡️ **Data Validation** - All inputs validated and sanitized
- 🚫 **No External Sharing** - Your expense data stays private
- 💾 **Reliable Storage** - Cloud SQLite with data persistence
- 🔄 **Error Recovery** - Robust error handling and recovery

## 📊 Response Formats

All tools return structured JSON responses:

### Success Response
```json
{
  "status": "success",
  "data": {...},
  "message": "Operation completed successfully"
}
```

### Error Response
```json
{
  "status": "error",
  "message": "Error description"
}
```

## 🆘 Troubleshooting

### Common Issues
1. **Connection Failed**: Verify the server URL is correct
2. **Invalid Date Format**: Use YYYY-MM-DD format
3. **Missing Required Fields**: Ensure date, amount, and category are provided
4. **Tool Not Found**: Check tool name spelling

### Getting Help
- Use `health_check` tool to verify server status
- Check tool documentation for required parameters
- Ensure JSON format is valid for tool calls

## 🚀 Current Version: 2.0

### ✅ Recently Added Features (v2.0)
- ✅ **Advanced Budget Management** - Set, track, and monitor spending budgets
- ✅ **Recurring Expense Tracking** - Manage subscriptions and recurring payments
- ✅ **Bulk Operations** - Add multiple expenses and export data
- ✅ **Enhanced Analytics** - Category trends, top expenses, comprehensive statistics
- ✅ **CRUD Operations** - Full create, read, update, delete functionality
- ✅ **Advanced Search** - Keyword search across all expense fields
- ✅ **CSV Export** - Export expense data for external analysis

### 🔮 Future Enhancements (v3.0 Roadmap)

Planned features for upcoming versions:
- 📊 **Interactive Dashboards** - Visual charts and graphs in Claude Desktop
- 🎯 **Smart Categorization** - AI-powered expense category suggestions
- 📧 **Receipt Processing** - Extract expense data from receipt images
- 🔔 **Advanced Notifications** - Custom alerts and spending warnings
- 📱 **Mobile App** - Dedicated mobile interface
- 🌍 **Multi-Currency Support** - Handle expenses in different currencies
- 👥 **Shared Budgets** - Family/team expense tracking
- 🤖 **Spending Insights** - AI-powered spending pattern analysis
- 📊 **Financial Goals** - Savings targets and progress tracking
- 🔗 **Bank Integration** - Connect to bank accounts for automatic tracking

## 📄 API Documentation

For detailed API documentation and interactive testing, visit:
**https://prabhatmcp.fastmcp.app/mcp**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Test with the live server
5. Submit a pull request

## 📞 Support

For support or questions:
- 🌐 **Live Server:** https://prabhatmcp.fastmcp.app/mcp
- 🔧 **Health Check:** Use the `health_check` tool
- 📝 **Documentation:** This README and inline tool descriptions

---

**Built with ❤️ using FastMCP | Deployed on FastMCP Cloud**

*Start tracking your expenses today at https://prabhatmcp.fastmcp.app/mcp*