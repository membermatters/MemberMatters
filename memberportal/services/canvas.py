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
            headers={"Authorization": "Bearer " + self.api_token},
        )

        return r.json()

    def _query_graph(self, query):
        response = requests.post(
            self.graphql_url,
            headers={"Authorization": "Bearer " + self.api_token},
            data=query,
        )

        return response.json()

    def get_course_details(self, course_id):
        query = {
            "query": "query MyQuery {course(id: "
            + str(course_id)
            + ") {enrollmentsConnection {nodes {user {email}grades {finalScore}}}}}",
        }
        return self._query_graph(query)

    def get_course_scores(self, course_id):
        students = self.get_course_details(course_id)
        print("query")
        print(students)
        students = students.get("data")

        if not students:
            return {}

        students = students["course"]["enrollmentsConnection"]["nodes"]
        scores = {}

        for student in students:
            print("student: " + str(student))
            scores[student.get("user").get("email").lower()] = student.get(
                "grades"
            ).get("finalScore")

        return scores

    def get_student_score_for_course(self, course_id, email):
        scores = self.get_course_scores(course_id)
        print("scores")
        print(scores)

        return scores.get(email.lower())
