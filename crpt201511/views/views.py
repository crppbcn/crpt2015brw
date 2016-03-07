from __future__ import division

from threading import Thread

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.forms.models import modelformset_factory, inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext, loader
from django.template.response import TemplateResponse
from django.views.decorators.csrf import ensure_csrf_cookie


from crpt201511.utils.assessment_utils import *
from crpt201511.utils.user_utils import *

from crpt201511.constants import *
from crpt201511.models import *
from crpt201511.settings import CRPT_URL
from crpt201511.trace import *
from crpt201511.utils.env_utils import *
from crpt201511.forms import *
from crpt201511.utils.form_utils import *
from crpt201511.my_ftp import MyFTP


# ###############################################
#
# Navigation Views
#
################################################

def my_copyright(request):
    """
    View for the my_copyright page

    :param request:
    :return:
    """
    try:
        username = request.session.get('username')
        try:
            index_card = None
            #index_card = IndexCard.objects.get(username=username)
        except:
            index_card = None
        template = loader.get_template(TEMPLATE_COPYRIGHT)
        context = RequestContext(request, {
            'username': username,
            'is_copyright': 'is_copyright',
        })
        return HttpResponse(template.render(context))
    except:
        if debug_is_on():
            raise
        else:
            return render_to_response(TEMPLATE_ERROR,
                                      {"error_description": sys.exc_info(),
                                       "crpt_url": CRPT_URL},
                                      context_instance=RequestContext(request))


@ensure_csrf_cookie
@login_required
def welcome(request):
    """
    View for the welcome page

    :param request:
    :return:
    """
    try:
        person = get_person(request)
        # try:
        # get the latest assessment from the city. TODO: get the right assessment
        assessment = Assessment.objects.order_by('-date_started')[0]
        # except:
            # raise Exception('The City does not have any open assessment')
        template = loader.get_template(TEMPLATE_WELCOME)

        print("degree of completion: " + str(assessment.degree_of_completion))
        print("100-degree of completion: " + str(float(100-assessment.degree_of_completion)))

        total_mov_questions = assessment.mov_public_knowledge_noq + assessment.mov_media_noq + \
                              assessment.mov_official_document_noq

        context = RequestContext(request, {
            'person': person,
            'assessment': assessment,
            'filled_percen': str(assessment.degree_of_completion),
            'not_filled_percen': str(float(100-assessment.degree_of_completion)),
            'organisational_score': str(assessment.organizational_score),
            'physical_score': str(assessment.physical_score),
            'functional_score': str(assessment.functional_score),
            'mov_public_knowledge': str(assessment.mov_public_knowledge_noq),
            'mov_media': str(assessment.mov_media_noq),
            'mov_official_document': str(assessment.mov_official_document_noq),
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
def steps(request, assessment_id):
    """
    View for the steps page

    :param request:
    :return:
    """
    try:
        person = get_person(request)
        assessment = Assessment.objects.get(id=assessment_id)
        try:
            # TODO: implement logic to not show again welcome page
            sections = CityIDSection.objects.filter(parent=None).order_by('order')
        except:
            sections = None
        template = loader.get_template(TEMPLATE_STEPS)
        context = RequestContext(request, {
            'person': person,
            'assessment': assessment,
            'sections': sections,
        })
        return HttpResponse(template.render(context))
    except:
        if debug_is_on():
            raise
        else:
            return render_to_response(TEMPLATE_ERROR,
                                      {"error_description": sys.exc_info(), "crpt_url": CRPT_URL},
                                      context_instance=RequestContext(request))




# ###############################################
#
# TEST
#
################################################
def test(request):
    # get assessment
    assessment = Assessment.objects.all()[:1]
    # formsets
    FormsetQtype1 = modelformset_factory(QuestionType1)
    FormsetQtype2 = modelformset_factory(QuestionType2)
    FormsetQtype3 = modelformset_factory(QuestionType3)
    # querysets
    qset_qtype1 = QuestionType1.objects.all()
    qset_qtype2 = QuestionType2.objects.all()
    qset_qtype3 = QuestionType3.objects.all()
    # formsets to template
    fset_qtype1 = FormsetQtype1(queryset=qset_qtype1)
    fset_qtype2 = FormsetQtype1(queryset=qset_qtype2)
    fset_qtype3 = FormsetQtype1(queryset=qset_qtype3)
    # return to template
    template = loader.get_template(TEMPLATE_TEST)
    context = RequestContext(request, {
        'fset_qtype1': fset_qtype1,
        'fset_qtype2': fset_qtype2,
        'fset_qtype3': fset_qtype3,
    })
    return HttpResponse(template.render(context))