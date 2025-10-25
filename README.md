# 💰 Advanced Expense Tracker MCP Server

A comprehensive Model Context Protocol (MCP) server for tracking and analyzing personal expenses with advanced analytics and insights.

🌐 **Live Server:** https://prabhatmcp.fastmcp.app/mcp  
📁 **GitHub Repository:** https://github.com/Prabhat9801/Expence_tracker_MCP_server

## 🌟 Features

### Core Expense Management
- ✅ **Add Expense** - Record new expenses with date, amount, category, subcategory, and notes
- ✅ **List Expenses** - View expenses within date ranges
- ✅ **Delete Expense** - Remove expense entries
- ✅ **Search Expenses** - Find expenses by content across categories, subcategories, and notes
- ✅ **Get Expense Statistics** - Comprehensive statistics with min/max/average analysis
- ✅ **Monthly Summary** - Get detailed monthly expense breakdowns

### Analytics & Insights
- 📊 **Spending Statistics** - Total transactions, amounts, averages with category breakdowns
- 📈 **Monthly Analysis** - Detailed monthly spending analysis by category
- 🔍 **Search & Filter** - Advanced search across all expense fields
- 📊 **Category Summaries** - Spending summaries grouped by categories
- 📅 **Date Range Analysis** - Flexible date-based expense analysis

### Data Management
- 📋 **Category Management** - Predefined expense categories for consistency
- 🏥 **Health Monitoring** - Server health check and status monitoring
- 💾 **Cloud Storage** - Expenses stored securely in cloud database
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

### Core Operations

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

#### `delete_expense`
Remove an expense by ID.
```json
{
  "expense_id": 123
}
```

#### `search_expenses`
Search expenses by query across categories, subcategories, and notes.
```json
{
  "query": "coffee",
  "start_date": "2024-10-01",
  "end_date": "2024-10-31"
}
```

### Analytics Tools

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

#### `get_expense_statistics`
Comprehensive spending statistics and category breakdowns.
```json
{
  "start_date": "2024-01-01",
  "end_date": "2024-12-31"
}
```

### Utility Tools

#### `get_categories`
Get available expense categories.
```json
{}
```

#### `health_check`
Check server status and health.
```json
{}
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

### Adding Your First Expense
```json
{
  "date": "2024-10-25",
  "amount": 12.99,
  "category": "Food & Dining",
  "subcategory": "Lunch",
  "note": "Subway sandwich"
}
```

### Monthly Spending Analysis
```json
{
  "year": 2024,
  "month": 10
}
```

### Search for Coffee Expenses
```json
{
  "query": "coffee",
  "start_date": "2024-10-01",
  "end_date": "2024-10-31"
}
```

### Get Overall Statistics
```json
{
  "start_date": "2024-01-01",
  "end_date": "2024-12-31"
}
```

## 🔧 Integration

### MCP Client Setup
1. **Configure your MCP client** to connect to: `https://prabhatmcp.fastmcp.app/mcp`
2. **Test connection** using the `health_check` tool
3. **Start tracking** expenses with the `add_expense` tool

### Supported Clients
- Claude Desktop
- Continue.dev
- Custom MCP implementations
- Any MCP-compatible client

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

## 🚀 Future Enhancements

Planned features for upcoming versions:
- 📊 Advanced analytics and visualizations
- 💰 Budget tracking and alerts
- 📤 CSV import/export capabilities
- 🔄 Recurring expense detection
- 📱 Mobile-friendly interfaces
- 🎯 Spending goals and targets

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