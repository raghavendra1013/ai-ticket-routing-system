AI-Powered Support Ticket Routing System.
1. Overview

This project is a full-stack AI-powered customer support ticket management system. It automates ticket classification, priority prediction, agent assignment, and analytics.

The system is designed to address real-world problems such as:

Manual ticket sorting
Uneven agent workload
Lack of real-time monitoring

It integrates Machine Learning with backend APIs and frontend dashboards to create a complete intelligent support system.


2. Features

2.1 AI-Based Ticket Classification
Uses TF-IDF with Logistic Regression
Predicts:
Ticket category
Ticket priority
Provides confidence score for predictions

2.2 Intelligent Agent Assignment
Category-based routing
Load balancing using least active tickets
High-priority tickets assigned to expert agents

2.3 Queue Management System
Priority-based ordering:
High → Medium → Low
FIFO within the same priority level
Agent capacity limit (maximum 3 active tickets)

2.4 OTP-Based Authentication
Email-based OTP verification using SMTP
Secure login flow

2.5 Role-Based Access Control
Admin
View all tickets
Update ticket status
Monitor analytics dashboard
Manage agent queues
Customer
Raise support tickets
Track personal tickets
View personal dashboard

2.6 Analytics Dashboard
Admin Dashboard
Total tickets
Open and resolved tickets
Category distribution
Priority distribution
Agent workload
Agent performance
Average resolution time
Customer Dashboard
Personal ticket statistics
Category insights
Status tracking

2.7 Ticket History Tracking
Logs all ticket status changes with timestamps


3. System Architecture

Frontend (HTML, CSS, JavaScript)
↓
Flask Backend (API Layer)
↓
Business Logic (Routing and ML)
↓
SQLite Database
↓
Machine Learning Models


4. Tech Stack
4.1 Backend
Python
Flask
Flask-CORS
SQLite

4.2 Machine Learning
Scikit-learn
Pandas
Joblib

4.3 Frontend
HTML5
CSS3
JavaScript
Chart.js


5. Machine Learning Pipeline

5.1 Dataset
File: ticket_dataset.csv
Contains text, category, and priority labels

5.2 Model
TF-IDF Vectorizer
Logistic Regression classifier

5.3 Outputs
Category prediction
Priority prediction

5.4 Evaluation
Train-test split (80/20)
Accuracy calculated on test data

5.5 Model Files

models/

classifier.pkl
priority_model.pkl


6. Project Structure

project/
│
├── backend/
│ ├── app.py
│ ├── database.py
│ ├── model.py
│ ├── router.py
│ ├── train_model.py
│
├── models/
│ ├── classifier.pkl
│ ├── priority_model.pkl
│
├── database/
│ └── tickets.db
│
├── frontend/
│ ├── index.html
│ ├── login.html
│ ├── tickets.html
│ ├── my_tickets.html
│ ├── dashboard.html
│ ├── customer_dashboard.html
│ ├── style.css
│ ├── script.js
│
└── ticket_dataset.csv


7. Installation and Setup

7.1 Clone Repository

git clone https://github.com/raghavendra1013/ai-ticket-routing-system

cd ai-ticket-routing-system

7.2 Install Dependencies

pip install flask flask-cors scikit-learn pandas joblib

7.3 Train Machine Learning Model

cd backend
python train_model.py

7.4 Run Backend Server

python app.py

Server will run at:
http://127.0.0.1:5000

7.5 Open Frontend

Open the following file in your browser:
frontend/login.html


8. Default Credentials

Admin Login:
Username: admin
Password: admin123

9. Usage Guide
9.1 Customer Flow
Sign up or log in using OTP verification
Submit a ticket
System predicts category and priority
Ticket is assigned to an agent
Track ticket status in dashboard

9.2 Admin Flow
Log in as admin
View all tickets
Update ticket status
Monitor analytics dashboard
Manage and process queues


10. API Documentation

10.1 Authentication

POST /signup → Register user
POST /login → Login
POST /send_otp → Send OTP
POST /verify_otp → Verify OTP

10.2 Tickets

POST /submit_ticket → Create ticket
GET /tickets → Get all tickets
POST /my_tickets → Get user tickets
POST /update_status → Update ticket status

10.3 Dashboard

GET /ticket_stats → Admin statistics
POST /customer_stats → Customer statistics

10.4 Queue

GET /full_queue_status → View all queues
POST /process_next/<agent> → Process next ticket


11. Database Schema
11.1 Users Table

id | username | email | password | role

11.2 Tickets Table

id | name | email | subject | description
category | priority | status
agent_assigned
created_at | resolved_at

11.3 Ticket History Table

id | ticket_id | status | timestamp


12. Important Notes

Update email credentials in app.py for OTP functionality
Train models before starting backend
SQLite database is created automatically
Ensure correct file paths for model files


13. Future Improvements
JWT-based authentication
Deployment (AWS, Render, etc.)
Real-time updates using WebSockets
Advanced NLP models (BERT)
File attachment support
Multi-admin role management


14. Author

This project was developed as a full-stack AI system combining machine learning, backend development, frontend design, and database management.
