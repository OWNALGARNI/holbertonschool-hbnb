"""
Check users in database
"""
from app import create_app
from app.extensions import db
from app.models.user import User

def check_users():
    app = create_app()
    
    with app.app_context():
        users = User.query.all()
        
        print("=" * 60)
        print(f"Total users in database: {len(users)}")
        print("=" * 60)
        
        for user in users:
            print(f"\nUser ID: {user.id}")
            print(f"Email: {user.email}")
            print(f"First Name: {user.first_name}")
            print(f"Last Name: {user.last_name}")
            print(f"Is Admin: {user.is_admin}")
            print(f"Password Hash (first 20 chars): {user.password[:20]}...")
            
            # Test password verification
            test_passwords = ["admin123", "user123"]
            for pwd in test_passwords:
                result = user.verify_password(pwd)
                print(f"  Password '{pwd}' verified: {result}")
        
        print("\n" + "=" * 60)
        
        # Try to verify admin password specifically
        admin = User.query.filter_by(email="admin@test.com").first()
        if admin:
            print("\n🔍 Testing admin@test.com password:")
            print(f"   Password 'admin123': {admin.verify_password('admin123')}")

if __name__ == '__main__':
    check_users()
