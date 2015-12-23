

def check_person_access_to_assessment(assessment, person):
    """
    Check logged user access permission to the assessment
    :param assessment:
    :param person:
    :return:
    """
    if not assessment or not person or assessment.city != person.city:
        return False
    else:
        return True


def get_remote_folder_name(assessment, section):
    """
    Get remote folder name to put uploaded files
    :param assessment:
    :param section:
    :return:
    """
    return assessment.name.replace(' ','') + "-" + str(assessment.date_started) + "-" + section.name.replace(' ','')