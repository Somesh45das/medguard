"""Test the missing pages"""
from app import create_app

app = create_app()
client = app.test_client()

# Login as admin
client.post('/auth/login', data={'email': 'admin@hospital.com', 'password': 'admin123'})

# Test queue page
r1 = client.get('/admin/queue')
print(f'Queue page: {r1.status_code} ({len(r1.data)} bytes)')
if r1.status_code == 200 and len(r1.data) > 1000:
    print('  ✅ Queue page WORKS!')
else:
    print('  ❌ Queue page FAILED')

# Test manage doctors
r2 = client.get('/admin/manage/doctors')
print(f'Manage doctors: {r2.status_code} ({len(r2.data)} bytes)')
if r2.status_code == 200 and len(r2.data) > 1000:
    print('  ✅ Manage doctors WORKS!')
else:
    print('  ❌ Manage doctors FAILED')
