from __future__ import division
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.template import RequestContext, loader
from django.shortcuts import redirect, render_to_response
from django.http import HttpResponse
from django.forms.models import modelformset_factory

from threading import Thread

from crpt201511.utils.user_utils import *
from crpt201511.models import *
from crpt201511.utils.env_utils import *
from crpt201511.utils.assessment_utils import *
from crpt201511.settings import CRPT_URL
from crpt201511.forms import AssessmentStakeholderForm
from crpt201511.trace import *
from crpt201511.utils.mail_utils import *

@ensure_csrf_cookie
@login_required
def stakeholder_groups(request, assessment_id):
    """
    View for stakeholders
    :param request:
    :return:
    """
    try:
        person = get_person(request)
        assessment = Assessment.objects.get(id=assessment_id)
        # check person has rights for the assessment.
        if not check_person_access_to_assessment(assessment, person):
            print("assessment: " + assessment.name)
            raise Exception('User has no permission to access this assessment')

        stakeholder_groups = StakeholderGroup.objects.all().order_by('id')

        template = loader.get_template(TEMPLATE_STAKEHOLDERS_GROUPS_PAGE)
        context = RequestContext(request, {
            'person': person,
            'assessment': assessment,
            'stakeholder_groups': stakeholder_groups,
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
def stakeholders(request, assessment_id, sg_id, st_id=None, s_id=None):
    """
    View for the stakeholders page

    :param request:
    :param assessment_id:
    :param sg_id:
    :param st_id:
    :param s_id:
    :return:
    """
    try:
        person = get_person(request)
        assessment = Assessment.objects.get(id=assessment_id)
        # check person has rights for the assessment.
        if not check_person_access_to_assessment(assessment, person):
            print("assessment: " + assessment.name)
            raise Exception('User has no permission to access this assessment')

        # stakeholders group
        sg = StakeholderGroup.objects.get(id=sg_id)
        # stakeholder types
        sts = StakeholderType.objects.filter(stakeholder_group=sg).order_by('id')
        # stakeholder type
        if st_id:
            st = StakeholderType.objects.get(id=st_id)
        else:
            st = sts[:1].get()
        # stakeholder
        if s_id:
            s = Stakeholder.objects.get(id=s_id)
        else:
            s = Stakeholder.objects.filter(stakeholder_type=st).order_by('id')[:1].get()

        # AssessmentStakeHolders
        assessment_stakeholders = AssessmentStakeholder.objects.filter(assessment=assessment, stakeholder=s).order_by('id')

        # get considerations
        considerations = StakeholderGroupConsideration.objects.filter(stakeholder_group=sg).order_by('id')

        # comments
        comments = AssessmentStakeholderComment.objects.filter(assessment_stakeholder__in=assessment_stakeholders)

        # formset
        fs = modelformset_factory(AssessmentStakeholder, max_num=0, exclude=[], form=AssessmentStakeholderForm)

        if request.method == 'POST':
            f_set = fs(request.POST, request.FILES)
            if f_set and f_set.is_valid():
                f_set.save()

                # redirect to next page
                url_to_redirect_base = '/stakeholders/' + str(assessment_id) + SLASH
                url_to_redirect_sg = url_to_redirect_base + str(sg.id) + SLASH
                url_to_redirect_st = url_to_redirect_sg + str(st.id) + SLASH
                if s.next_one:
                    url_to_redirect = url_to_redirect_sg + str(s.next_one.stakeholder_type.id) + SLASH + \
                                      str(s.next_one.id) + SLASH
                else:
                    if st.next_one:
                        url_to_redirect = url_to_redirect_sg + str(st.next_one.id) + SLASH
                    else:
                        if sg.next_one:
                            url_to_redirect = url_to_redirect_base + str(sg.next_one.id) + SLASH
                        else:
                            url_to_redirect = url_to_redirect_sg

                return redirect(url_to_redirect, context_instance=RequestContext(request))

            else:
                print(str(f_set.errors))
                sys.stdout.flush()

        else:
            query_set = assessment_stakeholders
            f_set = fs(queryset=query_set)

        # return page
        template = loader.get_template(TEMPLATE_STAKEHOLDERS_PAGE)
        context = RequestContext(request, {
            'person': person,
            'assessment': assessment,
            'fs': f_set,
            'stakeholder_types': sts,
            'stakeholder_group': sg,
            'stakeholder_type': st,
            'stakeholder': s,
            'considerations': considerations,
            'comments': comments,
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
def add_stakeholder_comment(request):
    """
    View to add comment to a stakeholder

    :param request:
    :return:
    """
    try:
        person = get_person(request)

        if request.method == "POST":
            # get values from form
            assessment_id = request.POST['assessment_id']
            try:
                stakeholder_group_id = request.POST['stakeholder_group_id']
            except:
                stakeholder_group_id = None
            try:
                stakeholder_type_id = request.POST['stakeholder_type_id']
            except:
                stakeholder_type_id = None
            try:
                stakeholder_id = request.POST['stakeholder_id']
            except:
                stakeholder_id = None
            comment = request.POST['textComments']

            # get section and assessment
            stakeholder = AssessmentStakeholder.objects.get(id=stakeholder_id)
            # create comment
            my_comment = AssessmentStakeholderComment()
            my_comment.assessment_stakeholder = stakeholder
            my_comment.comment = comment
            my_comment.person = person
            my_comment.save()

            # trace action
            trace_action(TRACE_COMMENT, person, "User added comment in assessment_stakeholder: " + stakeholder.name)

            # send mail
            try:
                send_mail = request.POST['send_mail']
                t = Thread(target=send_comments_email, args=(my_comment.comment, "Stakeholder: " + stakeholder.name, person))
                t.start()
                # send_comments_email(my_comment.comment, section, person)
            except:
                # checkbox not set
                pass

            # redirect to hazard_type page
            url_to_redirect = "/stakeholders/" + str(assessment_id) + SLASH + str(stakeholder_group_id) + SLASH + \
                              str(stakeholder_type_id) + SLASH + str(stakeholder.id) + SLASH

            return redirect(url_to_redirect, context_instance=RequestContext(request))
        else:
            raise Exception("GET call to add new section comment")
    except:
        if debug_is_on():
            raise
        else:
            return render_to_response(TEMPLATE_ERROR, {"error_description": sys.exc_info(), "crpt_url": CRPT_URL},
                                      context_instance=RequestContext(request))
