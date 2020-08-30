import os.path
from pathlib import Path
from subprocess import call

# pdf2txt.py のパス
#py_path = Path(sys.exec_prefix) / "Scripts" / "pdf2txt.py"
#C:\Users\otsuka\AppData\Roaming\Python\Python38\Scripts
py_path = Path(os.path.expanduser('~')) / "AppData\Roaming\Python\Python38\Scripts" / "pdf2txt.py"
print(py_path)

# pdf2txt.py の呼び出し
#call(["py", str(py_path), "-o extract-sample.txt", "-p 1", "000120170.pdf"])
call(["py", str(py_path), "-o extract-sample.txt", "-p 1", "shitei-02aomori-ika-r0207.pdf"])
