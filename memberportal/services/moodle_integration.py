from constance import config
import requests
import math


def get_moodle_url(function_name: str):
    MOODLE_BASE_URL = config.MOODLE_API_BASE_URL
    MOODLE_TOKEN = config.MOODLE_API_TOKEN

    MOODLE_URL = (
        MOODLE_BASE_URL
        + "/webservice/rest/server.php?wstoken="
        + MOODLE_TOKEN
        + "&moodlewsrestformat=json&wsfunction="
    )

    return MOODLE_URL + function_name


def get_moodle_completion_state(completion_state_id: int):
    # completion state value: 0 means incomplete, 1 complete, 2 complete - pass, 3 complete - fail

    if completion_state_id == 0:
        return "incomplete"
    elif completion_state_id == 1:
        return "complete"
    elif completion_state_id == 2:
        return "complete_pass"
    elif completion_state_id == 3:
        return "complete_fail"
    else:
        raise RuntimeError("Invalid completion state id: " + str(completion_state_id))


def moodle_get_course_activity_completion_status(course_id: str, user_id: str):
    course_activities_url = (
        get_moodle_url("core_completion_get_activities_completion_status")
        + f"&courseid={course_id}&userid={user_id}"
    )

    course_activities_data = requests.get(course_activities_url).json()

    total_course_activities = len(course_activities_data.get("statuses"))
    completed_course_activities = []
    incomplete_course_activities = []

    for activity in course_activities_data.get("statuses"):
        activity_status = get_moodle_completion_state(activity["state"])

        if activity_status in ("complete", "complete_pass", "complete_fail"):
            completed_course_activities.append(activity)
        else:
            incomplete_course_activities.append(activity)

    return {
        "total_course_activities": total_course_activities,
        "completed_course_activities": len(completed_course_activities),
        "incomplete_course_activities": len(incomplete_course_activities),
        "percentage_completed": math.floor(
            (len(completed_course_activities) / total_course_activities) * 100
        ),
    }


def moodle_get_user_from_email(user_email: str):
    user_data_url = (
        get_moodle_url("core_user_get_users_by_field")
        + f"&field=email&values[0]={user_email}"
    )

    user_data = requests.get(user_data_url).json()

    if len(user_data) > 1:
        raise RuntimeError("Multiple users found with email: " + user_email)

    elif len(user_data) == 0:
        raise RuntimeError("No users found with email: " + user_email)

    else:
        user = {
            "id": user_data[0]["id"],
            "email": user_data[0]["email"],
            "username": user_data[0]["username"],
            "firstname": user_data[0]["firstname"],
            "lastname": user_data[0]["lastname"],
            "fullname": user_data[0]["fullname"],
        }

        return user
