import json
import requests
import os
from datetime import date
from django.contrib.gis.db.models.functions import AsGeoJSON

from django.contrib.gis.geos import fromstr

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itv_app.settings')

django.setup()

from team_members.models import TeamMember, MemberLocation, AreaManager
from jobs.models import Job, JobPhase

today_date = date.today()
login_url = "https://api.infinityteamview.com/user_login"  # for login
job_fleet_url = "https://api.infinityteamview.com/get_task_view_and_fleet_details"
area_manager_url = "https://api.infinityteamview.com/view_all_dispatcher"

login_headers = {  # headers for url
    b"User-Agent": b"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40",
    b"Host": b"api.infinityteamview.com",
    b"Accept": b'application/json, text/plain, */*',
    b"Referer": b"https://dashboard.infinityteamview.com/",
    b"Content-Type": b"application/x-www-form-urlencoded",
    b"Content-Length": b"90",
    b"Origin": b"https://dashboard.infinityteamview.com",
    b"DNT": b"1",
    b"Connection": b"keep-alive",

}

job_fleet_headers = {  # Headers for Job_and_fleet_url
    b"Host": b"api.infinityteamview.com",
    b"User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 "
        "Safari/537.36 Edg/84.0.522.40",
    b"Accept": b"application/json, text/plain, */*",
    b"Accept-Language": b"null",
    b"Accept-Encoding": b"gzip, deflate, br",
    b"Referer": b"https://dashboard.infinityteamview.com/",
    b"Content-Type": b"application/x-www-form-urlencoded",
    b"Content-Length": b"160",
    b"Origin": b"https://dashboard.infinityteamview.com",
    b"DNT": b"1",
    b"Connection": b"keep-alive",
    b"Sec-Fetch-Dest": b"empty",
    b"Sec-Fetch-Mode": b"cors",
    b"Sec-Fetch-Site": b"same-site"
}

area_manager_headers = {b'accept': b'application/json, text/plain, */*', b'accept-language': b'en',
                        b'content-type': b'application/x-www-form-urlencoded',
                        b'sec-fetch-dest': b'empty', 'sec-fetch-mode': b'cors', b'sec-fetch-site': b'same-site',
                        b'sec-gpc': b'1',
                        b'referrer': b'https://dashboard.infinityteamview.com/', b'referrerPolicy': b'origin',
                        b'mode': b'cors', b'credentials': b'omit'}

login_data = {  # data for url
    b"email": b"appadmin@infinityplumbingdesigns.com",
    b"password": b"sabinelongingskips",
    b"timezone": b"480",
    b"gzip": b"1",
}

# data for fleet url
job_fleet_data = {
    b"user_id": b"1",
    b"date": today_date,
    b"today": b"1",
    b"ignore_fleets": b"0",
    b"get_completed_tasks": b"1",
    b"is_offline": b"1",
    b"team_id": b"0",
}


def get_login():  # Logs in and adds access token to the
    r = requests.post(login_url, headers=login_headers, data=login_data)
    response = r.content
    parsed = json.loads(response)
    return parsed


def get_data(_url=job_fleet_url, _header=job_fleet_headers, _data=job_fleet_data):
    if 'access_token' in _data:
        r = requests.post(_url, headers=_header, data=_data)
        response = r.content
        parsed = json.loads(response)
    else:
        login = get_login()
        _data['access_token'] = login["data"]["access_token"]
        r = requests.post(_url, headers=_header, data=_data)
        response = r.content
        parsed = json.loads(response)
    return parsed


def get_area_managers(url=area_manager_url, headers=area_manager_headers):
    data = dict()
    data["access_token"] = str(get_login()["data"]["access_token"])
    r = requests.post(url, headers=headers, data=data).json()["data"]
    return r


def get_fleets():
    data = get_data()
    fleets = data["data"]["teams"]["0"]["fleets"]
    return fleets


def get_jobs():
    data = get_data()
    jobs = data["data"]["teams"]["0"]["jobs"]
    return jobs


