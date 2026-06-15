# test_setup.py
# Save karo C:\ai_engineer\ mein aur chalaao

import sys
import subprocess

print("=" * 50)
print("AI Engineer Setup Verification")
print("=" * 50)

# Python version check
python_version = sys.version
print(f"✅ Python: {python_version}")

# Library checks
libraries = ["openai", "dotenv", "jupyter"]
for lib in libraries:
    try:
        __import__(lib)
        print(f"✅ {lib}: Installed")
    except ImportError:
        print(f"❌ {lib}: NOT installed — run: pip install {lib}")

print("=" * 50)
print("Agar sab ✅ hain toh SETUP COMPLETE! 🎉")
print("Week 1 shuru karne ke liye ready ho!")
print("=" * 50)