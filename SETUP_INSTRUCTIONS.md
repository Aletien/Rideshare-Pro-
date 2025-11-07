# RideShare Pro - Complete Setup Instructions

## System Requirements

- Python 3.8 or higher
- Node.js 16 or higher
- PostgreSQL 12 or higher
- npm or yarn package manager
- Git

## Step 1: Backend Setup (Django)

### 1.1 Navigate to Project Directory
```bash
cd /home/code/rideshare-pro
```

### 1.2 Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 1.3 Install Python Dependencies
```bash
pip install --upgrade pip
pip install django==5.2.8
pip install djangorestframework
pip install django-cors-headers
pip install python-decouple
pip install psycopg2-binary
pip install pillow
pip install djangorestframework-simplejwt
pip install daphne
pip install channels
```

### 1.4 Create PostgreSQL Database
```bash
createdb -h localhost rideshare_db
```

If you need to specify a user:
```bash
createdb -h localhost -U postgres rideshare_db
```

### 1.5 Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 1.6 Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
# Follow the prompts to create admin account
```

### 1.7 Start Django Development Server
```bash
python manage.py runserver 0.0.0.0:8000
```

The Django API will be available at: `http://localhost:8000/api`
Admin panel: `http://localhost:8000/admin`

## Step 2: Frontend Setup (Next.js)

### 2.1 Navigate to Frontend Directory
```bash
cd frontend
```

### 2.2 Install Node Dependencies
```bash
npm install
```

### 2.3 Create Environment File
```bash
cat > .env.local << 'EOF'
NEXT_PUBLIC_API_URL=http://localhost:8000/api
