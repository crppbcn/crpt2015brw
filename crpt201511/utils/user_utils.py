from crpt201511.models import Person, User

############################################
#
# Helper functions to manage users and permissions
#
############################################


def get_person_by_username(username):
    """
    Get person by username
    :param username:
    :return:
    """
    user = get_user_by_username(username)
    if user:
        return get_person_by_user(user)
    else:
        return None


def get_person_by_user(user):
    """
    Get person by username
    :param username:
    :return:
    """
    if user:
        try:
            person = Person.objects.get(user=user)
        except:
            person = None
        return person
    else:
        return None

def get_person(request):
    """
    Get person from request
    :param request:
    :return:
    """
    # get username
    username = request.session.get('username')
    return get_person_by_username(username)


def get_user_by_username(username):
    """
    Get person by username
    :param username:
    :return:
    """
    try:
        user = User.objects.get(username=username)
    except:
        user = None
    return user





