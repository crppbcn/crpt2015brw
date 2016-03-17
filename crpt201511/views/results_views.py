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
from crpt201511.utils.hazard_utils import *


@ensure_csrf_cookie
@login_required
def results_hazards(request, assessment_id):
    """
    View for hazards selected diagram
    :param request:
    :param assessment_id:
    :return:
    """
    try:
        person = get_person(request)
        assessment = Assessment.objects.get(id=assessment_id)
        # check person has rights for the assessment. TODO: Constants
        if not check_person_access_to_assessment(assessment, person):
            print("assessment: " + assessment.name)
            raise Exception('User has no permission to access this assessment')

        # get hazards selected
        hs_list = get_hazards_selected(assessment)

        # return page
        template = loader.get_template(TEMPLATE_RESULTS_HAZARDS)
        context = RequestContext(request, {
            'person': person,
            'assessment': assessment,
            'selected_main': "HAZARDS_SELECTED",
            'hazard_selected': hs_list,
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
def results_overall(request, assessment_id):
    """
    View for hazards selected diagram
    :param request:
    :param assessment_id:
    :return:
    """
    try:
        person = get_person(request)
        # try:
        # get the latest assessment from the city.
        if assessment_id:
            assessment = Assessment.objects.get(id=assessment_id)
        else:
            assessment = Assessment.objects.order_by('-date_started')[0]
        # except:
            # raise Exception('The City does not have any open assessment')
        template = loader.get_template(TEMPLATE_RESULTS_OVERALL)

        context = RequestContext(request, {
            'person': person,
            'assessment': assessment,
            'filled_percen': str(assessment.degree_of_completion),
            'not_filled_percen': str(float(100-assessment.degree_of_completion)),
            'city_id_percen': str(assessment.city_id_completion),
            'hazards_percen': str(assessment.hazards_completion),
            'stakeholders_percen': str(assessment.stakeholders_completion),
            'organisational_score': str(assessment.organizational_score),
            'physical_score': str(assessment.physical_score),
            'functional_score': str(assessment.functional_score),
            'mov_public_knowledge': str(assessment.mov_public_knowledge_noq),
            'mov_media': str(assessment.mov_media_noq),
            'mov_official_document': str(assessment.mov_official_document_noq),
            'selected_main': "RESULTS_OVERALL",
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
def results_dashboard_bcn(request, assessment_id):
    """
    View for hazards selected diagram
    :param request:
    :param assessment_id:
    :return:
    """
    try:
        person = get_person(request)
        # try:
        # get the latest assessment from the city.
        if assessment_id:
            assessment = Assessment.objects.get(id=assessment_id)
        else:
            assessment = Assessment.objects.order_by('-date_started')[0]
        # except:
            # raise Exception('The City does not have any open assessment')
        template = loader.get_template(TEMPLATE_RESULTS_DASHBOARD_BCN)

        context = RequestContext(request, {
            'person': person,
            'assessment': assessment,
            'selected_main': "RESULTS_DASHBOARD",
            'selected_detail': "RESULTS_DASHBOARD_BCN",
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
def results_dashboard_cagayan(request, assessment_id):
    """
    View for hazards selected diagram
    :param request:
    :param assessment_id:
    :return:
    """
    try:
        person = get_person(request)
        # try:
        # get the latest assessment from the city.
        if assessment_id:
            assessment = Assessment.objects.get(id=assessment_id)
        else:
            assessment = Assessment.objects.order_by('-date_started')[0]
        # except:
            # raise Exception('The City does not have any open assessment')
        template = loader.get_template(TEMPLATE_RESULTS_DASHBOARD_CAGAYAN)

        context = RequestContext(request, {
            'person': person,
            'assessment': assessment,
            'selected_main': "RESULTS_DASHBOARD",
            'selected_detail': "RESULTS_DASHBOARD_CAGAYAN",
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
def results_dashboard_lokoja(request, assessment_id):
    """
    View for hazards selected diagram
    :param request:
    :param assessment_id:
    :return:
    """
    try:
        person = get_person(request)
        # try:
        # get the latest assessment from the city.
        if assessment_id:
            assessment = Assessment.objects.get(id=assessment_id)
        else:
            assessment = Assessment.objects.order_by('-date_started')[0]
        # except:
            # raise Exception('The City does not have any open assessment')
        template = loader.get_template(TEMPLATE_RESULTS_DASHBOARD_LOKOJA)

        context = RequestContext(request, {
            'person': person,
            'assessment': assessment,
            'selected_main': "RESULTS_DASHBOARD",
            'selected_detail': "RESULTS_DASHBOARD_LOKOJA",
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
def results_dashboard_tehran(request, assessment_id):
    """
    View for hazards selected diagram
    :param request:
    :param assessment_id:
    :return:
    """
    try:
        person = get_person(request)
        # try:
        # get the latest assessment from the city.
        if assessment_id:
            assessment = Assessment.objects.get(id=assessment_id)
        else:
            assessment = Assessment.objects.order_by('-date_started')[0]
        # except:
            # raise Exception('The City does not have any open assessment')
        template = loader.get_template(TEMPLATE_RESULTS_DASHBOARD_TEHRAN)

        context = RequestContext(request, {
            'person': person,
            'assessment': assessment,
            'selected_main': "RESULTS_DASHBOARD",
            'selected_detail': "RESULTS_DASHBOARD_TEHRAN",
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
def results_gis_google(request, assessment_id):
    """
    View for hazards selected diagram
    :param request:
    :param assessment_id:
    :return:
    """
    try:
        person = get_person(request)
        # try:
        # get the latest assessment from the city.
        if assessment_id:
            assessment = Assessment.objects.get(id=assessment_id)
        else:
            assessment = Assessment.objects.order_by('-date_started')[0]
        # except:
            # raise Exception('The City does not have any open assessment')
        template = loader.get_template(TEMPLATE_RESULTS_GIS_GOOGLE)

        context = RequestContext(request, {
            'person': person,
            'assessment': assessment,
            'selected_main': "RESULTS_GIS",
            'selected_detail': "RESULTS_GIS_GOOGLE",
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
def results_gis_no_base(request, assessment_id):
    """
    View for hazards selected diagram
    :param request:
    :param assessment_id:
    :return:
    """
    try:
        person = get_person(request)
        # try:
        # get the latest assessment from the city.
        if assessment_id:
            assessment = Assessment.objects.get(id=assessment_id)
        else:
            assessment = Assessment.objects.order_by('-date_started')[0]
        # except:
            # raise Exception('The City does not have any open assessment')
        template = loader.get_template(TEMPLATE_RESULTS_GIS_NO_BASE)

        context = RequestContext(request, {
            'person': person,
            'assessment': assessment,
            'selected_main': "RESULTS_GIS",
            'selected_detail': "RESULTS_GIS_NO_BASE",
        })
        return HttpResponse(template.render(context))
    except:
        if debug_is_on():
            raise
        else:
            return render_to_response(TEMPLATE_ERROR,
                                      {"error_description": sys.exc_info(), "crpt_url": CRPT_URL},
                                      context_instance=RequestContext(request))
