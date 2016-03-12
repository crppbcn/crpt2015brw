from __future__ import division

from crpt201511.models import HazardGroup, HazardType, AssessmentHazardType

class HazardGroupSelected:
    """
    Represents a hazard group with selected hazard types
    """
    def __init__(self):
        self.name = ''
        self.percen = 0,0
        self.hazard_types = {}


def get_hazards_selected(assessment):
    """
    Retrieves the answered hazards in an assessment
    :param assessment:
    :return:
    """
    # get hazard types in the assessment
    hazard_types = AssessmentHazardType.objects.filter(assessment=assessment)

    # construct the result
    n_of_hts = 0

    group_dict = {}

    for hg in HazardGroup.objects.all().order_by('id'):
        ht_dict = {}
        for ht in HazardType.objects.filter(hazard_group=hg).order_by('id'):
            for aht in AssessmentHazardType.objects.filter(assessment=assessment, hazard_type=ht).order_by('id'):
                if aht.is_selected():
                    n_of_hts += 1
                    ht_dict[aht.hazard_type.name] = 1
        if len(ht_dict) > 0:
            group_dict[hg.name] = ht_dict

    #print("group_dict: " + str(group_dict))

    for key_g in group_dict.keys():
        for key_t in group_dict[key_g].keys():
            group_dict[key_g][key_t] = float("{0:.2f}".format(group_dict[key_g][key_t] / n_of_hts * 100))


    #print("group_dict: " + str(group_dict))

    return group_dict

