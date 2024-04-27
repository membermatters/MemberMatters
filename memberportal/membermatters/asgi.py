import os

## Tracing
from opentelemetry import trace, context, propagate
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.asgi import OpenTelemetryMiddleware

## Logging
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

## Databases
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor

## DJANGO
from opentelemetry.instrumentation.django import DjangoInstrumentor

# INTERNAL URLS
from django.conf.urls import url
from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "membermatters.settings")
django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from membermatters.websocket_urls import urlpatterns

### OTEL EXPORTER SETUP ###

resource = Resource(
    attributes={
        "service.name": "member_portal_backend",
        "deployment.environment": "production",
        "service.namespace": "membermatters",
    }
)

#### TRACES
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

otlp_trace_exporter = OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")

span_processor = BatchSpanProcessor(otlp_trace_exporter)

trace.get_tracer_provider().add_span_processor(span_processor)

#### LOGS
logger_provider = LoggerProvider(resource=resource)
otlp_logs_exporter = OTLPLogExporter(endpoint="http://localhost:4318/v1/logs")
logger_provider.add_log_record_processor(BatchLogRecordProcessor(otlp_logs_exporter))

#### Database
Psycopg2Instrumentor().instrument(enable_commenter=True, commenter_options={})

#### Django
DjangoInstrumentor().instrument(is_sql_commentor_enabled=True)

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(URLRouter(urlpatterns)),
    }
)
application = OpenTelemetryMiddleware(application)
