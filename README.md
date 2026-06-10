# SmartHR Dashboard 🏢

A full-stack HR Analytics Dashboard built with Python and FastAPI.
Inspired by real-world HRMIS experience to solve common HR data challenges.

## Features
- Employee management with department tracking
- Leave request system with approval workflow  
- HR analytics: headcount by department, leave patterns
- Auto-seeded with realistic mock HR data
- Interactive API documentation

## Tech Stack
- **Backend:** Python, FastAPI, SQLAlchemy
- **Database:** SQLite
- **Data:** Pandas, Faker
- **API Docs:** Swagger UI (auto-generated)

## Getting Started

```bash
# Clone the repo
git clone https://github.com/jaweednoori/smarthr-dashboard.git
cd smarthr-dashboard

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for the interactive API documentation.

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/employees` | List all employees |
| GET | `/employees/{id}` | Get single employee |
| GET | `/departments` | List all departments |
| GET | `/analytics/headcount` | Headcount by department |
| GET | `/analytics/leave-summary` | Leave request summary |
| GET | `/leave-requests` | All leave requests |

## About
Built as part of a portfolio project bridging HRMIS domain expertise
with modern Python web development.
