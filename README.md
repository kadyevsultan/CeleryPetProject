# PetMailing - Reminder System

PetMailing is a reminder application built with Django, Celery, and Redis. 
It allows users to create and manage reminders that are sent to their email. 
The project includes features like user authentication, reminder creation, and email notifications. 
It also provides the ability to view upcoming and completed reminders.

## Features
- User authentication (Login/Signup)
- User authentication with Google account
- Create, view, and delete reminders
- Email notifications for upcoming reminders
- Completed reminder tracking
- Celery for background task processing (email sending)
- Redis as a message broker

## Requirements
- Docker
- Docker Compose
- Python 3.8+
- PostgreSQL (configured in the project)
- Redis (configured in the project)
- Gunicorn for production server
- ...

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/petmailing.git
   cd web
   create .env or send message on me for taking my working .env
   docker compose up --build
