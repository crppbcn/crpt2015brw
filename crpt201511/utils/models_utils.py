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