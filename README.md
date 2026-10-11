# expense-tracker
# Expense Tracker

A multi-user expense tracking web app built with Django. Users register, log in, and manage their own expenses, then review monthly summaries and get budget alerts.

## Features

- User registration, login, and logout
- Private data per user (each user sees only their own expenses)
- Add, edit, and delete expenses (full CRUD)
- Custom categories for each user
- Filter by category and date range, and search notes
- Monthly summary with a category-wise doughnut chart (Chart.js)
- Monthly budget with a progress bar and warnings at 80% and over the limit
- Responsive design with Bootstrap

## Tech Stack

- **Backend:** Python, Django
- **Database:** SQLite (development)
- **Frontend:** HTML, Bootstrap 5, Chart.js


## Run Locally

```
git clone https://github.com/kabitapradhan12/expense-tracker.git
cd expense-tracker
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open http://127.0.0.1:8000/

On Mac or Linux, activate the environment with `source venv/bin/activate`.

## Project Structure

- `config/`: project settings and main URLs
- `expenses/`: models, views, forms, and app URLs
- `templates/`: HTML templates (a shared `base.html` plus page templates)

## Security Notes

- Every query is filtered by the logged-in user, so users cannot view or change each other's data.
- Edit and delete views return a 404 for expenses that belong to another user.
- Forms use CSRF protection, and logout and delete use POST requests.

## Planned Improvements

- REST API with token authentication
- Automated tests
- Deployment with PostgreSQL

## Author

Kabita Pradhan | [GitHub](https://github.com/kabitapradhan12)