# Space Directory

The Space Directory functionality is provided via the [SpaceAPI](https://spaceapi.io) format.

## Reading the data

Any system can read the current information about the space by calling `https://<your_membermatters_installation>/api/spacedirectory/`.

By default, this returns the following data:

| Name | Description | Configuration Location |
|------|-------------|------------------------|
| space| The name of the space | Constance Config (Django Admin pages) |
| logo | The uri of the space logo | Constance Config (Django Admin Pages)|
| url  | The URL of the membermatters installation | Django Base URL |
| contact | Contact information, including email and various social media handles | Constance Config (Django Admin Pages)|
| spacefed | Details of whether the Federated Hackspace Authentication service is running | Constance Config (Django Admin Pages)|
| projects | A list of projects that the space is involved in | Constance Config (Django Admin Pages)|
| issue_report_channels | What's the best way to report an issue? |  Constance Config (Django Admin Pages)|
| state | Is the state open or closed, and what message should we display? | Dynamic (Django Admin or API Endpoint) |
| icon | An icon for each of "open" and "closed" |  Constance Config (Django Admin Pages)|
| api_compatibility | The version of the [SpaceAPI](https://spaceapi.io) that we are compatible with (can be multiple values) |  Hard-coded based on Member Matters release version |
| sensors | A dictionary of sensor data (and associated properties where relevant) as described in the [SpaceAPI JSON Schema documentation](https://spaceapi.io/docs/#schema-key-sensors) | Dynamic (Django Admin or API Endpoint) |
| location | The physical location of the space including latitude and longitude | Constance Config (Django Admin Pages)|

The data is returned as a JSON document.

For tools that can help you interact with the data to display your current state on your homepage etc, visit the [SpaceAPI Tools](https://spaceapi.io/how-to-use/) page and have a play!

## Updating the data

For anything in table above that is marked as "dynamic", you can update that information via the API.

Simply `POST` a JSON document to `https://<your_membermatters_installation>/api/spacedirectory/update` as an authenticated user, and the relevant fields will be updated.

### Updating the status and the message

Let's say you're opening the space and you want to ensure that everyone knows it's an "Open Night" (i.e. general public are welcome, not just members).

You can do this with the following command:

```bash
curl -X POST -d 'username=<myuser>&password=<mypass>' \
    'https://<your_membermatters_installation/api/token' # Use the output of this command for the next one


curl -X POST -H 'Authorization: Token <response from above>' \
    -d '{"is_open": true, "message": "Open Night TONIGHT! All Welcome between 1800hrs and 2300hrs"}' \
    https://<your_membermatters_installation>/api/spacedirectory/update
```

### Adding Sensor Data

[Sensors](https://spaceapi.io/docs/#schema-key-sensors) are a really cool part of the SpaceAPI schema, as it allows you to publish all kinds of things from how many drinks are still in the fridge through to environment readings such as temperature, windspeed, and humidity.

By default, MemberMatters exposes the total number of active members and how many have "signed in" to the space, however you can add your own sensors as long as they conform to the appropriate type.

To update a sensor or property value, you just need to POST the appropriate JSON to `https://<your_membermatters_installation>/api/spacedirectory/update` as laid out below.

**NOTE**: If a sensor or property is missing from the database then it will be created.  If it exists but the value is not included or changed, it will not be updated.

#### Sensors *without* properties

Many of the sensors do not have any extra properties.  Updating these is simple, as you just need to send a JSON array of dicts with the correct fields filled out:

```json
{
    "sensors": [
        { 
            "type": "temperature",
            "name": "test_sensor",
            "location": "default",
            "description": "This is a sensor",
            "unit": "°C",
            "value": 21.0
        }
    ]
}
```

Want to update more than one sensor at a time? No worries, just add to the array:

```json
{
    "sensors": [
        { 
            "type": "temperature",
            "name": "test_sensor",
            "location": "default",
            "description": "This is a sensor",
            "unit": "°C",
            "value": 21.0
        },
        { 
            "type": "humidity",
            "name": "test_sensor",
            "location": "default",
            "description": "This is a sensor",
            "unit": "%H",
            "value": 45.0
        }
    ]
}
```

#### Sensors *with* properties

For those sensors that do have properties, only a few extra fields are required:

```json
{
    "sensors": [
        { 
            "type": "wind",
            "name": "wind_sensor_01",
            "location": "The Roof",
            "description": "A weather station",
            "properties": [
                {
                    "name": "gust",
                    "unit": "m/s",
                    "speed": 5.0
                }
            ]
        }
    ]
}
```

As with the sensors, additional properties can be created by adding more dictionaries to the properties array:


```json
{
    "sensors": [
        { 
            "type": "wind",
            "name": "wind_sensor_01",
            "location": "The Roof",
            "description": "A weather station",
            "properties": [
                {
                    "name": "speed",
                    "unit": "m/s",
                    "speed": 5.0
                },
                {
                    "name": "gust",
                    "unit": "m/s",
                    "speed": 9.0
                }
            ]
        }
    ]
}
```

### A full example

The following JSON updates the space status to "Open", sets a message advising that there is a workshop running that evening, and sets the values for various sensors:

```json

{   "is_open": true,
    "message": "Soldering workshop tonight - 8pm to 10pm"
    "sensors": [
        { 
            "type": "temperature",
            "name": "test_sensor",
            "location": "default",
            "description": "This is a sensor",
            "unit": "°C",
            "value": 21.0
        },
        { 
            "type": "wind",
            "name": "wind_sensor_01",
            "location": "The Roof",
            "description": "A weather station",
            "properties": [
                {
                    "name": "speed",
                    "unit": "m/s",
                    "speed": 5.0
                },
                {
                    "name": "gust",
                    "unit": "m/s",
                    "speed": 9.0
                }
            ]
        }
    ]
}
```
