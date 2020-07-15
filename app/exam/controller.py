import os
import subprocess
import tempfile
from flask import redirect, url_for
from .models import Exam
from app.logger import log


def check_answer(exam: Exam, code: str):
    """check exam result"""
    MAP = {
        Exam.Language.py: check_answer_py,
        Exam.Language.java: check_answer_java,
        Exam.Language.js: check_answer_js,
    }
    if exam.lang not in MAP:
        log(log.ERROR, "unknown exam language: [%s]", exam.lang)
        return True
    return MAP[exam.lang](exam, code)


def check_answer_py(exam: Exam, code: str):
    with tempfile.TemporaryDirectory() as tmpdirname:
        test_file_path = os.path.join(tmpdirname, "test.py")
        with open(test_file_path, "w") as f:
            f.write(code)
            f.write("\n")
            if exam.verification:
                f.write("\n")
                f.write("\n")
                f.write(exam.verification)
                f.write("\n")
        cmd = ["python", test_file_path]
        test_process = subprocess.run(cmd, capture_output=True)
        if test_process.stderr:
            for error_line in test_process.stderr.decode().split("\n"):
                log(log.WARNING, "EXAM ERROR: %s", error_line)
        return test_process.returncode == 0


def check_answer_java(exam: Exam, code: str):
    return True


def check_answer_js(exam: Exam, code: str):
    return True


def goto_next_exam(exam_id: int):
    next_exem_id = exam_id
    lang = "py"
    return redirect(url_for(f"exam.exam_{lang}", exam_id=next_exem_id))
