import requests
from constance import config


class Canvas:
    base_url = "https://canvas.instructure.com/api/v1/"
    graphql_url = "https://canvas.instructure.com/api/graphql/"

    def __init__(self):
        self.api_token = config.CANVAS_API_TOKEN

    def _get(self, url):
        r = requests.get(
            self.base_url + url,
            headers={"Authorization": f"Bearer {self.api_token}"},
        )

        return r.json()

    def _query_graph(self, query):
        response = requests.post(
            self.graphql_url,
            headers={"Authorization": f"Bearer {self.api_token}"},
            data=query,
        )

        return response.json()

    def get_course_details(self, course_id):
        """
        Build the query and get the course details.
        :param course_id:
        :return:
        """
        query = {
            "query": 'query MyQuery {course(id: "'
            + str(course_id)
            + '") {enrollmentsConnection {nodes {user {email}grades {finalScore}}}}}',
        }
        return self._query_graph(query)

    def get_course_scores(self, course_id):
        """
        Get all of the scores for a given course_id.
        :param course_id:
        :return:
        """
        # get the course details
        students = self.get_course_details(course_id)
        students = students.get("data")

        if not students:
            # if there are no students just return an empty dict
            return {}

        # get the result of our query
        students = students["course"]["enrollmentsConnection"]["nodes"]
        scores = {}

        # loop through each student, and if they have an email, add them to the scores dict
        for student in students:
            student_email = student.get("user").get("email")
            if student_email:
                scores[student_email.lower()] = student.get("grades").get("finalScore")

        return scores

    def get_student_score_for_course(self, course_id, email):
        """
        Get the student's score for a particular course_id. Returns None if nonexistent.
        :param course_id:
        :param email:
        :return: score or None
        """
        scores = self.get_course_scores(course_id)

        return scores.get(email.lower())
