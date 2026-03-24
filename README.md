AI POWERED SUPPORT TICKET ROUTING SYSTEM

An intelligent end-to-end customer support platform that automates ticket classification, prioritization, and agent assignment using Machine Learning and a queue-based routing system.

This project simulates a real-world support infrastructure used in SaaS and enterprise systems, combining AI, backend APIs, and frontend dashboards.

SYSTEM ARCHITECTURE

High-Level Architecture (Text Diagram)

Frontend (HTML, CSS, JavaScript)
|
| HTTP Requests (REST API)
v
Flask Backend (app.py)
|
|------------------------------|
| | |
v v v
ML Engine Routing Engine Authentication System
(model.py) (router.py) (OTP + Login)
| | |
|--------------|---------------|
v
SQLite Database
(tickets.db)
|
v
Email Service (SMTP)

ARCHITECTURE EXPLANATION

Frontend Layer

Built using HTML, CSS, and JavaScript
Handles user interaction
Sends API requests to backend
Pages include ticket submission, dashboards, login system

Backend Layer (Flask)

Core controller of the application
Handles API endpoints, business logic, and database operations
Integrates ML predictions and routing decisions
Returns JSON responses

Machine Learning Engine

Uses TF-IDF vectorization + Logistic Regression
Predicts:
Category of ticket
Priority of ticket
Includes confidence scoring
Low confidence fallback sets priority to medium

Routing Engine

Assigns agents based on ticket category
Uses load balancing (least active tickets)
High priority tickets assigned to top agents
Maintains queue per agent

Queue System

Priority-based ordering (High > Medium > Low)
FIFO within same priority
Agent capacity limit (max 3 active tickets)
Supports "process next ticket" functionality

Database Layer (SQLite)
Tables:

tickets
Stores ticket data, status, timestamps, agent assignment
users
Stores login credentials and roles
ticket_history
Tracks status changes over time

Authentication System

OTP-based login via email
Role-based access:
Admin
Customer

Analytics System

Real-time queries from database
Displayed using charts
Admin dashboard and customer dashboard

END TO END FLOW

User submits ticket
-> Frontend sends request to backend
-> Backend calls ML model
-> Category and priority predicted
-> Routing engine assigns agent
-> Ticket stored in database
-> Ticket enters agent queue
-> Admin manages tickets
-> Customer tracks status

CORE FEATURES

AI Ticket Classification

Automatic category detection
Priority prediction with confidence score

Smart Agent Assignment

Category-based mapping
Load balancing
High-priority escalation

Queue Management

Priority queues
Agent capacity control
Sequential processing

OTP Authentication

Email-based verification
Secure login system

Customer Features

Raise tickets
View personal tickets
Track ticket status
View analytics dashboard

Admin Features

View all tickets
Update ticket status
Monitor analytics
Track agent performance
View queue status

Interactive Dashboards

Built using Chart.js
Includes:
Category distribution
Priority analysis
Agent workload
Resolution metrics

TECH STACK

Backend

Flask
SQLite

Frontend

HTML5
CSS3
JavaScript

Machine Learning

Scikit-learn
TF-IDF Vectorizer
Logistic Regression

Other Tools

Joblib (model saving)
SMTP (email OTP system)

PROJECT STRUCTURE

backend

app.py (main server)
database.py (database setup)
model.py (ML prediction)
router.py (agent routing + queues)
train_model.py (model training)

frontend

index.html (raise ticket)
login.html (login/signup)
dashboard.html (admin dashboard)
customer_dashboard.html
tickets.html (manage tickets)
my_tickets.html
script.js (logic)
style.css (design)

data

ticket_dataset.csv

models

classifier.pkl
priority_model.pkl

database

tickets.db

API ENDPOINTS

Authentication

POST /send_otp
POST /verify_otp
POST /login
POST /signup

Tickets

POST /submit_ticket
GET /tickets
POST /my_tickets
POST /update_status

Analytics

GET /ticket_stats
POST /customer_stats

Queue System

GET /full_queue_status
POST /process_next/<agent>

MACHINE LEARNING PIPELINE

Input: Ticket description

Step 1: Text vectorization using TF-IDF
Step 2: Classification using Logistic Regression

Outputs:

Category prediction
Priority prediction
Confidence score

SETUP INSTRUCTIONS

Install dependencies
pip install flask flask-cors scikit-learn pandas joblib
Train models
python train_model.py
Run backend
python app.py
Open frontend
Open login.html in browser

DEFAULT ADMIN LOGIN

Username: admin
Password: admin123

SYSTEM HIGHLIGHTS

Fully automated ticket routing
AI-driven prioritization
Queue-based workload management
Real-time dashboards
Clean modular architecture
Scalable design

FUTURE IMPROVEMENTS

JWT authentication
Cloud deployment (AWS, Docker)
Real-time updates (WebSockets)
Advanced NLP models (BERT)
SLA tracking system
Multi-language support



Full-stack AI project combining machine learning, backend systems, and frontend dashboards to simulate a real-world support platform.