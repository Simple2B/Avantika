from flask import flash, redirect, url_for

from exam.models import Exam
from exam.controller import goto_next_exam
from auth.models import User
from .models import Result

# from app.logger import log


"""Function witch connect with button 'Go', and do field 'passed', true or false"""


def go_pass_exam(exam_id: int, user_id: int):
    # Переводим полученные значения в инт
    exam_id = int(exam_id)
    user_id = int(user_id)
    # Находим язык экзамена что бы правильно в конце редиректить
    the_lang = Exam.query.filter(Exam.id == exam_id).first()
    lang = the_lang.lang
    # находим в таблице результатов соответсвующий экзаменну и текущему пользователю результат прохождения экзаменна
    # (возможно тут лучше будет использовать current_user)
    the_passed = Result.query.filter(Exam.id == exam_id, User.id == user_id).first()
    passed = the_passed.passed
    if passed is None:
        # Создать новый инстанс БД
        # Если ответ на форме экзаменна сейчас был введен верно поставить passed = True
        # Если ответ на форме экзаменна сейчас введен не верно поставить passed = False
        pass
    if passed:
        flash("Exam successful passed already", "success")
    if passed is False:
        # Если ответ на форме экзаменна сейчас был введен верно поставить passed = True
        pass
    return redirect(url_for(f"exam.exam_{lang.name}"))


"""Function witch connect with button 'Go', and do field 'passed', true or false"""


def next_to_pass_exam(exam_id: int, user_id: int):
    # Переводим полученные значения в инт
    exam_id = int(exam_id)
    user_id = int(user_id)
    # находим в таблице результатов соответсвующий экзаменну и текущему пользователю результат прохождения экзаменна
    # (возможно тут лучше будет использовать current_user)
    the_passed = Result.query.filter(Exam.id == exam_id, User.id == user_id).first()
    passed = the_passed.passed
    if passed is None:
        # Создать новый инстанс БД
        passed = False
        pass
    if passed:
        flash("Exam successful passed already", "success")
    if passed is False:
        passed = False
        pass
    return goto_next_exam(exam_id)
