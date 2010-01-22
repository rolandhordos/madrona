from django.contrib import admin
from nc_mlpa.layers.models import EcotrustLayerList


class EcotrustLayerListAdmin(admin.ModelAdmin):
    list_display = ('kml', 'active', 'creation_date',)
    
admin.site.register(EcotrustLayerList, EcotrustLayerListAdmin)
