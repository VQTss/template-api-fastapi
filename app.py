# Library for fastapi
from fastapi import FastAPI, Query
from fastapi.security import HTTPBasic
import requests
import base64
from time import time
import uvicorn
import json
import logging 


# Library for prometheus
from prometheus_client import start_http_server
from opentelemetry import metrics
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.metrics import set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource



# Library for tracing
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import get_tracer_provider, set_tracer_provider
from opentelemetry.exporter.jaeger.thrift import JaegerExporter



# Library for logs
from loguru import Logger



# Config
from config import Config  


# Library for models



# ==================== Start Logging Config ========================
logger = logging.getLogger(Config.SERVICE_NAME)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
# ==================== End Logging Config ========================



