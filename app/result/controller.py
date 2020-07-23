from .models import Result
from app.logger import log


def go_pass_exam(exam_id: int, user_id: int):
    """Function mark exam as passed for the user

    Args:
        exam_id (int): exam ID
        user_id (int): user ID
    """
    result = Result.query.filter(
        Result.exam_id == exam_id, Result.user_id == user_id
    ).first()
    if not result:
        log(log.DEBUG, "Create new result: user_id:%d exam_id:%d", user_id, exam_id)
        result = Result(exam_id=exam_id, user_id=user_id)
    result.passed = True
    result.save()


def next_to_pass_exam(exam_id: int, user_id: int):
    """Function mark exam as passed for the user

    Args:
        exam_id (int): exam ID
        user_id (int): user ID
    """
    result = Result.query.filter(
        Result.exam_id == exam_id, Result.user_id == user_id
    ).first()
    if not result:
        log(log.ERROR, "EXAM NOT PASSED: %s", exam_id)
        result = Result(exam_id=exam_id, user_id=user_id)
    result.passed = False
    result.save()
