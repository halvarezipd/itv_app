from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin, LeafletGeoAdminMixin
from .models import AreaManager, MemberLocation, TeamMember


class MemberLocationInline(LeafletGeoAdminMixin, admin.StackedInline):
    model = MemberLocation


@admin.register(TeamMember)
class TeamMemberAdmin(LeafletGeoAdmin):
    list_display = ("team_member_name", "team_member_phone_number", "team_member_status", "team_member_is_active")
    readonly_fields = (
                        "team_member_name", "team_member_phone_number", "team_member_status", "team_member_is_active", "team_member_email",
                        "team_member_battery_level", "team_member_registration_status", "team_member_is_available", "team_member_last_updated_location_time",
                        "team_member_image", "team_member_image_thumbnail", "team_member_app_version", "team_member_app_id", "team_member_id", "team_member_has_network",
                        "team_member_last_updated_location_time_parsed",
                       )
    search_fields = ("team_member_name", "team_member_status")
    inlines = [MemberLocationInline]


@admin.register(MemberLocation)
class MemberLocationAdmin(LeafletGeoAdmin):
    list_display = ('team_member', 'team_member_location', 'team_member_location_time')
    search_fields = ("team_member__team_member_name",)
    default_zoom = 0


@admin.register(AreaManager)
class AreaManagerAdmin(admin.ModelAdmin):
    list_display = ('manager_username', 'manager_phone', 'manager_dispatcher_id')
    readonly_fields = ('manager_payroll_id', 'manager_dispatcher_id', 'manager_comp_code', 'manager_company_image')
