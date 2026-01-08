from mcp_tools.sales.executor import execute_sales_query
from mcp_tools.sales.sql_builder import Payload

def query_sales(payload: Payload):
    return execute_sales_query(payload)
