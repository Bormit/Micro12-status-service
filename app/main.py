from fastapi import FastAPI, HTTPException
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from pydantic import BaseModel

class CreateStatusModel(BaseModel):
    status: str
    listOrder: str

class Status:
    def __init__(self, id: int, status: str, listOrder: str):
        self.id = id
        self.status = status
        self.listOrder = listOrder

statusList: list[Status] = [
    # Status(0, 'Создан', 'Microwave'),
    # Status(1, 'Оплачен', 'Cat food'),
    # Status(2, 'Ожидает оплаты', 'Fridge')
]

def add_status(content: CreateStatusModel):
    id = len(statusList)
    statusList.append(Status(id, content.status, content.listOrder))
    return id

app = FastAPI()


#######
# Jaeger

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

resource = Resource(attributes={
    SERVICE_NAME: "status-service"
})

jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(jaeger_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

FastAPIInstrumentor.instrument_app(app)

#
#######

#######
#Prometheus

from prometheus_fastapi_instrumentator import Instrumentator

@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)

#
#######


@app.get("/v1/orders")
async def get_orders():
    return statusList

@app.post("/v1/orders")
async def add_stat(content: CreateStatusModel):
    add_status(content)
    return statusList[-1]

@app.get("/v1/orders/{id}")
async def get_orders_by_id(id: int):
    result = [item for item in statusList if item.id == id]
    if len(result) > 0:
        return result[0]
    else:
        raise HTTPException(status_code=404, detail="Orders not found")

@app.get("/__health")
async def check_service():
    return

