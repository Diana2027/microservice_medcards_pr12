from fastapi import FastAPI, HTTPException
from app.medcard import Medcard, CreateMedcard

medcards: list[Medcard] = [
    # Medcard(0, 'Медкарта №1', 'Дементьева Маргарита Ярославовна'),
    # Medcard(1, 'Медкарта №2', 'Матвеев Савва Тимофеевич'),
    # Medcard(2, 'Медкарта №3', 'Суркова Ева Артёмовна'),
    # Medcard(3, 'Медкарта №4', 'Соколова Полина Давидовна'),
    # Medcard(4, 'Медкарта №5', 'Селезнева Ника Ильинична'),
    # Medcard(5, 'Медкарта №6', 'Авдеев Максим Максимович')
]

def add_medcard(content: CreateMedcard):
    id = len(medcards)
    medcards.append(Medcard(id, content.title, content.fio))
    return id

app = FastAPI()

########
# Jaeger

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

resource = Resource(attributes={
    SERVICE_NAME: 'cards-service'
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
########

########
# Prometheus

from prometheus_fastapi_instrumentator import Instrumentator

@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)

#
########

@app.get("/v1/cards")
async def get_cards():
    return medcards

@app.post("/v1/cards")
async def add_card(content: CreateMedcard):
    add_medcard(content)
    return medcards[-1]

@app.get("/v1/cards/{id}")
async def get_cards_by_id(id: int):
    result = [item for item in medcards if item.id == id]
    if len(result) > 0:
        return result[0]
    raise HTTPException(status_code = 404, detail="Документ не найден")

@app.get("/__health")
async def check_service():
    return