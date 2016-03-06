import sys

from threading import Thread

from django.dispatch import receiver


from crpt201511.signals.my_signals import recalculate_element_score
from crpt201511.utils.scoring_utils import calculate_overall_element_scoring


def handle_recalculate_element_score(sender, **kwargs):
    if sender:
        # throw recalculation for element
        print("Handling signal!!!")
        t = Thread(target=calculate_overall_element_scoring, args=(sender,))
        t.start()
    else:
        print("Handling signal!!! - No sender!!!")
    sys.stdout.flush()


recalculate_element_score.connect(handle_recalculate_element_score)