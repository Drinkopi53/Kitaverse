# Kitaverse Packaging Script

import os
import shutil
import zipfile
import datetime

def create_distribution():
    \"\"\"Create a distribution package for Kitaverse\"\"\"
    print(\"Creating Kitaverse distribution package...\")
    
    # Create distribution directory
    dist_dir = \"dist\"
    if not os.path.exists(dist_dir):
        os.makedirs(dist_dir)
    
    # Create package name with timestamp
    timestamp = datetime.datetime.now().strftime(\"%Y%m%d_%H%M%S\")
    package_name = f\"kitaverse_{timestamp}\"
    package_dir = os.path.join(dist_dir, package_name)
    
    # Create package directory structure
    os.makedirs(package_dir)
    os.makedirs(os.path.join(package_dir, \"app\"))
    os.makedirs(os.path.join(package_dir, \"app\", \"backend\"))
    os.makedirs(os.path.join(package_dir, \"app\", \"client\"))
    
    # Copy essential files
    files_to_copy = [
        \"README.md\",
        \"requirements.txt\",
        \"Dockerfile\",
        \"start_server.bat\",
        \"test_kitaverse.py\"
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, package_dir)
    
    # Copy backend files
    backend_files = [
        \"app/backend/main.py\",
        \"app/backend/README.md\"
    ]
    
    for file in backend_files:
        if os.path.exists(file):
            target_path = os.path.join(package_dir, file)
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            shutil.copy2(file, target_path)
    
    # Copy client files
    client_files = [
        \"app/client/main.py\",
        \"app/client/mobile.py\",
        \"app/client/index.html\",
        \"app/client/README.md\",
        \"app/client/config.json\",
        \"app/client/config_optimized.prc\",
        \"app/client/spaces.json\"
    ]
    
    for file in client_files:
        if os.path.exists(file):
            target_path = os.path.join(package_dir, file)
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            shutil.copy2(file, target_path)
    
    # Create a simple installation script
    install_script = \"\"\"#!/bin/bash
# Kitaverse Installation Script

echo \"Installing Kitaverse dependencies...\"
pip install -r requirements.txt

echo \"Kitaverse installation complete!\"
echo \"To run Kitaverse:\"
echo \"1. Start the backend server: python app/backend/main.py\"
echo \"2. Open app/client/index.html in a web browser\"
\"\"\"
    
    with open(os.path.join(package_dir, \"install.sh\"), \"w\") as f:
        f.write(install_script)
    
    # Create a Windows installation batch file
    install_batch = \"\"\"@echo off
echo Installing Kitaverse dependencies...
pip install -r requirements.txt

echo Kitaverse installation complete!
echo To run Kitaverse:
echo 1. Start the backend server: python app/backend/main.py
echo 2. Open app/client/index.html in a web browser
pause
\"\"\"
    
    with open(os.path.join(package_dir, \"install.bat\"), \"w\") as f:
        f.write(install_batch)
    
    # Create ZIP archive
    zip_filename = f\"{package_name}.zip\"
    zip_path = os.path.join(dist_dir, zip_filename)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, package_dir)
                zipf.write(file_path, os.path.join(package_name, arc_path))
    
    # Clean up temporary directory
    shutil.rmtree(package_dir)
    
    print(f\"Distribution package created: {zip_path}\")
    return zip_path

def main():
    \"\"\"Main function\"\"\"
    print(\"Kitaverse Packaging Tool\")
    print(\"=\" * 30)
    
    try:
        package_path = create_distribution()
        print(\"\\nPackage created successfully!\")
        print(f\"Package location: {package_path}\")
        print(\"\\nTo distribute Kitaverse:\")
        print(\"1. Share the ZIP file with users\")
        print(\"2. Users can extract and run install.sh (Linux/Mac) or install.bat (Windows)\")
        print(\"3. Follow the instructions to start the server and open the client\")
    except Exception as e:
        print(f\"Error creating package: {e}\")

if __name__ == \"__main__\":
    main()