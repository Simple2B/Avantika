#!/user/bin/env python
import json
import click

from app import create_app, db, models, forms
from app.auth.models import User
from app.exam.models import Exam

app = create_app()


# flask cli context setup
@app.shell_context_processor
def get_context():
    """Objects exposed here will be automatically available from the shell."""
    return dict(app=app, db=db, models=models, forms=forms)


def load_exams():
    with open('exams.json', 'r') as f:
        for exam in json.load(f):
            if not Exam.query.filter(Exam.name == exam['name']).first():
                Exam(name=exam['name']).from_dict(**exam).save()


@app.cli.command()
def create_db():
    """Create the configured database."""
    db.create_all()
    admin = User(username="admin")
    admin.password = "admin"
    admin.save()
    load_exams()


@app.cli.command()
@click.confirmation_option(prompt="Drop all database tables?")
def drop_db():
    """Drop the current database."""
    db.drop_all()


if __name__ == "__main__":
    app.run()
