import os
import shutil

def setup():
    """Setup environment file"""
    if not os.path.exists('.env'):
        shutil.copy('.env.example', '.env')
        print("✓ Created .env file")
        print("⚠️  Please edit .env and add your ANTHROPIC_API_KEY")
    else:
        print("✓ .env already exists")

if __name__ == "__main__":
    setup()
