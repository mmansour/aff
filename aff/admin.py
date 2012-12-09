from aff.models import ActiveRegion, PropertyDescription, PropertyImage
from django.contrib import admin
from mezzanine.core.admin import DisplayableAdmin

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage

class ProperyDescriptionAdmin(DisplayableAdmin):

    fieldsets = [
        ("Title",                       {'fields': ['title']}),
        ("Published Date",              {'fields': ['publish_date']}),
        ("Published Status",            {'fields': ['status']}),
        ("Address",                     {'fields':['address1', 'city','state']}),
    ]

    inlines = [
        PropertyImageInline,
    ]


    list_display = ('title', 'city','state', 'user', 'publish_date', 'status')
    list_display_links = ('title',)
#    list_editable = ('is_order_closed',)
#    list_filter = ['user','is_order_closed', 'publish_date',]
#    search_fields = ['title',]
#    date_hierarchy = 'publish_date'


class ActiveRegionAdmin(admin.ModelAdmin):
    list_display = ('region','country',)
    list_display_links = ('region',)
#    list_editable = ('email_address',)


admin.site.register(PropertyDescription, ProperyDescriptionAdmin)
admin.site.register(ActiveRegion, ActiveRegionAdmin)
