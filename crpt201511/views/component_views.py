from __future__ import division

from threading import Thread

import math

from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext, loader
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
from crpt201511.utils.mail_utils import send_comments_email


@ensure_csrf_cookie
@login_required
def component(request, assessment_id, component_id=None, subcomponent_id=None, third_component_id=None):
    """
    View for component of indicators form

    :param request:
    :param assessment_id: assessment id
    :param component_id: component id
    :param subcomponent_id: subcomponent id
    :param third_component_id: third_component id
    :return:
    """
    try:
        left_elements = None

        # get username from session
        person = get_person(request)
        # get assessment
        assessment = Assessment.objects.get(id=assessment_id)
        # check person has rights for the assessment. TODO: Constants
        if not check_person_access_to_assessment(assessment, person):
            print("assessment: " + assessment.name)
            raise Exception('User has no permission to access this assessment')

        # get component
        if component_id:
            component = Component.objects.get(id=component_id)
        else:
            component = Component.objects.all().order_by('order')[:1].get()

        # elements of menu
        menu_elements = Component.objects.filter(parent=None).order_by('order')

        # TODO: review data_loader to assign parent properly

        # adjustment of horizontal menu
        menu_horizontal_elem_width = math.floor(100/len(menu_elements))

        # get subcomponent
        if subcomponent_id:
            subcomponent = Component.objects.get(id=subcomponent_id)
        else:
            try:
                subcomponent = Component.objects.filter(parent=component).order_by('order')[:1].get()
            except:
                subcomponent = None

        # elements of left menu
        if component:
            left_elements = Component.objects.filter(parent_id=component.id).order_by('order')

        # third level of hierarchy
        if third_component_id:
            third_component = Component.objects.get(id=third_component_id)
        else:
            try:
                third_component = Component.objects.filter(parent=subcomponent).order_by('order')[:1].get()
            except:
                third_component = None
        print("third_component_id: " + str(third_component_id))
        print("third_component: " + third_component.name)


        # considerations at component and subcomponent level
        considerations = ComponentConsideration.objects.filter(element=component).order_by('id')
        if subcomponent:
            # concatenate querysets same type
            considerations = considerations | ComponentConsideration.objects.filter(element=subcomponent).\
                order_by('id')
            if third_component:
                considerations = considerations | ComponentConsideration.objects.filter(element=third_component)


        # comments
        # TODO: create assessment components and change coding
        if third_component:
            comments = AssessmentComponentComment.objects.filter(element=third_component, assessment=assessment).\
                order_by('date_created')
        else:
            if subcomponent:
                comments = AssessmentComponentComment.objects.filter(element=subcomponent, assessment=assessment).\
                    order_by('date_created')
            else:
                comments = AssessmentComponentComment.objects.filter(element=component, assessment=assessment).\
                    order_by('date_created')

        # formset definition
        fs_char_field = modelformset_factory(AssessmentComponentQuestionCharField, max_num=1, exclude=[],
                                             form=AssessmentComponentQuestionCharFieldForm)
        fs_text_field = modelformset_factory(AssessmentComponentQuestionTextField, max_num=1, exclude=[],
                                             form=AssessmentComponentQuestionTextFieldForm)
        fs_select_field = modelformset_factory(AssessmentComponentQuestionSelectField, max_num=1, exclude=[],
                                               form=AssessmentComponentQuestionSelectFieldForm)

        if request.method == 'POST':
            fs_cf = fs_char_field(request.POST, request.FILES, prefix='fs_cf')
            fs_tf = fs_text_field(request.POST, request.FILES, prefix='fs_tf')
            fs_sf = fs_select_field(request.POST, request.FILES, prefix='fs_sf')

            if fs_cf and fs_cf.is_valid() and fs_tf and fs_tf.is_valid() and fs_sf and fs_sf.is_valid():

                if fs_cf and fs_cf.is_valid():
                    not_applicable_responses_treatment(fs_cf)
                    trace_updated_fields(fs_cf, person, assessment)
                    fs_cf.save()
                else:
                    print("fs_cf not informed or not valid!")
                    print(str(fs_cf.errors))
                    sys.stdout.flush()

                if fs_tf and fs_tf.is_valid():
                    not_applicable_responses_treatment(fs_tf)
                    trace_updated_fields(fs_tf, person, assessment)
                    fs_tf.save()
                else:
                    print("fs_tf not informed or not valid!")
                    print(str(fs_tf.errors))
                    print(str(fs_tf.errors))
                    sys.stdout.flush()

                if fs_sf and fs_sf.is_valid():
                    trace_updated_fields(fs_sf, person, assessment)
                    # treatment for user added choices ("please specify")
                    for f in fs_sf:
                        data = f.cleaned_data
                        try:
                            # add new choice to the list
                            # TODO: delete??
                            """
                            other_choice = data['other']
                            if other_choice != "":
                                print("other_choice: " + other_choice)
                                a_cid_other_tx = AssessmentCityIDChoicesOtherTx()
                                a_cid_other_tx.assessment = assessment
                                a_cid_other_tx.name = other_choice
                                a_cid_other_tx.save()
                                # add new selected choice
                                question = f.save(commit=False)
                                response = data['response']
                                response = response[:len(response)-1]
                                new_str = ", u'" + str(a_cid_other_tx.id) + "']"
                                response += new_str
                                question.response = response
                                question.save()
                            else:
                                f.save()
                            """
                            pass
                        except KeyError:
                            # n_a field not found
                            pass
                    # Not needed. Each form is saved individually
                    fs_sf.save()
                else:
                    print("fs_sf not informed or not valid!")
                    print(str(fs_sf.errors))
                    sys.stdout.flush()

                # navigate to next component
                url_to_redirect = "/component/" + assessment_id + "/"
                if subcomponent:
                    if subcomponent.next_one:
                        print("1.component: " + subcomponent.parent.name)
                        print("1.subcomponent: " + subcomponent.next_one.name)
                        url_to_redirect += str(subcomponent.parent.id) + "/" + str(subcomponent.next_one.id) + "/"
                    else:
                        if subcomponent.parent.next_one:
                            print("2.component: " + subcomponent.parent.next_one.name)
                            url_to_redirect += str(subcomponent.parent.next_one.id) + "/"
                        else:
                            print("3.component: " + subcomponent.parent.name)
                            url_to_redirect += str(subcomponent.parent.id) + "/"
                else:
                    """
                    print("4.component: " + component.next_one.name)
                    url_to_redirect += str(component.next_one.id) + "/"
                    """
                # print("url_to_redirect: " + url_to_redirect)
                return redirect(url_to_redirect, context_instance=RequestContext(request))
            else:
                # additional treatment of errors if needed
                if fs_cf:
                    print("fs_cf errors: " + str(fs_cf.errors))
                if fs_tf:
                    print("fs_tf errors: " + str(fs_tf.errors))
                if fs_sf:
                    print("fs_sf errors: " + str(fs_sf.errors))
                sys.stdout.flush()
        else:
            # formsets
            query_set = AssessmentComponentQuestionCharField.objects.filter(component=third_component).order_by('order')
            fs_cf = fs_char_field(queryset=query_set, prefix='fs_cf')

            query_set = AssessmentComponentQuestionTextField.objects.filter(component=third_component).order_by('order')
            fs_tf = fs_text_field(queryset=query_set, prefix='fs_tf')

            query_set = AssessmentComponentQuestionSelectField.objects.filter(component=third_component).order_by('order')
            fs_sf = fs_select_field(queryset=query_set, prefix='fs_sf')

        # return page
        template = loader.get_template(TEMPLATE_COMPONENTS_PAGE)
        context = RequestContext(request, {
            'fs_cf': fs_cf,
            'fs_tf': fs_tf,
            'fs_sf': fs_sf,
            'person': person,
            'left_elements': left_elements,
            'menu_elements': menu_elements,
            'menu_horizontal_elem_width': menu_horizontal_elem_width,
            'page': "city_id",
            'assessment': assessment,
            'section': component,
            'subsection': subcomponent,
            'third_component': third_component,
            'comments': comments,
            'considerations': considerations,
            'is_component': 'True',
        })
        return HttpResponse(template.render(context))
    except:
        if debug_is_on():
            raise
        else:
            return render_to_response(TEMPLATE_ERROR, {"error_description": sys.exc_info(), "crpt_url": CRPT_URL},
                                      context_instance=RequestContext(request))


