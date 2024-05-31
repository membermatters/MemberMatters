import logging
import json

from rest_framework import permissions

import api_metrics.metrics
from api_metrics.models import Metric
from api_general.models import SiteSession

from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger("metrics")


class Statistics(APIView):
    """
    get: gets site statistics.
    """

    def get(self, request):
        members = SiteSession.objects.filter(signout_date=None).order_by("-signin_date")
        member_list = []

        for member in members:
            member_list.append(member.user.profile.get_full_name())

        statistics = {"onSite": {"members": member_list, "count": members.count()}}

        return Response(statistics)


class UpdatePromMetrics(APIView):
    """
    post: triggers Django to update the Prometheus site metrics from the database.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        # get the latest distinct metric
        metrics = Metric.objects.order_by("creation_date").distinct("metric_name")

        for metric in metrics:
            if metric.metric_name in [
                Metric.MetricName.MEMBER_COUNT_TOTAL,
                Metric.MetricName.SUBSCRIPTION_COUNT_TOTAL,
            ]:
                prom_metric = getattr(api_metrics.metrics, metric.name)

                if not prom_metric:
                    logger.error(f"Prometheus metric {metric.name} not found.")
                    continue

                for state in metric.data:
                    prom_metric.labels(state=state["state"]).set(state["total"])

        return Response()
