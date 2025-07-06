#!/usr/bin/env python3
"""
run_streamlit.py
Entrypoint script that automatically launches your NXID Tokenomics Streamlit app.
It will look for 'NXID_tokenomics.py' first, then 'main.py'.
"""
import os
import sys
import subprocess

def find_entry_script():
    """Return path to the first existing entry script."""
    cwd = os.path.abspath(os.path.dirname(__file__))
    for fname in ("NXID_tokenomics.py", "main.py"):
        path = os.path.join(cwd, fname)
        if os.path.isfile(path):
            return path
    return None

def run_streamlit(entry_path):
    """Invoke Streamlit CLI to run the given script."""
    cmd = [
        sys.executable, "-m", "streamlit", "run", entry_path,
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false"
    ]
    subprocess.check_call(cmd)

def main():
    entry = find_entry_script()
    if not entry:
        print("❌ Error: No entry script found. Expected 'NXID_tokenomics.py' or 'main.py'.")
        sys.exit(1)
    print(f"▶️ Launching Streamlit app from '{os.path.basename(entry)}'...")
    try:
        run_streamlit(entry)
    except subprocess.CalledProcessError as e:
        print(f"❌ Streamlit failed with exit code {e.returncode}.")
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
