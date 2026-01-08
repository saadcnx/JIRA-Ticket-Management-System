-- JIRA Ticket Management System Database Schema

CREATE DATABASE IF NOT EXISTS jira_portal;
USE jira_portal;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tickets Table (Optional for future expansion)
CREATE TABLE IF NOT EXISTS tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    jira_ticket_key VARCHAR(50),
    title VARCHAR(255),
    description TEXT,
    issue_type VARCHAR(50),
    priority VARCHAR(50),
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Insert sample data
INSERT INTO users (username, email, password) VALUES
('admin', 'admin@jiraportal.com', 'admin123'),
('demo_user', 'demo@example.com', 'demo123');
