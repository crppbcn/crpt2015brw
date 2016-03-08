from __future__ import division
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.template import RequestContext, loader
from django.shortcuts import redirect, render_to_response
from django.http import HttpResponse
from django.forms.models import modelformset_factory


from crpt201511.utils.user_utils import *
from crpt201511.models import *
from crpt201511.utils.env_utils import *
from crpt201511.utils.assessment_utils import *
from crpt201511.settings import CRPT_URL
from crpt201511.forms import AssessmentHazardTypeForm


@ensure_csrf_cookie
@login_required
def hazard_groups(request, assessment_id):
    """
    View for the hazard groups page

    :param request:
    :return:
    """
    try:
        person = get_person(request)
        assessment = Assessment.objects.get(id=assessment_id)
        # check person has rights for the assessment. TODO: Constants
        if not check_person_access_to_assessment(assessment, person):
            print("assessment: " + assessment.name)
            raise Exception('User has no permission to access this assessment')

        hazard_groups = HazardGroup.objects.all().order_by('id')
        nohg = len(hazard_groups)
        hg_width = 100 / nohg

        template = loader.get_template(TEMPLATE_HAZARDS_GROUPS_PAGE)
        context = RequestContext(request, {
            'person': person,
            'assessment': assessment,
            'hazard_groups': hazard_groups,
            'hg_width': hg_width,
        })
        return HttpResponse(template.render(context))
    except:
        if debug_is_on():
            raise
        else:
            return render_to_response(TEMPLATE_ERROR,
                                      {"error_description": sys.exc_info(), "crpt_url": CRPT_URL},
                                      context_instance=RequestContext(request))


@ensure_csrf_cookie
@login_required
def hazard_types(request, assessment_id, hg_id):
    """
    View for the hazard types page

    :param request:
    :return:
    """
    try:
        person = get_person(request)
        assessment = Assessment.objects.get(id=assessment_id)
        # check person has rights for the assessment. TODO: Constants
        if not check_person_access_to_assessment(assessment, person):
            print("assessment: " + assessment.name)
            raise Exception('User has no permission to access this assessment')

        hazard_types = HazardType.objects.filter(hazard_group_id=hg_id).order_by('id')
        nohg = len(hazard_types)
        ht_width = 100 / nohg

        template = loader.get_template(TEMPLATE_HAZARDS_TYPES_PAGE)
        context = RequestContext(request, {
            'person': person,
            'assessment': assessment,
            'hazard_types': hazard_types,
            'ht_width': ht_width,
        })
        return HttpResponse(template.render(context))
    except:
        if debug_is_on():
            raise
        else:
            return render_to_response(TEMPLATE_ERROR,
                                      {"error_description": sys.exc_info(), "crpt_url": CRPT_URL},
                                      context_instance=RequestContext(request))

@ensure_csrf_cookie
@login_required
def hazard_type_detail(request, assessment_id, ht_id):
    """
    View for the hazard type detail page

    :param request:
    :return:
    """
    try:
        person = get_person(request)
        assessment = Assessment.objects.get(id=assessment_id)
        # check person has rights for the assessment. TODO: Constants
        if not check_person_access_to_assessment(assessment, person):
            print("assessment: " + assessment.name)
            raise Exception('User has no permission to access this assessment')

        ht = HazardType.objects.get(id=ht_id)

        # formset definition
        fs = modelformset_factory(AssessmentHazardType, max_num=0, exclude=[], form=AssessmentHazardTypeForm)

        if request.method == 'POST':

            f_set = fs(request.POST, request.FILES)
            if f_set and f_set.is_valid():
                f_set.save()
            else:
                print(str(f_set.errors))
                sys.stdout.flush()

        else:
            query_set = AssessmentHazardType.objects.filter(id=ht_id).order_by('order')
            f_set = fs(queryset=query_set)



        # return page
        template = loader.get_template(TEMPLATE_HAZARDS_DETAIL_PAGE)
        context = RequestContext(request, {
            'person': person,
            'assessment': assessment,
            'selected': "HT_DETAIL",
            'ht': ht,
            'fs': f_set,
        })
        return HttpResponse(template.render(context))
    except:
        if debug_is_on():
            raise
        else:
            return render_to_response(TEMPLATE_ERROR,
                                      {"error_description": sys.exc_info(), "crpt_url": CRPT_URL},
                                      context_instance=RequestContext(request))

@ensure_csrf_cookie
@login_required
def hazard_type_interrelations(request, assessment_id, ht_id):
    """
    View for the hazard type interrelations page

    :param request:
    :return:
    """
    try:
        person = get_person(request)
        assessment = Assessment.objects.get(id=assessment_id)
        # check person has rights for the assessment. TODO: Constants
        if not check_person_access_to_assessment(assessment, person):
            print("assessment: " + assessment.name)
            raise Exception('User has no permission to access this assessment')

        ht = HazardType.objects.get(id=ht_id)



        template = loader.get_template(TEMPLATE_HAZARDS_INTERRELATIONS_PAGE)
        context = RequestContext(request, {
            'person': person,
            'assessment': assessment,
            'selected': "HT_DETAIL",
            'ht': ht,
        })
        return HttpResponse(template.render(context))
    except:
        if debug_is_on():
            raise
        else:
            return render_to_response(TEMPLATE_ERROR,
                                      {"error_description": sys.exc_info(), "crpt_url": CRPT_URL},
                                      context_instance=RequestContext(request))

@ensure_csrf_cookie
@login_required
def hazard_type_impacts(request, assessment_id, ht_id, element_id=None):
    """
    View for the hazard type interrelations page

    :param request:
    :return:
    """
    try:
        person = get_person(request)
        assessment = Assessment.objects.get(id=assessment_id)
        # check person has rights for the assessment. TODO: Constants
        if not check_person_access_to_assessment(assessment, person):
            print("assessment: " + assessment.name)
            raise Exception('User has no permission to access this assessment')

        ht = HazardType.objects.get(id=ht_id)



        template = loader.get_template(TEMPLATE_HAZARDS_IMPACTS_PAGE)
        context = RequestContext(request, {
            'person': person,
            'assessment': assessment,
            'selected': "HT_DETAIL",
            'ht': ht,
        })
        return HttpResponse(template.render(context))
    except:
        if debug_is_on():
            raise
        else:
            return render_to_response(TEMPLATE_ERROR,
                                      {"error_description": sys.exc_info(), "crpt_url": CRPT_URL},
                                      context_instance=RequestContext(request))
