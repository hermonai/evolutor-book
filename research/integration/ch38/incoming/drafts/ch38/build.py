import subprocess
subprocess.run(['python3','reference.py'],check=True)
print('Reference passed; GPU benchmark and production PDF render remain separate gates.')
