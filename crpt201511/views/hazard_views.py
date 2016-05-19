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
from crpt201511.forms import AssessmentHazardTypeForm
from crpt201511.utils.hazard_utils import *
from crpt201511.trace import *
from crpt201511.utils.mail_utils import *


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
        # check person has rights for the assessment.
        if not check_person_access_to_assessment(assessment, person):
            print("assessment: " + assessment.name)
            raise Exception('User has no permission to access this assessment')

        hazard_groups = HazardGroup.objects.all().order_by('id')
        nohg = len(hazard_groups)
        hg_width = 100 / nohg*2

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
        # check person has rights for the assessment.
        if not check_person_access_to_assessment(assessment, person):
            print("assessment: " + assessment.name)
            raise Exception('User has no permission to access this assessment')

        hazard_group = HazardGroup.objects.get(id=hg_id)
        hazard_types = HazardType.objects.filter(hazard_group=hazard_group).order_by('id')
        nohg = len(hazard_types)
        ht_width = 100 / nohg
        template = loader.get_template(TEMPLATE_HAZARDS_TYPES_PAGE)
        context = RequestContext(request, {
            'person': person,
            'assessment': assessment,
            'hazard_types': hazard_types,
            'ht_width': ht_width,
            'is_hazard_type': True,
            'hazard_group': hazard_group,
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
        # check person has rights for the assessment.
        if not check_person_access_to_assessment(assessment, person):
            print("assessment: " + assessment.name)
            raise Exception('User has no permission to access this assessment')

        # get hazard type, description and examples
        ht = HazardType.objects.get(id=ht_id)

        # get assessment hazard type
        a_h_t_list = AssessmentHazardType.objects.filter(hazard_type=ht, assessment=assessment).order_by('id')

        # considerations as list of subtypes. listed in template for each subtype
        h_sts = HazardSubtype.objects.filter(hazard_type=ht).order_by('id')
        considerations = HazardSubtypeFurtherExplanation.objects.filter(hazard_subtype__in=h_sts)

        # comments
        comments = AssessmentHazardComment.objects.filter(assessment_hazard_type__in=a_h_t_list).order_by('id')

        # formset definition
        fs = modelformset_factory(AssessmentHazardType, max_num=0, exclude=[], form=AssessmentHazardTypeForm)

        if request.method == 'POST':
            f_set = fs(request.POST, request.FILES)
            if f_set and f_set.is_valid():
                # save
                f_set.save()


                # process subtypes
                for f in f_set:
                    # all subtypes enabled = false
                    a_h_subtypes = AssessmentHazardSubtype.objects.filter(a_h_type_id=f.instance.id)
                    for elem in a_h_subtypes:
                        a_h_subtype = AssessmentHazardSubtype.objects.get(id=int(elem.id))
                        a_h_subtype.enabled = False
                        a_h_subtype.save()
                    # only selected enabled = true
                    a_h_subtypes_list = get_list_of_ids(f.instance.subtypes)
                    if len(a_h_subtypes_list) > 0:
                        for elem in a_h_subtypes_list:
                            a_h_subtype = AssessmentHazardSubtype.objects.get(id=int(elem))
                            a_h_subtype.enabled = True
                            a_h_subtype.save()




                # redirect to next page
                url_to_redirect = '/hazard_type_interrelations/' + assessment_id + SLASH + ht_id
                return redirect(url_to_redirect, context_instance=RequestContext(request))

            else:
                print(str(f_set.errors))
                sys.stdout.flush()

        else:
            query_set = a_h_t_list
            f_set = fs(queryset=query_set)


        # return page
        template = loader.get_template(TEMPLATE_HAZARDS_DETAIL_PAGE)
        context = RequestContext(request, {
            'person': person,
            'assessment': assessment,
            'selected': "HT_DETAIL",
            'ht': ht,
            'fs': f_set,
            'considerations': considerations,
            'comments': comments,
            'is_hazard_detail':True,
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
        # check person has rights for the assessment.
        if not check_person_access_to_assessment(assessment, person):
            print("assessment: " + assessment.name)
            raise Exception('User has no permission to access this assessment')

        # get hazard type, description and examples
        ht = HazardType.objects.get(id=ht_id)
        aht = AssessmentHazardType.objects.filter(assessment=assessment, hazard_type=ht)

        # considerations as list of subtypes. listed in template for each subtype
        considerations = HazardSubtype.objects.filter(hazard_type=ht).order_by('id')

        # comments
        comments = AssessmentHazardComment.objects.filter(assessment_hazard_type__in=aht).order_by('id')


        # formset definition
        fs_factory_causes = modelformset_factory(AssessmentHazardCause, max_num=0, exclude=[])
        fs_factory_consequences = modelformset_factory(AssessmentHazardConsequence, max_num=0, exclude=[])

        if request.method == 'POST':

            fs_causes = fs_factory_causes(request.POST, request.FILES, prefix='fs_causes')
            fs_consequences = fs_factory_consequences(request.POST, request.FILES, prefix='fs_consequences')

            if fs_causes and fs_causes.is_valid() and fs_consequences and fs_consequences.is_valid():
                fs_causes.save()
                fs_consequences.save()

                # redirect to next page
                url_to_redirect = '/hazard_type_impacts/' + assessment_id + SLASH + ht_id
                return redirect(url_to_redirect, context_instance=RequestContext(request))

            else:
                if fs_causes.errors:
                    print(str(fs_causes.errors))
                if fs_consequences.errors:
                    print(str(fs_consequences.errors))
                sys.stdout.flush()

        else:
            query_set = AssessmentHazardCause.objects.filter(a_h_type=aht).order_by('id')
            fs_causes = fs_factory_causes(queryset=query_set, prefix='fs_causes')
            query_set = AssessmentHazardConsequence.objects.filter(a_h_type=aht).order_by('id')
            fs_consequences = fs_factory_consequences(queryset=query_set, prefix='fs_consequences')

        # return page
        template = loader.get_template(TEMPLATE_HAZARDS_INTERRELATIONS_PAGE)
        context = RequestContext(request, {
            'person': person,
            'assessment': assessment,
            'selected': "HT_INTERRELATIONS",
            'ht': ht,
            'fs_causes': fs_causes,
            'fs_consequences': fs_consequences,
            'considerations': considerations,
            'comments': comments,
            'is_hazard_detail': True,
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
        # check person has rights for the assessment.
        if not check_person_access_to_assessment(assessment, person):
            print("assessment: " + assessment.name)
            raise Exception('User has no permission to access this assessment')

        # get hazard type, description and examples
        ht = HazardType.objects.get(id=ht_id)
        aht = AssessmentHazardType.objects.filter(assessment=assessment, hazard_type=ht)

        # considerations as list of subtypes. listed in template for each subtype
        considerations = HazardSubtype.objects.filter(hazard_type=ht).order_by('id')

        # comments
        comments = AssessmentHazardComment.objects.filter(assessment_hazard_type__in=aht).order_by('id')

        # formset definition
        fs = modelformset_factory(AssessmentElementImpact, max_num=0, exclude=[])

        if request.method == 'POST':

            f_set = fs(request.POST, request.FILES)
            if f_set and f_set.is_valid():
                f_set.save()

                # redirect to next page
                url_to_redirect = '/hazard_type_detail/' + assessment_id + SLASH + ht_id
                return redirect(url_to_redirect, context_instance=RequestContext(request))

            else:
                print(str(f_set.errors))
                sys.stdout.flush()

        else:
            query_set = AssessmentElementImpact.objects.filter(a_h_type=aht, assessment=assessment).order_by('id')
            f_set = fs(queryset=query_set)

        # return page
        template = loader.get_template(TEMPLATE_HAZARDS_IMPACTS_PAGE)
        context = RequestContext(request, {
            'person': person,
            'assessment': assessment,
            'fs': f_set,
            'selected': "HT_IMPACTS",
            'ht': ht,
            'considerations': considerations,
            'comments': comments,
            'is_hazard_detail': True,
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
def hazards_selected(request, assessment_id):
    """
    View for hazards selected diagram
    :param request:
    :param assessment_id:
    :return:
    """
    try:
        person = get_person(request)
        assessment = Assessment.objects.get(id=assessment_id)
        # check person has rights for the assessment.
        if not check_person_access_to_assessment(assessment, person):
            print("assessment: " + assessment.name)
            raise Exception('User has no permission to access this assessment')

        # get hazards selected
        hs_list = get_hazards_selected(assessment)

        print("hazards_selected length: " + str(len(hs_list)))
        sys.stdout.flush()

        # return page
        template = loader.get_template(TEMPLATE_HAZARDS_SELECTED_PAGE)
        context = RequestContext(request, {
            'person': person,
            'assessment': assessment,
            'selected': "HAZARDS_SELECTED",
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
def hazards_relations(request, assessment_id):
    """
    View for hazards relations diagram
    :param request:
    :param assessment_id:
    :return:
    """
    try:
        person = get_person(request)
        assessment = Assessment.objects.get(id=assessment_id)
        # check person has rights for the assessment.
        if not check_person_access_to_assessment(assessment, person):
            print("assessment: " + assessment.name)
            raise Exception('User has no permission to access this assessment')

        # get hazards selected
        str_causes_all = ''
        for hs in AssessmentHazardType.objects.filter(assessment=assessment):

            causes = AssessmentHazardCause.objects.filter(a_h_type=hs)
            consequences = AssessmentHazardConsequence.objects.filter(a_h_type=hs, enabled=True)

            str_causes_base = '{"name":"'+hs.hazard_type.hazard_group.name+'.'+hs.hazard_type.name+\
                     '","children":{"size":1200,"imports":['
            str_causes = ''
            for c in causes:
                str_causes += '"'+c.a_h_type_cause.hazard_type.hazard_group.name+'.'+c.a_h_type_cause.hazard_type.name+'",'

            str_causes = str_causes[:len(str_causes)-1]
            str_causes_hs = str_causes_base + str_causes + ']}}'

            str_causes_all += str_causes_hs + ','

        #if str_causes_all[len(str_causes_all)-1:len(str_causes_all)] == ',':
        #    str_causes_all = str_causes_all[:len(str_causes_all)-1]
        str_causes_all = str('[' + str_causes_all + ']')

        print("str_causes_all: " + str(str_causes_all))
        sys.stdout.flush()


        # return page
        template = loader.get_template(TEMPLATE_HAZARDS_RELATIONS_PAGE)
        context = RequestContext(request, {
            'person': person,
            'assessment': assessment,
            'selected': "HAZARDS_RELATIONS",
            'str_causes_all':str_causes_all,
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
def add_hazard_type_comment(request):
    """
    View to add comment to a hazard type

    :param request:
    :return:
    """
    try:
        person = get_person(request)

        if request.method == "POST":
            # get values from form
            assessment_id = request.POST['assessment_id']
            try:
                hazard_type_id = request.POST['hazard_type_id']
            except:
                hazard_type_id = None
            comment = request.POST['textComments']
            try:
                destination = request.POST['destination']
            except:
                destination = "hazard_type_detail"

            # get section and assessment
            assessment = Assessment.objects.get(id=assessment_id)
            hazard_type = HazardType.objects.get(id=hazard_type_id)
            a_hazard_type = AssessmentHazardType.objects.get(hazard_type=hazard_type, assessment=assessment)
            # create comment
            my_comment = AssessmentHazardComment()
            my_comment.assessment_hazard_type = a_hazard_type
            my_comment.comment = comment
            my_comment.person = person
            my_comment.save()

            # trace action
            trace_action(TRACE_COMMENT, person, "User added comment in assessment_hazard_type: " + hazard_type.name)

            # send mail
            try:
                send_mail = request.POST['send_mail']
                t = Thread(target=send_comments_email, args=(my_comment.comment, "Hazard Type: " + hazard_type.name, person))
                t.start()
                # send_comments_email(my_comment.comment, section, person)
            except:
                # checkbox not set
                pass

            # redirect to hazard_type page
            url_to_redirect = SLASH + str(destination) + SLASH + str(assessment_id) + SLASH + str(hazard_type.id) + SLASH

            return redirect(url_to_redirect, context_instance=RequestContext(request))
        else:
            raise Exception("GET call to add new section comment")
    except:
        if debug_is_on():
            raise
        else:
            return render_to_response(TEMPLATE_ERROR, {"error_description": sys.exc_info(), "crpt_url": CRPT_URL},
                                      context_instance=RequestContext(request))
