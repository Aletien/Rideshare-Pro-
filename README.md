# RideShare Pro - Django + Next.js

A modern, full-stack ride-sharing platform built with Django REST Framework backend and Next.js frontend with Tailwind CSS.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- npm or yarn

### Backend Setup (Django)

```bash
# Navigate to project root
cd /home/code/rideshare-pro

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install django djangorestframework django-cors-headers python-decouple psycopg2-binary pillow djangorestframework-simplejwt daphne channels

# Create database
createdb -h localhost rideshare_db

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver 0.0.0.0:8000
```

### Frontend Setup (Next.js)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env.local
cat > .env.local << 'ENVEOF'
NEXT_PUBLIC_API_URL=http://localhost:8000/api
ENVEOF

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 📁 Project Structure

```
rideshare-pro/
├── manage.py
├── rideshare_backend/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── users/                       # User management app
│   ├── models.py               # User, PassengerProfile, DriverProfile, Vehicle
│   ├── views.py                # Authentication and profile endpoints
│   ├── serializers.py          # DRF serializers
│   └── migrations/
├── rides/                       # Ride management app
│   ├── models.py               # Ride, RideLocation, Rating
│   ├── views.py                # Ride endpoints
│   ├── serializers.py
│   └── migrations/
├── payments/                    # Payment processing app
│   ├── models.py               # PaymentMethod, Transaction, Invoice
│   ├── views.py
│   ├── serializers.py
│   └── migrations/
├── drivers/                     # Driver-specific features
├── admin_panel/                 # Admin dashboard
├── frontend/                    # Next.js application
│   ├── app/
│   │   ├── page.tsx            # Home page
│   │   ├── login/page.tsx      # Login page
│   │   ├── register/page.tsx   # Registration page
│   │   ├── dashboard/page.tsx  # User dashboard
│   │   └── layout.tsx
│   ├── lib/
│   │   └── api.ts              # API client
│   ├── components/
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   └── tsconfig.json
└── venv/                        # Python virtual environment
```

## 🔌 API Endpoints

### Authentication
- `POST /api/users/register/` - Register new user
- `POST /api/users/login/` - Login user
- `GET /api/users/profile/` - Get current user profile

### Passengers
- `GET /api/passengers/` - Get passenger profile
- `POST /api/rides/request_ride/` - Request a ride
- `GET /api/rides/` - Get user's rides
- `POST /api/rides/{id}/cancel_ride/` - Cancel a ride

### Drivers
- `GET /api/drivers/` - Get driver profile
- `POST /api/drivers/go_online/` - Go online
- `POST /api/drivers/go_offline/` - Go offline
- `POST /api/rides/{id}/accept_ride/` - Accept a ride
- `POST /api/rides/{id}/start_ride/` - Start a ride
- `POST /api/rides/{id}/complete_ride/` - Complete a ride

### Rides
- `GET /api/rides/` - List rides
- `POST /api/locations/update_location/` - Update driver location
- `POST /api/ratings/rate_ride/` - Rate a ride

## 🗄️ Database Models

### Users App
- **User** - Custom user model with user_type field
- **PassengerProfile** - Passenger-specific data
- **DriverProfile** - Driver-specific data with status and earnings
- **Vehicle** - Vehicle information for drivers
- **AdminProfile** - Admin-specific data

### Rides App
- **Ride** - Ride information and status
- **RideLocation** - GPS tracking for rides
- **Rating** - User ratings and reviews

### Payments App
- **PaymentMethod** - Stored payment methods
- **Transaction** - Payment transactions
- **Invoice** - Ride invoices

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. User registers or logs in
2. Server returns `access_token` and `refresh_token`
3. Client stores tokens in localStorage
4. Client includes `Authorization: Bearer <token>` in requests
5. Tokens expire after 1 hour (access) or 7 days (refresh)

## 🎨 Frontend Features

- **Home Page** - Landing page with sign-up options
- **Authentication** - Login and registration forms
- **Dashboard** - User-specific dashboard based on user type
- **Responsive Design** - Mobile-friendly with Tailwind CSS
- **API Integration** - Axios-based API client

## 🛠️ Development

### Backend Development
```bash
# Run Django development server
python manage.py runserver

# Create new app
python manage.py startapp app_name

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Access admin panel
# Go to http://localhost:8000/admin
```

### Frontend Development
```bash
# Run Next.js development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linting
npm run lint
```

## 📦 Deployment

### Backend (Django)
```bash
# Collect static files
python manage.py collectstatic

# Use Gunicorn for production
gunicorn rideshare_backend.wsgi:application --bind 0.0.0.0:8000
```

### Frontend (Next.js)
```bash
# Build
npm run build

# Start
npm start
```

## 🔧 Configuration

### Environment Variables

Create `.env` file in project root:
```
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://user:password@localhost:5432/rideshare_db
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

Create `frontend/.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## 📚 Technologies Used

### Backend
- Django 5.2
- Django REST Framework
- PostgreSQL
- Daphne (ASGI server)
- Channels (WebSockets)
- JWT Authentication

### Frontend
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Axios

## 🚀 Features

### Current
- ✅ User authentication (Passenger, Driver, Admin)
- ✅ Ride request and acceptance
- ✅ Driver online/offline status
- ✅ Location tracking
- ✅ Rating system
- ✅ Payment methods
- ✅ Transaction history

### Planned
- 📋 Real-time notifications
- 📋 Chat between driver and passenger
- 📋 Advanced analytics
- 📋 Mobile app (React Native)
- 📋 Stripe payment integration
- 📋 Email notifications

## 📝 API Documentation

Full API documentation is available at:
- Swagger UI: `http://localhost:8000/api/schema/swagger/`
- ReDoc: `http://localhost:8000/api/schema/redoc/`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Allan Bakwanamaha
Email: etienallan@gmail.com

## 🆘 Support

For issues and questions, please open an issue on GitHub.
