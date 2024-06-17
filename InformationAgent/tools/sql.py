from langchain.tools import Tool
from pydantic.v1 import BaseModel
from typing import List
import sqlite3

connect = sqlite3.connect("db.sqlite")

def run_sqlite_query(query):
    c = connect.cursor()
    try:
        c.execute(query)
        return c.fetchall()
    except sqlite3.OperationalError as err :
        return f"The following error occured : {str(err)}"

#To customise argument from __args1 which Langchain by default provides for tools.
class RunQueryArgsSchema(BaseModel):
    query:str

run_query_tool = Tool.from_function(
    name="run_sqlite_query",
    description = "Run a sqlite query",
    func=run_sqlite_query,
    args_schema=RunQueryArgsSchema #feeding the class will make langchain to use the custom name of argument instead of default one, which will be more meaningful for llms
)



def list_tables():
    c = connect.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = c.fetchall()
    return "\n".join(row[0] for row in rows if row[0] is not None)



def describe_tables(table_names):
    c = connect.cursor()
    tables = '. '.join("'"+table+"'" for table in table_names)
    rows  = c.execute(f"SELECT sql FROM sqlite_master WHERE type= 'table' and name IN({tables});")
    return '\n'.join(row[0] for row in rows if row[0] is not None)


#To customise argument from __args1 which Langchain by default provides for tools.
class DescribeTablesArgsSchema(BaseModel):
    tables_name:List[str]

describe_tables_tool = Tool.from_function(
    name="describe_tables",
    description="Given a list of table names, return the schema of those tables",
    func=describe_tables,
    args_schema=DescribeTablesArgsSchema
)