@ensure_csrf_cookie
@login_required
def add_section_comment(request):
    """
    View to add comment to a section

    :param request:
    :return:
    """
    try:
        person = get_person(request)

        if request.method == "POST":
            # get values from form
            assessment_id = request.POST['assessment_id']
            section_id = request.POST['section_id']
            comment = request.POST['textComments']

            # get section and assessment
            section = CityIDSection.objects.get(id=section_id)
            assessment = Assessment.objects.get(id=assessment_id)
            # create comment
            my_comment = AssessmentCityIDSectionComment()
            my_comment.assessment = assessment
            my_comment.element = section
            my_comment.comment = comment
            my_comment.person = person
            my_comment.save()

            # trace action
            trace_action(TRACE_COMMENT, person, "User added comment in section: " + section.name)

            # send mail
            try:
                send_mail = request.POST['send_mail']
                t = Thread(target=send_comments_email, args=(my_comment.comment, section, person))
                t.start()
                # send_comments_email(my_comment.comment, section, person)
            except:
                # checkbox not set
                pass

            # redirect to section page
            url_to_redirect = "/city_id/" + assessment_id + "/"
            if section.parent:
                url_to_redirect += str(section.parent.id) + "/"
            url_to_redirect += str(section.id) + "/"

            return redirect(url_to_redirect, context_instance=RequestContext(request))
        else:
            raise Exception("GET call to add new section comment")
    except:
        if debug_is_on():
            raise
        else:
            return render_to_response(TEMPLATE_ERROR, {"error_description": sys.exc_info(), "crpt_url": CRPT_URL},
                                      context_instance=RequestContext(request))
