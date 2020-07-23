from .models import Result
from app.logger import log


def go_pass_exam(exam_id: int, user_id: int):
    """Function witch connect with button 'Go', and do field 'passed', true or false"""
    # Переводим полученные значения в инт
    exam_id = int(exam_id)
    user_id = int(user_id)
    # находим в таблице результатов соответсвующий экзаменну и текущему пользователю результат прохождения экзаменна
    # (возможно тут лучше будет использовать current_user)
    the_passed = Result.query.filter(
        Result.exam_id == exam_id, Result.user_id == user_id
    ).first()
    if not the_passed:
        # Создать новый инстанс БД
        log(log.WARNING, "EXAM ALREADY NOT PASSED: %s", exam_id)
        the_passed = Result(exam_id=exam_id, user_id=user_id)
        the_passed.passed = True
        the_passed.save()
    passed = the_passed.passed
    if passed is False:
        log(log.INFO, "EXAM PASSED: %s", exam_id)
        passed = True
        the_passed.save()


def next_to_pass_exam(exam_id: int, user_id: int):
    """Function witch connect with button 'Next', and do field 'passed', true or false"""
    # Переводим полученные значения в инт
    exam_id = int(exam_id)
    user_id = int(user_id)
    the_passed = Result.query.filter(
        Result.exam_id == exam_id, Result.user_id == user_id
    ).first()
    if not the_passed:
        # Создать новый инстанс БД
        log(log.ERROR, "EXAM NOT PASSED: %s", exam_id)
        the_passed = Result(exam_id=exam_id, user_id=user_id)
    the_passed.passed = False
    the_passed.save()
