import msgspec
from datetime import date
from typing import Literal, Optional, List, Tuple, TypedDict
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import TextClause
from mcp_tools.sales.schema import DIMENSIONS, METRICS

class TimeRange(TypedDict):
    # Using 'date' type ensures YYYY-MM-DD validation
    start: date
    end: date

class Payload(msgspec.Struct):
    metrics: list[str]
    dimensions: list[str]
    filters: dict[Literal["sales_person", "country", "product", "date"], str]
    time_range: TimeRange
    limit: Optional[int] = None


class DBParams(msgspec.Struct):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    limit: Optional[int] = None
    filters: dict[Literal["sales_person", "country", "product", "date"], str] = {}


def build_sales_query(payload: Payload) -> Tuple[TextClause, DBParams]:
    """
    Builds a parameterized SQLAlchemy text query
    and a parameters dictionary.
    """

    select_clauses: List[str] = []
    group_by_clauses: List[str] = []
    where_clauses: List[str] = []
    params: DBParams = DBParams(
        start_date=None,
        end_date=None,
        limit=None,
        filters={}
    )

    # Metrics (aggregations)
    for metric in payload.metrics:
        if metric not in METRICS:
            raise ValueError(f"Invalid metric: {metric}")
        select_clauses.append(f"{METRICS[metric]} AS {metric}")

    # Dimensions (group by)
    for dim in payload.dimensions:
        if dim not in DIMENSIONS:
            raise ValueError(f"Invalid dimension: {dim}")
        column = DIMENSIONS[dim]
        select_clauses.append(column)
        group_by_clauses.append(column)

    # Time range (mandatory)
    if not payload.time_range:
        raise ValueError("time_range is required")

    where_clauses.append("sale_date BETWEEN :start_date AND :end_date")
    params.start_date = payload.time_range["start"]
    params.end_date = payload.time_range["end"]

    # Filters
    for key, value in payload.filters.items():
        if key not in DIMENSIONS:
            raise ValueError(f"Invalid filter: {key}")
        where_clauses.append(f"{DIMENSIONS[key]} = :{key}")
        params.filters[key] = value

    # Base query
    query = f"""
        SELECT {", ".join(select_clauses)}
        FROM public.chocolate_sales
        WHERE {" AND ".join(where_clauses)}
    """

    # Group by
    if group_by_clauses:
        query += f" GROUP BY {', '.join(group_by_clauses)}"

    # Limit
    if payload.limit:
        query += " LIMIT :limit"
        params.limit = payload.limit

    return text(query), params
