"""
Simple script to help with backend deployment
This script provides guidance for deploying the CORS fixes to Render
"""

import subprocess
import sys

def run_command(command, description):
    """Run a command and display the result"""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(f"Exit code: {result.returncode}")
        if result.stdout:
            print(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            print(f"STDERR:\n{result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def main():
    print("AI Research Assistant - Backend Deployment Helper")
    print("=" * 60)
    
    print("\nCORS FIX SUMMARY:")
    print("1. Updated CORS middleware to allow all origins")
    print("2. Added explicit OPTIONS handler for /api/query")
    print("3. Added CORS headers to POST responses")
    
    print("\nDEPLOYMENT INSTRUCTIONS:")
    print("1. Push changes to Git repository")
    print("2. Render will automatically deploy the changes")
    print("3. Wait for deployment to complete (2-3 minutes)")
    print("4. Test the frontend application")
    
    print("\nFILES MODIFIED:")
    print("- backend/app/main.py (CORS middleware)")
    print("- backend/app/routes/query_router.py (OPTIONS handler)")
    
    # Check if git is available
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        print(f"\n{'='*50}")
        print("Git is available. You can deploy with:")
        print("1. git add .")
        print("2. git commit -m 'Fix CORS issues for deployment'")
        print("3. git push")
        print(f"{'='*50}")
    except:
        print("\nGit not found. Please manually push changes to your repository.")
    
    print("\nAfter deployment, test with:")
    print("python test_cors_fix.py")
    
    print("\nIf issues persist, check:")
    print("1. Render deployment logs")
    print("2. Environment variables in Render dashboard")
    print("3. Browser developer tools for detailed CORS errors")

if __name__ == "__main__":
    main()
