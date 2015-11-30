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

class AssessmentVersionAdmin(admin.ModelAdmin):
    list_display = ('version', 'name', 'date_released')

admin.site.register(crpt201511.models.AssessmentVersion, AssessmentVersionAdmin)


class ElementAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')

admin.site.register(crpt201511.models.Element, ElementAdmin)


class CityIDStatementAdmin(admin.ModelAdmin):
    list_display = ('question', 'section')

admin.site.register(crpt201511.models.CityIDStatement, CityIDStatementAdmin)


class AssessmentCityIDResponseAdmin(admin.ModelAdmin):
    list_display = ('value', 'statement', 'assessment')

admin.site.register(crpt201511.models.AssessmentCityIDResponse, AssessmentCityIDResponseAdmin)