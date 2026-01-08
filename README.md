
## 📋 Table of Contents
- [✨ Features](#-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [🚀 Quick Start](#-quick-start)
- [📁 Project Structure](#-project-structure)
- [🔧 Installation](#-installation)
- [🎮 Usage](#-usage)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [👨‍💻 Author](#-author)

## ✨ Features

### 🔐 **Authentication & Security**
- User Registration & Login System
- Session Management with Flask-Session
- Password Hashing & Validation
- Protected Routes & Middleware

### 🎫 **JIRA Integration**
- Direct JIRA Cloud API Integration
- Create Tickets with Custom Fields
- Multiple Issue Types Support
- Real-time Ticket Creation
- Priority Level Management

### 💻 **User Interface**
- Modern & Responsive Design
- Intuitive Dashboard
- Real-time Form Validation
- Flash Messages & Notifications
- Mobile-Friendly Layout

### 🗄️ **Database Management**
- MySQL Integration with Flask-MySQLdb
- User Management System
- Secure Data Storage
- Efficient Query Handling

### ⚡ **Performance**
- Fast API Response Times
- Optimized Database Queries
- Efficient Session Handling
- Scalable Architecture

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | HTML5, CSS3, JavaScript |
| **Backend** | Flask, Python 3.8+ |
| **Database** | MySQL 8.0 |
| **Authentication** | Flask Session |
| **API Integration** | Atlassian JIRA REST API |
| **Styling** | Custom CSS, Font Awesome, Google Fonts |
| **Deployment** | Gunicorn, Nginx (Production Ready) |

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL 5.7+
- JIRA Account with API Access

### One-Line Installation

git clone https://github.com/saadcnx/JIRA-Ticket-Management-System


🔧 Installation
Step 1: Clone Repository
git clone https://github.com/saadcnx/JIRA-Ticket-Management-System
cd jira-ticket-system

Step 2: Setup Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Step 3: Install Dependencies
pip install -r requirements.txt

Step 4: Configure Environment
cp .env.example .env
# Edit .env with your credentials

Step 5: Setup Database
mysql -u root -p < database_schema.sql

Step 6: Run Application
python app.py

Step 7: Access Application
Open http://localhost:5000 in your browser

🎮 Usage
1. User Registration
Navigate to /create_account_page
Fill in username, email, and password
Click "Create Account"
Auto-login to dashboard

2. Login System
Go to /login_page
Enter credentials
Access protected dashboard

3. Create JIRA Ticket
Click "Create Ticket" from dashboard
Fill ticket details:
Reporter Name
Issue Type (Bug/Task/Story)
Priority Level
Summary & Description
Submit to create ticket in JIRA

4. Logout
Click logout button to securely end session

# Create JIRA Ticket
POST /jira_create

Parameters:
- reporter: String (required)
- issueType: String (Bug/Task/Story)
- summary: String (required)
- description: String (required)
- priority: String (Low/Medium/High)

Response:
{
    "success": true,
    "ticket_key": "SCRUM-123",
    "url": "https://jira-url/browse/SCRUM-123"
}

User Authentication API

# User Login
POST /login

# User Registration  
POST /create_account

# User Logout
GET /logout
🔧 Environment Variables
Variable	Description	Example
SECRET_KEY	Flask secret key	your-secret-key
MYSQL_HOST	MySQL host	localhost
MYSQL_USER	MySQL username	root
MYSQL_PASSWORD	MySQL password	password
MYSQL_DB	Database name	jira_portal
JIRA_URL	JIRA instance URL	https://your.atlassian.net
JIRA_USER	JIRA email	user@domain.com
JIRA_API_TOKEN	JIRA API token	your-api-token

🤝 Contributing
Fork the repository
Create a feature branch (git checkout -b feature/AmazingFeature)
Commit changes (git commit -m 'Add AmazingFeature')
Push to branch (git push origin feature/AmazingFeature)

Open a Pull Request

🐛 Bug Reports
Please use GitHub Issues to report bugs.

👨‍💻 Author
Saad Khan - Devops Engineer
GitHub: @saadcnx
LinkedIn: Saad Khan
Email: saadcnx@gmail.com

🙏 Acknowledgments
Flask Documentation Team
Atlassian for JIRA API
Font Awesome for icons
Google Fonts for typography

