# Sky Food Corner - Cafe Website

A modern cafe website built with Django and Tailwind CSS featuring menu display, online ordering, reservations, and customer reviews.

## Features

- 📋 **Menu Management** - Display categorized menu items with images and prices
- 🛒 **Online Orders** - Add items to your order and checkout
- 🪑 **Table Reservations** - Online reservation system
- ⭐ **Customer Reviews** - Rating and review system
- 👤 **User Authentication** - Registration and login functionality
- 📱 **Responsive Design** - Mobile-friendly interface
- 🎨 **Modern UI** - Clean design with Tailwind CSS

## Tech Stack

- **Backend**: Django 5.0+
- **Frontend**: Tailwind CSS 3.4+
- **Database**: SQLite (default)
- **Image Processing**: Pillow

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+ (for Tailwind CSS)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cafe
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Node.js dependencies**
   ```bash
   npm install
   ```

5. **Build CSS**
   ```bash
   npm run build-css
   ```

6. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

8. **Start the development server**
   ```bash
   python manage.py runserver
   ```

9. **Visit the website**
   Open your browser and go to `http://127.0.0.1:8000`

## Development

### Watch CSS changes
```bash
npm run watch-css
```

### Admin Panel
Access the admin panel at `http://127.0.0.1:8000/admin/` to manage:
- Menu categories and items
- Orders
- Reservations
- Reviews
- Users

### Project Structure
```
cafe/
├── restaurant/              # Main app
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── urls.py             # URL routing
│   ├── templates/          # HTML templates
│   └── static/             # Static files
│       └── restaurant/
│           ├── css/        # Tailwind CSS
│           └── js/         # JavaScript
├── skyfoodcorner/          # Project settings
├── manage.py               # Django management
├── requirements.txt        # Python dependencies
└── package.json            # Node.js dependencies
```

## Customization

### Colors
Custom cafe colors are defined in `tailwind.config.js`:
- `cafe-brown`: #8B4513
- `cafe-light`: #D2B48C  
- `cafe-dark`: #5D2906

### Templates
Modify templates in `restaurant/templates/restaurant/` to customize the UI.

### CSS
Add custom styles in `restaurant/static/restaurant/css/input.css`.

## Deployment

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS`
3. Set up proper database (PostgreSQL recommended)
4. Configure static file serving
5. Set up environment variables for secrets

## License

This project is for educational purposes.

## Support

For issues or questions, please contact the development team.