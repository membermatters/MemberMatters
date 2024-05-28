from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.views import APIView
from constance import config
from .models import SpaceAPI, SpaceAPISensor, SpaceAPISensorProperties
from profile.models import Profile
from api_general.models import SiteSession
from otel import tracer
import json


class SpaceDirectoryStatus(APIView):
    """Generates a spaceapi compliant status message if enabled."""

    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        with tracer.start_as_current_span("get_spaceapi_details"):
            if not config.ENABLE_SPACE_DIRECTORY:
                return Response(
                    "Space Directory is not enabled on this server.",
                    status=status.HTTP_404_NOT_FOUND,
                )

            else:
                spaceapi = {
                    "space": config.SITE_OWNER,
                    "logo": config.SITE_LOGO,
                    "url": config.MAIN_SITE_URL,
                    "contact": {
                        "email": config.SPACE_DIRECTORY_CONTACT_EMAIL,
                        "twitter": config.SPACE_DIRECTORY_CONTACT_TWITTER,
                        "phone": config.SPACE_DIRECTORY_CONTACT_PHONE,
                        "facebook": config.SPACE_DIRECTORY_CONTACT_FACEBOOK,
                    },
                    "spacefed": {
                        "spacenet": config.SPACE_DIRECTORY_FED_SPACENET,
                        "spacesaml": config.SPACE_DIRECTORY_FED_SPACESAML,
                        "spacephone": config.SPACE_DIRECTORY_FED_SPACEPHONE,
                    },
                    "projects": json.loads(config.SPACE_DIRECTORY_PROJECTS),
                    "issue_report_channels": ["email"],
                }

                # Get the default data
                spaceapi_data = SpaceAPI.objects.get()

                # Get a list of all the sensors
                spaceapi_sensors = SpaceAPISensor.objects.all()

                # Create an empty dict to add the sensor data to
                sensor_data = {}

                # Iterate over the sensors and update the dict as appropriate
                for sensor in spaceapi_sensors:
                    sensor_details = {}
                    # Do we already have a sensor of this type? If not, create it now
                    if sensor.sensor_type not in sensor_data:
                        sensor_data[sensor.sensor_type] = []

                    ## Setup the basic details
                    sensor_details = {
                        "name": sensor.name,
                        "description": sensor.description or "",
                        "location": sensor.location,
                    }

                    ### Do we have properties? If so, let's add them
                    if len(sensor.properties.all()) > 0:
                        sensor_details["properties"] = {}
                        for prop in sensor.properties.all():
                            properties = {
                                prop.name: {"value": prop.value, "unit": prop.unit}
                            }
                            sensor_details["properties"].update(properties)
                    else:
                        sensor_details.update(
                            {"value": sensor.value, "unit": sensor.unit}
                        )

                    sensor_data[sensor.sensor_type].append(sensor_details)

                ## Add the user count and members on site count to the sensors
                spaceapi_user_count = (
                    Profile.objects.all().filter(state="active").count()
                )
                spaceapi_members_on_site = SiteSession.objects.filter(
                    signout_date=None
                ).order_by("-signin_date")

                sensor_data["total_member_count"] = [{"value": spaceapi_user_count}]

                sensor_data["people_now_present"] = [
                    {"value": spaceapi_members_on_site.count()}
                ]

                # Is the camera array empty? If not, add them
                if not config.SPACE_DIRECTORY_CAMS:
                    spaceapi["cameras"] = config.SPACE_DIRECTORY_CAMS

                # Set the STATE part of the schema, the icons, and the schema version
                spaceapi["state"] = {
                    "open": spaceapi_data.space_is_open,
                    "message": spaceapi_data.space_message,
                    "lastchange": spaceapi_data.status_last_change.timestamp(),
                }
                spaceapi["icon"] = {
                    "open": config.SPACE_DIRECTORY_ICON_OPEN,
                    "closed": config.SPACE_DIRECTORY_ICON_CLOSED,
                }
                spaceapi["api_compatibility"] = ["14"]

                ## Add the sensor data to the main body of the schema
                spaceapi["sensors"] = sensor_data

                ## Add the location data based on the values in Constance
                spaceapi["location"] = {
                    "address": config.SPACE_DIRECTORY_LOCATION_ADDRESS,
                    "lat": config.SPACE_DIRECTORY_LOCATION_LAT,
                    "lon": config.SPACE_DIRECTORY_LOCATION_LON,
                }

                # Return the JSON document
                return Response(spaceapi)


class SpaceDirectoryUpdate(APIView):
    """Allows authenticated users to update the SpaceAPI information"""

    permission_classes = (permissions.IsAdminUser | HasAPIKey,)

    def post(self, request):
        # Get the current state of the space
        current_status = SpaceAPI.objects.get()

        ## Do we need to update the open/closed status
        if "is_open" in request.data:
            current_status.space_is_open = request.data["is_open"]

        ## Do we need to update the message?
        if "message" in request.data:
            current_status.space_message = request.data["message"]

        ## Do we have any sensor data?
        if "sensors" in request.data:
            for sensor in request.data["sensors"]:
                ### See if we have an existing sensor, if we do, update it,
                ### if we don't, create it.
                try:
                    current_sensor = (
                        SpaceAPISensor.objects.all().filter(name=sensor["name"]).first()
                    )
                    print(f"Found sensor: {current_sensor}")
                    if "type" in sensor:
                        current_sensor.sensor_type = sensor["type"]
                    if "value" in sensor:
                        current_sensor.value = sensor["value"]
                    if "unit" in sensor:
                        current_sensor.unit = sensor["unit"]
                    if "location" in sensor:
                        current_sensor.location = sensor["location"]
                    if "description" in sensor:
                        current_sensor.description = sensor["description"]

                    if "properties" in sensor:
                        for prop in sensor["properties"]:
                            #### Does the property exist? If so, update,
                            #### if not, create
                            try:
                                current_prop = SpaceAPISensorProperties.objects.filter(
                                    name=prop["name"], sensor_id=current_sensor
                                ).get()
                                print(f"Found property: {current_prop}")
                                if "name" in prop:
                                    current_prop.name = prop["name"]
                                if "value" in prop:
                                    current_prop.value = prop["value"]
                                if "unit" in prop:
                                    current_prop.unit = prop["unit"]
                                current_prop.save()
                            except:
                                new_prop = SpaceAPISensorProperties()
                                new_prop.name = prop["name"]
                                new_prop.value = prop["value"]
                                new_prop.unit = prop["unit"]
                                new_prop.sensor_id = current_sensor
                                new_prop.save()

                    current_sensor.save()
                except Exception as e:
                    new_sensor = SpaceAPISensor()
                    new_sensor.sensor_type = sensor["type"]
                    new_sensor.name = sensor["name"]
                    if "value" in sensor:
                        new_sensor.value = sensor["value"]
                    if "unit" in sensor:
                        new_sensor.unit = sensor["unit"]
                    new_sensor.location = sensor["location"]
                    new_sensor.description = sensor["description"]
                    new_sensor.save()

                    if "properties" in sensor:
                        ## This is a new sensor, we will always want to create the properties
                        for prop in sensor["properties"]:
                            new_prop = SpaceAPISensorProperties()
                            new_prop.name = prop["name"]
                            new_prop.value = prop["value"]
                            new_prop.unit = prop["unit"]
                            new_prop.sensor_id = new_sensor
                            new_prop.save()

        current_status.save()

        return Response()
