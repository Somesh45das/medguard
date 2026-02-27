"""Test queue redirect"""
from app import create_app

app = create_app()
client = app.test_client()

# Login as admin
client.post('/auth/login', data={'email': 'admin@hospital.com', 'password': 'admin123'})

# Test queue page
r1 = client.get('/admin/queue', follow_redirects=False)
print(f'Status: {r1.status_code}')
print(f'Location: {r1.headers.get("Location", "No redirect")}')

# Try the actual route
r2 = client.get('/admin/queue/', follow_redirects=False)
print(f'\nWith trailing slash:')
print(f'Status: {r2.status_code}')
print(f'Length: {len(r2.data)} bytes')
