# 🎓 College Management System - REST API

![Django REST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%2520web%2520tokens)

---

## 📌 Overview

**College Management System** is a comprehensive RESTful API built with Django REST Framework. It offers a full-featured backend system to manage academic institutions, with support for user roles, course structures, grading, attendance, and more.

---

## ✨ Features

- 🔐 Multi-role Authentication System (Admin, Professor, Student, Staff)  
- 🏛️ Academic Structure Management (Departments, Programs, Semesters)  
- 📚 Course Catalog & Offerings  
- 📝 Assignment & Exam Management  
- 🧮 Gradebook & Attendance Tracking  
- 👨‍🎓 Student Profiles & Enrollment  
- 👩‍🏫 Professor Dashboards  
- 📢 Announcements & Resource Sharing  
- 📖 Interactive API Documentation with Swagger & ReDoc  

---

## 🛠️ Technology Stack

- **Backend:** Django 5.2 + Django REST Framework  
- **Authentication:** JWT (JSON Web Tokens)  
- **Database:** PostgreSQL (or SQLite for development)  
- **Documentation:** Swagger / ReDoc  
- **Filtering:** Django Filter  
- **CORS:** django-cors-headers  

---

## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.9+  
- PostgreSQL (or SQLite for development)  
- `pip`  

---

### 📦 Installation

#### 1. Clone the repository

```bash
git clone https://github.com/AhmedHashim04/EduCore.git
cd EduCore
```

#### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure environment variables

Create a `.env` file in the root directory:

```ini
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/college_db
```

#### 5. Run migrations

```bash
python manage.py migrate
```

#### 6. Create a superuser

```bash
python manage.py createsuperuser
```

#### 7. Run development server

```bash
python manage.py runserver
```

---

## 📚 API Documentation

Interactive docs available at:

- **Swagger UI:** [http://localhost:8000/swagger/](http://localhost:8000/swagger/)  
- **ReDoc:** [http://localhost:8000/redoc/](http://localhost:8000/redoc/)  

---

## 🗂 Project Structure

```
college-management/
├── academics/           # Academic structure models
├── assessment/          # Assignments, exams, grading
├── courses/             # Courses and offerings
├── notifications/       # Announcements and resources
├── professor_dashboard/ # Professor-specific features
├── student_services/    # Student profiles, enrollment
├── users/               # Authentication and user management
├── college_management/  # Project settings
├── manage.py
└── requirements.txt
```

---

## 🔐 Authentication

This API uses JWT for authentication.

### 🔸 Obtain access & refresh tokens:

```bash
curl -X POST http://localhost:8000/api/auth/token/ \
-H "Content-Type: application/json" \
-d '{"username": "yourusername", "password": "yourpassword"}'
```

### 🔸 Use token in requests:

```bash
curl http://localhost:8000/api/courses/ \
-H "Authorization: Bearer your.access.token.here"
```

---

## 🌟 Example API Requests

### 🔹 Get all courses

```http
GET /api/courses/
```

### 🔹 Create a new assignment

```http
POST /api/assessment/assignments/
Content-Type: application/json

{
  "course_offering": 1,
  "title": "Final Project",
  "description": "Create a comprehensive project",
  "due_date": "2023-12-15T23:59:00Z",
  "total_points": 100,
  "submission_type": "both"
}
```

### 🔹 Get student profile

```http
GET /api/student-services/profiles/1/
```

---

## 🧪 Testing

To run all tests:

```bash
python manage.py test
```

---

## 🧰 Custom Management Commands

Create realistic sample data:

```bash
python manage.py create_sample_data
```

---

## 🏗️ Deployment Tips

For production environments:

- Use **PostgreSQL**
- Set `DEBUG=False`
- Configure **CORS** & **CSRF** properly
- Use **Gunicorn** behind **Nginx**
- Handle static files properly (e.g., with `collectstatic`)

### 🔧 Example production settings:

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
CORS_ALLOWED_ORIGINS = ['https://yourfrontend.com']
CSRF_TRUSTED_ORIGINS = ['https://yourdomain.com']
```

---

## 🤝 Contributing

1. Fork the project  
2. Create your feature branch: `git checkout -b feature/AmazingFeature`  
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`  
4. Push to the branch: `git push origin feature/AmazingFeature`  
5. Open a Pull Request  

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ✉️ Contact

**Project Maintainer** – Ahmed Hashim  
<div align="center">
  <img src="https://contrib.rocks/image?repo=AhmedHashim04/college-management-api" />
  <br/>
  <sub>Made with ❤️ by [contrib.rocks](https://contrib.rocks)</sub>
</div>