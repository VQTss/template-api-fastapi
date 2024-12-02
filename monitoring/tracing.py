from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import get_tracer_provider, set_tracer_provider
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.resources import SERVICE_NAME

class TraceManager:
    def __init__(self, service_name: str, jaeger_host: str = "localhost", jaeger_port: int = 6831):
        set_tracer_provider(
            TracerProvider(
                resource=Resource.create({SERVICE_NAME: service_name})
            )
        )

        self.tracer = get_tracer_provider().get_tracer(service_name, "0.1.2")

        # Set up Jaeger exporter
        jaeger_exporter = JaegerExporter(
            agent_host_name=jaeger_host,
            agent_port=jaeger_port
        )

        # Add BatchSpanProcessor
        span_processor = BatchSpanProcessor(jaeger_exporter)
        get_tracer_provider().add_span_processor(span_processor)

    def get_tracer(self):
        return self.tracer
