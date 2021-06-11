from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin, LeafletGeoAdminMixin
from .models import Job, JobPhase


class JobPhaseInlineAdmin(LeafletGeoAdminMixin, admin.StackedInline):
    model = JobPhase


@admin.register(Job)
class JobAdmin(LeafletGeoAdmin):
    list_display = ("job_name", "job_city")
    readonly_fields = ("job_name", "job_id", "job_address", "job_city", "job_started", "job_app_end_date",
                       "job_area_manager")
    search_fields = ("job_name", "job_area_manager")
    inlines = [JobPhaseInlineAdmin]


@admin.register(JobPhase)
class JobPhaseAdmin(LeafletGeoAdmin):
    list_display = ("phase_name", "phase_number", "phase_location")
    readonly_fields = ("phase_job_name",)
