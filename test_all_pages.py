"""
Test all pages to see which ones work
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app

def test_pages():
    """Test all pages."""
    app = create_app()
    
    with app.test_client() as client:
        print("\n" + "="*60)
        print("🧪 TESTING ALL PAGES")
        print("="*60 + "\n")
        
        pages = [
            ('/', 'Landing Page'),
            ('/auth/login', 'Login Page'),
            ('/auth/simple-login', 'Simple Login Page'),
            ('/auth/register', 'Register Page'),
            ('/patient/', 'Patient Home'),
            ('/patient/dashboard', 'Patient Dashboard (requires login)'),
            ('/patient/book', 'Book Appointment (requires login)'),
            ('/admin/', 'Admin Dashboard (requires login)'),
        ]
        
        for url, name in pages:
            try:
                response = client.get(url, follow_redirects=False)
                status = response.status_code
                
                if status == 200:
                    print(f"✅ {name:40} {url:30} → {status} OK")
                elif status == 302:
                    location = response.headers.get('Location', 'unknown')
                    print(f"🔄 {name:40} {url:30} → {status} Redirect to {location}")
                elif status == 404:
                    print(f"❌ {name:40} {url:30} → {status} NOT FOUND")
                elif status == 500:
                    print(f"💥 {name:40} {url:30} → {status} SERVER ERROR")
                else:
                    print(f"⚠️  {name:40} {url:30} → {status}")
            except Exception as e:
                print(f"💥 {name:40} {url:30} → ERROR: {str(e)[:50]}")
        
        print("\n" + "="*60)
        print("✅ TESTING COMPLETE")
        print("="*60 + "\n")
        
        print("📝 Notes:")
        print("  • 200 = Page loads successfully")
        print("  • 302 = Redirect (normal for protected pages)")
        print("  • 404 = Page not found")
        print("  • 500 = Server error (template or code issue)")
        print()


if __name__ == "__main__":
    test_pages()
