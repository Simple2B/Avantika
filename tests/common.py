from app.auth.models import User, Role, UserRoles


def register(user_name, password="password"):
    # noinspection PyArgumentList
    user = User(username=user_name, password=password)
    user.save()
    return user.id


def login(client, user_id, password="password"):
    return client.post(
        "/login", data=dict(user_id=user_id, password=password), follow_redirects=True,
    )


def logout(client):
    return client.get("/logout", follow_redirects=True)


def create_user(username, password, role_name):
    user = User(username=username)
    user.password = password
    user.save()
    role = Role.query.filter(Role.name == role_name).first()
    if not role:
        role = Role(name=role_name)
        role.save()
    user_to_role = UserRoles(user_id=user.id, role_id=role.id)
    user_to_role.save()
