from django.contrib.gis.db import models


class Job(models.Model):
    job_name = models.CharField(max_length=50)
    job_id = models.CharField(max_length=10, unique=True)
    job_address = models.CharField(max_length=150,blank=True, null=True)
    job_city = models.CharField(max_length=50,blank=True, null=True)
    job_started = models.DateTimeField(blank=True, null=True)
    job_app_end_date = models.DateTimeField(blank=True, null=True)
    job_area_manager = models.CharField(max_length=150,blank=True, null=True)
    job_location = models.PointField()
    
    def __str__(self) -> str:
        return self.job_name


class JobPhase(models.Model):
    phase_job_name = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="phases")
    phase_name = models.CharField(max_length=100, blank=True, null=True)
    phase_number = models.CharField(max_length=10, blank=True, null=True)
    phase_location = models.PointField()
    
    def __str__(self) -> str:
        return self.phase_name
