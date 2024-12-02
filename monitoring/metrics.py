from prometheus_client import start_http_server
from opentelemetry import metrics
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.metrics import set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

class MetricsManager:
    def __init__(self, service_name: str, port: int = 8099, addr: str = '0.0.0.0'):
        # Start Prometheus client
        start_http_server(port=port, addr=addr)

        # Metrics setup
        resource = Resource(attributes={SERVICE_NAME: service_name})
        reader = PrometheusMetricReader()
        provider = MeterProvider(resource=resource, metric_readers=[reader])
        set_meter_provider(provider)

        # Create metrics
        meter = metrics.get_meter(service_name, "0.1.2")
        self.request_counter = meter.create_counter(
            name=f"{service_name}_request_total",
            description=f"Total number of {service_name} requests",
        )
        self.success_counter = meter.create_counter(
            name=f"{service_name}_request_success_total",
            description=f"Count of successful {service_name} requests",
        )
        self.error_counter = meter.create_counter(
            name=f"{service_name}_request_error_total",
            description=f"Count of failed {service_name} requests",
        )
        self.response_latency = meter.create_histogram(
            name=f"{service_name}_response_latency_seconds",
            description=f"{service_name} response latency in seconds",
            unit="seconds"
        )
