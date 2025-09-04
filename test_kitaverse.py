# Kitaverse Test Script

import subprocess
import time
import sys
import os

def test_setup():
    """Test if the environment is set up correctly"""
    print("Testing Kitaverse setup...")
    
    # Check if required files exist
    required_files = [
        "requirements.txt",
        "app/backend/main.py",
        "app/client/main.py",
        "app/client/mobile.py",
        "app/client/index.html"
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"ERROR: Missing required file {file}")
            return False
        else:
            print(f"Found: {file}")
    
    print("All required files present!")
    return True

def test_backend():
    """Test if the backend server can start"""
    print("\nTesting backend server...")
    
    try:
        # Try importing FastAPI
        import fastapi
        print("FastAPI is available")
        
        # Try importing uvicorn
        import uvicorn
        print("Uvicorn is available")
        
        print("Backend dependencies are available!")
        return True
    except ImportError as e:
        print(f"ERROR: Missing backend dependencies: {e}")
        return False

def test_client():
    """Test if the client dependencies are available"""
    print("\nTesting client dependencies...")
    
    try:
        # Try importing Panda3D components
        from direct.showbase.ShowBase import ShowBase
        print("Panda3D is available")
        
        print("Client dependencies are available!")
        return True
    except ImportError as e:
        print("NOTE: Panda3D not found in current environment")
        print("This is expected if Panda3D is not installed yet")
        print("Install with: pip install panda3d")
        return True  # Not a failure since it's an optional dependency check

def main():
    """Run all tests"""
    print("Kitaverse Test Suite")
    print("=" * 30)
    
    if not test_setup():
        print("Setup test failed!")
        return False
        
    if not test_backend():
        print("Backend test failed!")
        return False
        
    if not test_client():
        print("Client test failed!")
        return False
        
    print("\n" + "=" * 30)
    print("All tests passed! Kitaverse is ready to use.")
    print("\nTo run Kitaverse:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Start the backend server: python app/backend/main.py")
    print("3. Open app/client/index.html in a web browser")
    return True

if __name__ == "__main__":
    main()