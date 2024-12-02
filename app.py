from fastapi import FastAPI, Query
import requests
import base64
import cv2
import json
from time import time
from config import Config
from monitoring.logging_config import setup_logging
from monitoring.metrics import MetricsManager
from monitoring.tracing import TraceManager
from utils.index import get_image_from_url, get_model
from opentelemetry import trace  # Import the trace object

# Initialize components
logger = setup_logging()
metrics_manager = MetricsManager(service_name=Config.SERVICE_NAME, port=Config.PROMETHUES_PORT)
trace_manager = TraceManager(service_name=Config.SERVICE_NAME)
tracer = trace_manager.get_tracer()

# Load the model
with tracer.start_as_current_span("model-loading"):
    model = get_model()

app = FastAPI()

@app.post("/od-macular-detection")
async def od_macular_detection(image_url: str = Query(..., description="URL of the image to process.")):
    start_time = time()
    label = {"api": "/od-macular-detection"}
    
    try:
        with tracer.start_as_current_span("processors") as processors:
            with tracer.start_as_current_span(
                "image-loader", links=[trace.Link(processors.get_span_context())]
            ):
                response = requests.get(image_url)
                response.raise_for_status()
                mime_type = response.headers.get('Content-Type', 'image/png')
                input_image = get_image_from_url(response.content)
            
            with tracer.start_as_current_span(
                "predictor", links=[trace.Link(processors.get_span_context())]
            ):
                outputs = model(input_image)
                outputs.render()
            
            with tracer.start_as_current_span(
                "image-annotation", links=[trace.Link(processors.get_span_context())]
            ):
                for im in outputs.ims:
                    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
                    _, encoded_image = cv2.imencode('.png', im)
                    base64_image = base64.b64encode(encoded_image).decode("utf-8")
            
            with tracer.start_as_current_span(
                "image-json", links=[trace.Link(processors.get_span_context())]
            ):
                od_macular = outputs.pandas().xyxy[0].to_json(orient="records")
                od_macular = json.loads(od_macular)
                results = {
                    "annotated_image": f"data:{mime_type};base64,{base64_image}",
                    "od_macular": od_macular
                }
                metrics_manager.success_counter.add(1, label)

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to retrieve image: {e}")
        metrics_manager.error_counter.add(1, label)
        return {"error": f"Failed to retrieve image from URL: {e}"}

    end_time = time()
    elapsed_time = end_time - start_time
    metrics_manager.response_latency.record(elapsed_time, label)
    metrics_manager.request_counter.add(1, label)

    return results

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app, host="0.0.0.0", port=Config.PORT_SERVER)
