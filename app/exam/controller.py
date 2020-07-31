import os
import subprocess
import tempfile
from flask import redirect, url_for
from .models import Exam
from app.logger import log


def check_answer(exam: Exam, code: str):
    """check exam result"""
    exam_lang = exam.lang.name
    MAP = {
        Exam.Language.py.name: check_answer_py,
        Exam.Language.java.name: check_answer_java,
        Exam.Language.js.name: check_answer_js,
    }
    if exam_lang not in MAP:
        log(log.ERROR, "unknown exam language: [%s]", exam_lang)
        return True
    return MAP[exam_lang](exam, code)


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
        cmd = ["python3", test_file_path]
        try:
            test_process = subprocess.run(cmd, capture_output=True, timeout=1)
            if test_process.stderr:
                for error_line in test_process.stderr.decode().split("\n"):
                    log(log.WARNING, "EXAM ERROR: %s", error_line)
                return False
            return test_process.returncode == 0
        except subprocess.TimeoutExpired:
            log(log.WARNING, "EXAM TIMEOUT: Exam:[]", exam.name)
            return False


def check_answer_java(exam: Exam, code: str):
    return True


def check_answer_js(exam: Exam, code: str):
    return True


def check_answer_choise(exam_id: int, cor_index: str):
    correct_index = Exam.query.filter(Exam.id == exam_id).first()
    if correct_index.correct_answer == cor_index:
        return True


def goto_next_exam(exam_id: int):
    exam_id = int(exam_id)
    the_exam = Exam.query.filter(Exam.id == exam_id).first()
    type_id = the_exam.type_id
    lang = the_exam.lang
    # Взять все экзаменны по заданому языку
    exams = (
        Exam.query.filter(Exam.lang == lang)
        .filter(Exam.type_id == type_id)
        .filter(Exam.deleted != True)  # noqa F712
        .all()
    )
    found_current = False
    next_exam = None
    index = 0
    for exam in exams:
        if found_current:
            next_exam = exam
            break
        if exam.id == exam_id:
            found_current = True
            if index >= (len(exams) - 1):
                first_exam = exams[0]
                next_exam = first_exam
                break
        index += 1

    return redirect(url_for(f"exam.exam_{lang.name}", exam_id=next_exam.id))


def goto_prev_exam(exam_id: int):
    exam_id = int(exam_id)
    the_exam = Exam.query.filter(Exam.id == exam_id).first()
    type_id = the_exam.type_id
    lang = the_exam.lang
    # Взять все экзаменны по заданому языку
    exams = (
        Exam.query.filter(Exam.lang == lang)
        .filter(Exam.type_id == type_id)
        .filter(Exam.deleted != True)  # noqa F712
        .all()
    )

    found_current = False
    next_exam = None
    index = 0
    exams.reverse()
    for exam in exams:
        if found_current:
            next_exam = exam
            break
        if exam.id == exam_id:
            found_current = True
            if index >= (len(exams) - 1):
                first_exam = exams[0]
                next_exam = first_exam
                break
        index += 1

    return redirect(url_for(f"exam.exam_{lang.name}", exam_id=next_exam.id))
