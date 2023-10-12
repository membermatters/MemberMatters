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
