import os
import subprocess
import tempfile
from .models import Exam


def check_answer(exam: Exam, code: str):
    with tempfile.TemporaryDirectory() as tmpdirname:
        test_file_path = os.path.join(tmpdirname, 'test.py')
        with open(test_file_path, 'w') as f:
            f.write(code)
            f.write('\n')
            f.writelines((
                "print('hello')\n",
                "exit(0)\n"
            ))
        cmd = ['python', test_file_path]
        p = subprocess.run(cmd, capture_output=True)
        return p.returncode == 0