def load_jobs_initial():
    jobs = get_jobs()
    for job in jobs:
        # store job info into variables for assignments
        latitude = job["jobs"][0]["latitude"]
        longitude = job["jobs"][0]["longitude"]
        itv_job_manager_picture = job["jobs"][0]["company_image"]
        job_id = job["jobs"][0]["hash_job_id"][:3]
        job_phase_name = job["jobs"][0]["job_name"]
        job_location = fromstr(f'POINT({longitude} {latitude})', srid=4326)  # setup variable to save location
        job_address = job["jobs"][0]["address"]
        job_city = job["jobs"][0]["city_name"]
        job_started = job["jobs"][0]["job_pickup_datetime"]
        job_app_end_date = job["jobs"][0]["job_delivery_datetime"]
        job_name = job["jobs"][0]["job_name"].upper()

        # Clean the name of the job
        if "PH" in job_name:
            new_job_name = job_name[:job_name.find(" PH")]
        elif "BUILDOUT" in job_name:
            new_job_name = job_name[:job_name.find(" BUILDOUT")]
        elif "MODEL" in job_name:
            new_job_name = job_name[:job_name.find(" MODEL")]
        else:
            new_job_name = job_name

        # If job id smaller than 3 digits save it as id otherwise just the digits after the first three letter
        if len(job["jobs"][0]["hash_job_id"]) > 3:
            job_number = job["jobs"][0]["hash_job_id"][3:]
        else:
            job_number = job["jobs"][0]["hash_job_id"]

        # try to get the job if it exists and create a phase
        try:
            add_job_phase = Job.objects.get(job_id=job_id)
            new_phase = JobPhase(
                phase_job_name=add_job_phase,
                phase_name=job_phase_name,
                phase_number=job_number,
                phase_location=job_location,
            )
            new_phase.save()
            print(f"New Phase Added to: {add_job_phase.job_name}")
            # if the job doesnt exist create it and add the phase
        except Job.DoesNotExist:
            job_area_manager = AreaManager.objects.get(manager_company_image=itv_job_manager_picture)
            new_job = Job(
                job_name=new_job_name,
                job_id=job_id,
                job_address=job_address,
                job_city=job_city,
                job_started=job_started,
                job_app_end_date=job_app_end_date,
                job_location=job_location,
                job_area_manager=job_area_manager,
            )
            new_job.save()
            create_phase = JobPhase(
                phase_job_name=new_job,
                phase_name=job_phase_name,
                phase_number=job_number,
                phase_location=job_location
            )
            create_phase.save()
            print(f"New Job Created: {new_job_name}, New Phase Created: {job_phase_name}")


def load_managers():
    area_managers = get_area_managers()
    for manager in area_managers:
        new_manager = AreaManager(
            manager_payroll_id=manager["payroll_id"],
            manager_dispatcher_id=manager["dispatcher_id"],
            manager_username=manager["username"],
            manager_first_name=manager["first_name"],
            manager_last_name=manager["last_name"],
            manager_email=manager["email"],
            manager_phone=manager["phone"],
            manager_comp_code=manager["username"],
            manager_company_image=manager["company_image"],
        )
        new_manager.save()
        print(f"Created: {new_manager.manager_username}")
    print("Finished")


def load_fleets_initial():
    fleets = get_fleets()
    for key, team_member in fleets.items():
        update_member = TeamMember(
            team_member_name=team_member["fleet_name"],
            team_member_phone_number=team_member["phone"],
            team_member_email=team_member["email"],
            team_member_status=team_member["status"],
            team_member_battery_level=team_member["battery_level"],
            team_member_registration_status=team_member["registration_status"],
            team_member_is_active=team_member["is_active"],
            team_member_is_available=team_member["is_available"],
            team_member_last_updated_location_time=team_member["last_updated_location_time"],
            team_member_image=team_member["fleet_image"],
            team_member_image_thumbnail=team_member["fleet_thumb_image"],
            team_member_app_version=team_member["store_version"],
            team_member_app_id=team_member["device_token"],
            team_member_id=team_member["fleet_id"],
            team_member_has_network=team_member["has_network"],
        )
        update_member.save()
        if team_member["longitude"] is None or team_member["latitude"] is None:
            continue
        new_location = MemberLocation()
        new_location.team_member = update_member
        latitude = team_member["latitude"]
        longitude = team_member["longitude"]
        location = fromstr(f'POINT({longitude} {latitude})', srid=4326)
        new_location.team_member_location = location
        new_location.save()
    print("Done")


def update_fleets():
    fleets = get_fleets()
    updated = 0
    not_updated = 0
    for key, team_member in fleets.items():
        update_member = TeamMember.objects.get(team_member_id=team_member["fleet_id"])
        try:
            latest_location_json = json.loads(
                MemberLocation.objects.annotate(json=AsGeoJSON('team_member_location')).filter(
                    team_member=update_member).last().json)
        except AttributeError:
            continue
        latest_longitude = str(latest_location_json["coordinates"][0])
        latest_latitude = str(latest_location_json["coordinates"][1])

        new_latitude = str(team_member["latitude"])[:11]
        new_longitude = str(team_member["longitude"])[:13]

        update_member.team_member_status = team_member["status"]
        update_member.team_member_battery_level = team_member["battery_level"]
        update_member.team_member_registration_status = team_member["registration_status"]
        update_member.team_member_is_active = team_member["is_active"]
        update_member.team_member_is_available = team_member["is_available"]
        update_member.team_member_last_updated_location_time = team_member["last_updated_location_time"]
        update_member.team_member_has_network = team_member["has_network"]
        update_member.save()
        print(f"Updated: {update_member.team_member_name}")

        if latest_latitude in new_latitude or latest_longitude in new_longitude:
            print("locations are the same, continuing.")
            not_updated += 1
            continue

        new_location = MemberLocation()
        new_location.team_member = update_member
        if new_longitude != None or new_latitude != None:
            new_location_point = fromstr(f'POINT({new_longitude} {new_latitude})', srid=4326)
        else:
            continue
        new_location.team_member_location = new_location_point
        new_location.save()
        print(f"Updated: {update_member.team_member_name}'s Location Updated")
        updated += 1
    print("Updated Locations: " + str(updated))
    print("Locations Not Updated: " + str(not_updated))


def init_db():
    load_managers()
    load_fleets_initial()
    load_jobs_initial()
