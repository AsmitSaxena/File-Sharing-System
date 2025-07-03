# CRC Django Project

## 1. Writing Test Cases

To ensure the reliability and correctness of your Django application, you should write test cases for your views, forms, and models. Here’s how you can get started:

### a. Create a Test File
Create a `tests.py` file inside your app directory (e.g., `CRC/tests.py`).

### b. Example Test Cases
```python
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test@example.com', password='testpass')

    def test_login_view(self):
        response = self.client.post(reverse('login'), {
            'email': 'test@example.com',
            'password': 'testpass',
            'user_type': 'client',
        })
        self.assertEqual(response.status_code, 302)  # Should redirect on success

    def test_signup_view(self):
        response = self.client.post(reverse('signup'), {
            'name': 'Test User',
            'email': 'newuser@example.com',
            'phone': '1234567890',
            'password': 'newpass',
            'confirm_password': 'newpass',
            'user_type': 'client',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser@example.com').exists())

    def test_logout_view(self):
        self.client.login(username='test@example.com', password='testpass')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

# Add more tests for file upload, dashboard access, and download link generation as needed.
```

### c. Running Tests
Run your tests using:
```
python manage.py test
```

---

## 2. Deployment Plan

To deploy your Django project to a production environment, follow these steps:

### a. Prepare for Production
- Set `DEBUG = False` in `settings.py`.
- Set `ALLOWED_HOSTS` to your domain or server IP.
- Use a secure secret key (never share your development key).
- Configure static and media file handling (e.g., using AWS S3, or serving via Nginx).

### b. Choose a Hosting Platform
- **Popular options:**
  - [Heroku](https://www.heroku.com/)
  - [DigitalOcean](https://www.digitalocean.com/)
  - [AWS EC2](https://aws.amazon.com/ec2/)
  - [PythonAnywhere](https://www.pythonanywhere.com/)
  - [Vercel/Render](https://vercel.com/), [Render](https://render.com/)

### c. Install a Production-Ready Web Server
- Use **Gunicorn** as the WSGI HTTP server.
- Use **Nginx** as a reverse proxy and to serve static/media files.

### d. Database
- Use PostgreSQL or MySQL for production (not SQLite).
- Update `DATABASES` in `settings.py` accordingly.

### e. Steps Overview
1. **Clone your repository** to the server.
2. **Set up a virtual environment** and install dependencies:
   ```
   python -m venv venv
   venv\Scripts\activate  # On Windows
   pip install -r requirements.txt
   ```
3. **Collect static files:**
   ```
   python manage.py collectstatic
   ```
4. **Apply migrations:**
   ```
   python manage.py migrate
   ```
5. **Create a superuser:**
   ```
   python manage.py createsuperuser
   ```
6. **Run Gunicorn:**
   ```
   gunicorn CRC.wsgi:application --bind 0.0.0.0:8000
   ```
7. **Configure Nginx** to proxy requests to Gunicorn and serve static/media files.

### f. Security
- Use HTTPS (SSL/TLS) for all traffic.
- Set up proper permissions and firewalls.
- Regularly update dependencies and Django itself.

---

## 3. Default Accounts for Testing

The following user accounts are available for testing and demonstration purposes:

| Email                        | Password   | User Type     |
|------------------------------|------------|--------------|
| asmitsaxena707@gmail.com     | 987654321  | operational  |
| aishnagupta183@gmail.com     | 987654321  | client       |

You can use these credentials to log in as either an operational or client user when running the application locally or during testing.

---


