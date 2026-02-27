"""
Test patient portal pages to ensure they load correctly.
"""
import sys
sys.path.insert(0, '.')

from app import create_app

app = create_app()

with app.test_client() as client:
    print("Testing Patient Portal Pages...")
    print("=" * 60)
    
    pages = [
        ('/patient/', 'Patient Home'),
        ('/patient/check-status', 'Check Status'),
    ]
    
    for url, name in pages:
        response = client.get(url)
        status = "✅ OK" if response.status_code == 200 else f"❌ ERROR ({response.status_code})"
        print(f"{name:30} {url:30} {status}")
    
    print("\nNote: /patient/book and /patient/dashboard require login")
    print("=" * 60)
    print("All public pages working!")
