from typing import TypedDict, List, Dict, Any, Sequence
from sqlalchemy.engine import Result, RowMapping
from datetime import date

from database import engine
from mcp_tools.sales.sql_builder import build_sales_query, Payload

class ResultSchema(TypedDict, total=False):
    sales_person: str
    country: str
    product: str
    sale_date: date
    total_sales: float
    boxes_shipped: int
    avg_sale: float

async def execute_sales_query(payload: Payload) -> List[ResultSchema]:
    """
    Executes a sales query built from structured intent
    and returns rows as dictionaries.
    """

    query, params = build_sales_query(payload)

    # Flatten DBParams into a dict usable by SQLAlchemy
    bound_params: Dict[str, Any] = {}

    if params.start_date:
        bound_params["start_date"] = params.start_date
    if params.end_date:
        bound_params["end_date"] = params.end_date
    if params.limit:
        bound_params["limit"] = params.limit

    # Add dynamic filter parameters
    for key, value in params.filters.items():
        bound_params[str(key)] = value

    async with engine.connect() as conn:
        result: Result[Any] = await conn.execute(query, bound_params)
        rows: Sequence[RowMapping] = result.mappings().all()

    # Cast RowMapping → ResultSchema
    return [ResultSchema(**row) for row in rows]
