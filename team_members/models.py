from django.contrib.gis.db import models


class AreaManager(models.Model):
    manager_dispatcher_id = models.CharField(max_length=20,null=True, blank=True)
    manager_payroll_id = models.CharField(max_length=20,null=True, blank=True)
    manager_username = models.CharField(max_length=20,null=True, blank=True)
    manager_first_name = models.CharField(max_length=20,null=True, blank=True)
    manager_last_name = models.CharField(max_length=20,null=True, blank=True)
    manager_email = models.CharField(max_length=100,null=True, blank=True)
    manager_phone = models.CharField(max_length=20,null=True, blank=True)
    manager_comp_code = models.CharField(max_length=20,null=True, blank=True)
    manager_company_image = models.CharField(max_length=200,null=True, blank=True)
    
    def __str__(self) -> str:
        return self.manager_username
    


class TeamMember(models.Model):
    team_member_name = models.CharField(max_length=200)
    team_member_phone_number = models.CharField(max_length=20,null=True, blank=True)
    team_member_email = models.CharField(max_length=250,null=True, blank=True)
    team_member_status = models.IntegerField(null=True, blank=True)
    team_member_battery_level = models.IntegerField(null=True, blank=True)
    team_member_registration_status = models.IntegerField(null=True, blank=True)
    team_member_is_active = models.IntegerField(null=True, blank=True)
    team_member_is_available = models.IntegerField(null=True, blank=True)
    team_member_last_updated_location_time = models.CharField(max_length=250,null=True, blank=True)
    team_member_last_updated_location_time_parsed = models.DateTimeField(max_length=250,null=True, blank=True)
    team_member_image = models.CharField(max_length=200,null=True, blank=True)
    team_member_image_thumbnail = models.CharField(max_length=250,null=True, blank=True)
    team_member_app_version = models.CharField(max_length=15,null=True, blank=True)
    team_member_app_id = models.CharField(max_length=200,null=True, blank=True)
    team_member_id = models.IntegerField(unique=True,null=True, blank=True)
    team_member_has_network = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.team_member_name


class MemberLocation(models.Model):
    team_member = models.ForeignKey('TeamMember', on_delete=models.CASCADE)
    team_member_location_time = models.DateTimeField(auto_now_add=True)
    team_member_location = models.PointField()

    def __str__(self):
        return str(self.team_member_location_time)
