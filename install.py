import subprocess
import sys


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package , "-U", "--no-cache-dir"])

pyqt5 = True
selenium = True
pynput = True

if sys.version_info[0] < 3:
    print("python version must be at least three\n"
          "recommended version: 3.7")
    exit(1)

try:
    import PyQt5.QtGui
except:
    pyqt5 = False

try:
    import selenium
except:
    selenium = False

try:
    import pynput
except:
    pynput = False


if not pyqt5:
    print("installing pyqt5")
    install("PyQt5")
    pyqt5 = True
if not selenium:
    print("installing selenium")
    install("selenium")
    selenium = True

if not pynput:
    print("installing pynput")
    install("pynput")
    pynput = True


if selenium and pyqt5 and pynput:
    print("everything installed")
    print("you can now start the program")
    input("Press Enter to continue...")