from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from constance import config
from .models import SpaceAPI, SpaceAPISensor, SpaceAPISensorProperties
import json


class SpaceDirectoryStatus(APIView):
    """Generates a spaceapi compliant status message if enabled."""

    permission_classes = (permissions.AllowAny,)

    def get(self, request):
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

            spaceapi_data = SpaceAPI.objects.get()

            spaceapi_sensors = SpaceAPISensor.objects.all()

            sensor_data = {}

            for sensor in spaceapi_sensors:
                sensor_details = {}
                if sensor.sensor_type not in sensor_data:
                    sensor_data[sensor.sensor_type] = []
                sensor_details = {
                    "name": sensor.name,
                    "description": sensor.description,
                    "location": sensor.location,
                    "properties": {},
                }
                if len(sensor.properties.all()) > 0:
                    for prop in sensor.properties.all():
                        properties = {
                            prop.name: {"value": prop.value, "unit": prop.unit}
                        }
                        sensor_details["properties"].update(properties)
                else:
                    sensor_details.update({"value": sensor.value, "unit": sensor.unit})

                sensor_data[sensor.sensor_type].append(sensor_details)

            if not config.SPACE_DIRECTORY_CAMS:
                spaceapi["cameras"] = config.SPACE_DIRECTORY_CAMS

            spaceapi["state"] = {
                "open": spaceapi_data.space_is_open,
                "message": spaceapi_data.space_message,
                "lastchange": spaceapi_data.status_last_change.timestamp(),
            }
            spaceapi["icon"] = {
                "open": config.SPACE_DIRECTORY_ICON_OPEN,
                "closed": config.SPACE_DIRECTORY_ICON_CLOSED,
            }
            spaceapi["api_compatibility"] = ["0.14"]

            spaceapi["sensors"] = sensor_data

            spaceapi["location"] = {
                "address": config.SPACE_DIRECTORY_LOCATION_ADDRESS,
                "lat": config.SPACE_DIRECTORY_LOCATION_LAT,
                "lon": config.SPACE_DIRECTORY_LOCATION_LON,
            }

            return Response(spaceapi)


class SpaceDirectoryUpdate(APIView):

    permissions_classes = permissions.IsAuthenticated

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
                    print(e)
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
