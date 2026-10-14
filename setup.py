#!/usr/bin/env python3
"""
VakilBot Setup Script
Installs dependencies and validates environment
"""
import subprocess
import sys
import os
import shutil


def print_step(msg):
    print(f"\n{'='*60}")
    print(f"  {msg}")
    print('='*60)


def run(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Error: {result.stderr}")
        sys.exit(1)
    return result.stdout


def main():
    backend_dir = os.path.join(os.path.dirname(__file__), "backend")

    print_step("🏛️  VakilBot - Indian Legal Help Bot Setup")

    # Check Python
    print(f"✅ Python {sys.version.split()[0]} detected")

    # Check/create .env
    env_file = os.path.join(backend_dir, ".env")
    env_example = os.path.join(backend_dir, ".env.example")
    if not os.path.exists(env_file):
        shutil.copy(env_example, env_file)
        print(f"📄 Created .env file — please add your GEMINI_API_KEY")
    else:
        print("✅ .env file found")

    # Check API key
    api_key = ""
    with open(env_file) as f:
        for line in f:
            if line.startswith("GEMINI_API_KEY="):
                api_key = line.split("=", 1)[1].strip()

    if not api_key or api_key == "your_gemini_api_key_here":
        print("\n⚠️  GEMINI_API_KEY not set!")
        print("   1. Go to https://aistudio.google.com/app/apikey")
        print("   2. Create a free API key")
        print(f"   3. Edit {env_file}")
        print("   4. Set: GEMINI_API_KEY=your_actual_key")
        print("\n   Then run this script again or run: py -3 backend/main.py")
        sys.exit(0)

    print_step("📦 Installing Python dependencies...")
    run(f'py -3 -m pip install -r requirements.txt --quiet', cwd=backend_dir)
    print("✅ Dependencies installed")

    print_step("🚀 Starting VakilBot server...")
    print("   Frontend: http://localhost:8000")
    print("   API Docs: http://localhost:8000/docs")
    print("   Press Ctrl+C to stop")

    os.chdir(backend_dir)
    subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])


if __name__ == "__main__":
    main()
