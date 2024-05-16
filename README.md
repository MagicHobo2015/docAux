# DocAux Backend

## Prerequisites

- **Python**: Ensure you have Python 3.11 or higher installed.
- **MySQL**: Install MySQL and create a new database.

## Setup Instructions

### 1. Configure Environment Variables

1. Create a new `.env` file.
2. Copy the contents of `.env.example` into `.env`.
3. Populate the variables with the appropriate values.

### 2. Set Up Virtual Environment

1. conda create --name myenv python=3.11.5|
2. conda activate myenv

### 3. Install Dependencies

1. pip install -r ai/pip_requirements.install_me
2. pip install -r backend/requirements.txt

### 4. Install MySql

1. https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/
2. create new database
3. CREATE DATABASE docAux;

### 5. Run backend

1. To run the backend:
2. cd backend
3. python run.py
