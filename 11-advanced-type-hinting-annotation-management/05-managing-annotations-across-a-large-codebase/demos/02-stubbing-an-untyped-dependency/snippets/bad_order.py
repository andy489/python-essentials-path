from telemetry_hub.models import summarize
from telemetry_hub.pipeline import Pipeline, validate

broken = Pipeline(validate).then(summarize)
