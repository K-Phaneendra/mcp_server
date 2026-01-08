import os
from fastapi import FastAPI
import json
from pathlib import Path

from mcp_tools.sales.server import query_sales
from mcp_tools.sales.sql_builder import Payload, TimeRange

from pydantic import BaseModel
from datetime import date
from typing import Optional, Literal

FilterKey = Literal["sales_person", "country", "product", "date"]


class TimeRangeAPI(BaseModel):
    start: date
    end: date


class PayloadAPI(BaseModel):
    metrics: list[str]
    dimensions: list[str]
    filters: dict[FilterKey, str]
    time_range: TimeRangeAPI
    limit: Optional[int] = None


app = FastAPI(title="query sales information")

@app.post("/")
async def run_query(payload: PayloadAPI):
    # Convert Pydantic → msgspec
    internal_payload = Payload(
        metrics=payload.metrics,
        dimensions=payload.dimensions,
        filters=dict(payload.filters),  # SAFE: already validated
        time_range=TimeRange(
            start=payload.time_range.start,
            end=payload.time_range.end,
        ),
        limit=payload.limit,
    )
    return await query_sales(internal_payload)

@app.get("/manifest.json")
def manifest():
    current_folder_path = Path(__file__).resolve().parent
    manifest_json = os.path.join(current_folder_path, "manifest.json")
    with open(manifest_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data