# 📝 Job Application Tracker (Django Project)

Job Tracker
A Django-based application that helps track job applications, including the status, position, and related details. This project is built with Python and Django and uses SQLite as the database backend. And this project helps to get automated email reminders for upcoming deadlines like exams, interviews, or application submissions. This project also includes integration with the Windows Task Scheduler to automate email reminders daily at 9 AM.

## 🚀 Features
- User Authentication (Login/Register)
- Add/Edit/Delete job applications
- Track statuses like:
  - Not Applied
  - Applied
  - Interview Scheduled
  - Exam Scheduled
  - Rejected
  - Selected
- Filter jobs:
  - Overdue
  - Due Today
  - Due in the next 3 days (Urgent)
- Email reminders for upcoming jobs based on status
- Automated email reminders daily using Windows Task Scheduler
- Clean UI using Django Templates

## 💻Technologies Used
Python: Programming language.
Django: A high-level Python web framework for building web applications.
SQLite: The default database for Django projects.
HTML/CSS: For basic structure and styling.
Bootstrap: For responsive design.
Email Notification: Bravo SMTP Service, Windows Task Schedular.

## ⚙️Setup Instructions
Follow these steps to set up the project locally:

## 📋Prerequisites
-Python (version 3.x)
-Django (installed using pip)

## Steps
1.Clone the repository:
git clone https://github.com/yourusername/job_tracker.git
cd job_tracker

2.Create a virtual environment (if not already done):
python -m venv env

3.Activate the virtual environment:
.\env\Scripts\activate

4.Apply migrations to set up the database:
python manage.py migrate

5.Run the development server:
python manage.py runserver
Visit http://127.0.0.1:8000/ in your browser.

6.To send reminders:
python manage.py send_reminders
7.Set up Task Scheduler on Windows to automate the above command daily.

## ✉️ Email Notifications
-Configured using Django's built-in SMTP backend.

-Bravo SMTP is used as the mail service provider.

-Email reminders are automatically sent to registered users about their upcoming or urgent job deadlines.

-Windows Task Scheduler is configured to trigger the custom Django management command (send_reminders) daily at 9:00 AM to ensure users receive timely email updates.


