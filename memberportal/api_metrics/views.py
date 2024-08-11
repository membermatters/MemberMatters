from django.db.models import Max, Sum
from django.utils import timezone
from rest_framework_api_key.permissions import HasAPIKey

import api_metrics.metrics as api_metrics
from api_metrics.models import Metric
from api_general.models import SiteSession

from constance import config
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
import logging

logger = logging.getLogger("metrics")


class Statistics(APIView):
    """
    get: gets site statistics.
    """

    def get(self, request):
        statistics = {}

        # On site members
        on_site = {"members": [], "count": 0}
        members = SiteSession.objects.filter(signout_date=None).order_by("-signin_date")
        on_site["count"] = members.count()

        for member in members:
            on_site["members"].append(member.user.profile.get_full_name())

        statistics["on_site"] = on_site

        for metric_name in Metric.MetricName.values:
            # Don't return any data from the API if the stats page isn't enabled
            if config.ENABLE_STATS_PAGE or request.user.is_admin:
                metric_data = []
                one_year_before_today = timezone.now() - timezone.timedelta(
                    days=config.STATS_MAX_DAYS
                )
                last_stat_per_day = (
                    Metric.objects.filter(
                        name=metric_name, creation_date__gte=one_year_before_today
                    )
                    .extra(select={"the_date": "date(creation_date)"})
                    .values_list("the_date")
                    .order_by("-the_date")
                    .annotate(max_date=Max("creation_date"))
                )
                max_dates = [item[1] for item in last_stat_per_day]
                metrics = Metric.objects.filter(
                    name=metric_name, creation_date__in=max_dates
                ).order_by("creation_date")
                for metric in metrics:
                    metric_data.append(
                        {"date": metric.creation_date, "data": metric.data}
                    )
                statistics[metric_name] = metric_data
            else:
                statistics[metric_name] = []

        return Response(statistics)


class UpdateStatistics(APIView):
    """
    put: This method updates and stores a new set of statistics.
    """

    permission_classes = (permissions.IsAdminUser | HasAPIKey,)

    def put(self, request):
        api_metrics.calculate_member_count()
        api_metrics.calculate_member_count_6_months()
        api_metrics.calculate_member_count_12_months()
        api_metrics.calculate_subscription_count()
        api_metrics.calculate_memberbucks_balance()
        api_metrics.calculate_memberbucks_transactions()

        return Response()


class UpdatePromMetrics(APIView):
    """
    post: triggers Django to update the Prometheus site metrics from the database.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        metrics = []

        # get the latest metric for each type
        for name in Metric.MetricName.values:
            metric = Metric.objects.filter(name=name).order_by("-creation_date").first()
            if metric:
                metrics.append(metric)

        for metric in metrics:
            if metric.name in [
                Metric.MetricName.MEMBER_COUNT_TOTAL,
                Metric.MetricName.MEMBER_COUNT_6_MONTHS,
                Metric.MetricName.MEMBER_COUNT_12_MONTHS,
                Metric.MetricName.SUBSCRIPTION_COUNT_TOTAL,
                Metric.MetricName.MEMBERBUCKS_BALANCE_TOTAL,
                Metric.MetricName.MEMBERBUCKS_TRANSACTIONS_TOTAL,
            ]:
                prom_metric = getattr(api_metrics.metrics, metric.name)

                if not prom_metric:
                    logger.error(f"Prometheus metric {metric.name} not found.")
                    continue

                for state in metric.data:
                    if metric.name in [
                        Metric.MetricName.MEMBERBUCKS_TRANSACTIONS_TOTAL,
                    ]:
                        logger.debug(
                            f"Setting {metric.name} {state['type']} to {state['total']}"
                        )
                        prom_metric.labels(type=state["type"]).set(state["total"])

                    elif metric.name in [Metric.MetricName.MEMBERBUCKS_BALANCE_TOTAL]:
                        logger.debug(f"Setting {metric.name} to {metric.data[state]}")
                        prom_metric.set(metric.data[state])

                    else:
                        logger.debug(
                            f"Setting {metric.name} {state['state']} to {state['total']}"
                        )
                        prom_metric.labels(state=state["state"]).set(state["total"])

        return Response()
