from django.contrib import admin

import crpt201511.models

admin.site.register(crpt201511.models.TraceAction)
admin.site.register(crpt201511.models.City)
admin.site.register(crpt201511.models.Role)
admin.site.register(crpt201511.models.Person)
admin.site.register(crpt201511.models.Dimension)
admin.site.register(crpt201511.models.HazardCategory)
admin.site.register(crpt201511.models.Hazard)
admin.site.register(crpt201511.models.MoVType)
admin.site.register(crpt201511.models.CityIDSection)
admin.site.register(crpt201511.models.CityIDQuestionCharField)
admin.site.register(crpt201511.models.CityIDQuestionTextField)
admin.site.register(crpt201511.models.CityIDQuestionUploadField)
admin.site.register(crpt201511.models.AssessmentCityIDQuestionCharField)
admin.site.register(crpt201511.models.AssessmentCityIDQuestionTextField)
admin.site.register(crpt201511.models.AssessmentCityIDQuestionUploadField)

class AssessmentVersionAdmin(admin.ModelAdmin):
    list_display = ('version', 'name', 'date_released')

admin.site.register(crpt201511.models.AssessmentVersion, AssessmentVersionAdmin)


class ElementAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')

admin.site.register(crpt201511.models.Element, ElementAdmin)





admin.site.register(crpt201511.models.QuestionType1)
admin.site.register(crpt201511.models.QuestionType2)
admin.site.register(crpt201511.models.QuestionType3)