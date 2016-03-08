import sys


def get_max_selected_value(response):
    """
    Gets the max. selected value for a component question response
    :param response:
    :return:
    """
    resp_length = len(str(response))
    try:
        max_selected_value = int(str(response)[resp_length-3:resp_length-2])-1  # -1 to rate from 0 to 10
        print("Max selected value: " + str(max_selected_value))
    except:
        max_selected_value = 0
        print("Error: " + str(sys.exc_info()))
    finally:
        return max_selected_value
        sys.stdout.flush()


def get_list_of_ids(response):
    """
    Gets a list of the selected ids for a response of multiple choice
    :param response:
    :return:
    """
    resp_length = len(str(response))
    left = resp_length-1
    right = resp_length
    return_list = []

    while left >= 0:
        try:
            id = int(str(response)[left:right])
            return_list.append(id)
        except:
            print("Error retrieving ids: " + str(response)[left:right])
            sys.stdout.flush()
        finally:
            left += - 1
            right += - 1

    return return_list