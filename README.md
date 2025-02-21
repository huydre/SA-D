<div align="center">
  <h1>📚 Bookstore Management System</h1>
  <p>
    A modern bookstore management solution built with Django REST Framework and React
    <br />
    <a href="https://github.com/huydre/SA-D"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/huydre/SA-D">View Demo</a>
    ·
    <a href="https://github.com/huydre/SA-D/issues">Report Bug</a>
    ·
    <a href="https://github.com/huydre/SA-D/issues">Request Feature</a>
  </p>

  ![GitHub stars](https://img.shields.io/github/stars/huydre/SA-D)
  ![GitHub forks](https://img.shields.io/github/forks/huydre/SA-D)
  ![GitHub issues](https://img.shields.io/github/issues/huydre/SA-D)
  ![GitHub license](https://img.shields.io/github/license/huydre/SA-D)

</div>

---

### 📋 Table of Contents
- [About The Project](#about-the-project)
  - [Built With](#built-with)
  - [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgments](#acknowledgments)

---

### 🎯 About The Project

The Bookstore Management System is a comprehensive solution developed as part of the Software Architecture and Design course at PTIT, under the guidance of Professor Tran Dinh Que. This system implements a modern distributed database architecture to manage bookstore operations efficiently.

#### Built With

**Backend:**
* ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
* ![DRF](https://img.shields.io/badge/Django_REST_Framework-092E20?style=for-the-badge&logo=django&logoColor=white)
* ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

**Frontend:**
* ![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
* ![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)

**Database:**
* ![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)
* ![MySQL](https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white)
* ![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

#### Architecture

The system utilizes a distributed database architecture:
- **MongoDB**: Book management and inventory
- **MySQL**: Customer data and profiles
- **SQLite**: Supporting features (Cart, Orders, etc.)
- **PostgreeSQL**: 

---

### 🚀 Getting Started

#### Prerequisites

* Python 3.8+
* Node.js 16+
* Database Systems:
  ```text
  - MySQL 8.0+
  - MongoDB 6.0+
  - PostgreSQL
  - XAMPP (for MySQL management)
  ```

#### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/huydre/SA-D
   cd SA-D
   ```

2. **Backend Setup**
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # For Unix/macOS
   # or
   venv\Scripts\activate     # For Windows

   # Install dependencies
   pip install -r requirements.txt

   # Configure environment
   cp .env.example .env
   # Update .env with your configurations

   # Initialize database
   python manage.py makemigrations
   python manage.py migrate

   # Start server
   python manage.py runserver
   ```

3. **Frontend Setup**
   ```bash
   # Navigate to frontend directory
   cd frontend

   # Install dependencies
   npm install

   # Start development server
   npm run dev
   ```

---

### 💻 Usage

After installation, you can access:
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000/api`
- Admin Panel: `http://localhost:8000/admin`

---

### 📖 API Documentation

Detailed API documentation is available at `/api/docs` after starting the backend server. The API follows RESTful principles and includes endpoints for:

- User Authentication
- Book Management
- Order Processing
- Customer Management
- Cart Operations

---

### 🤝 Contributing

Contributions make the open-source community an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

### 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

---

### 📧 Contact

Bui Hai Nam - buihainam203@gmail.com

Project Link: [https://github.com/huydre/SA-D](https://github.com/huydre/SA-D)

---

### 🙏 Acknowledgments

* Professor Tran Dinh Que for project guidance
* PTIT Software Architecture and Design course
* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Pages](https://pages.github.com)
* [React Icons](https://react-icons.github.io/react-icons/search)

---

<div align="center">
  <p>Made with ❤️ by HNam</p>
</div>