import subprocess
subprocess.run(['python3','reference.py'],check=True)
print('Reference passed; production PDF/render remains a separate gate.')
