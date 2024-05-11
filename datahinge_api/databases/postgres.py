from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
import zipfile
import io

router = APIRouter()

class DatabaseConfig(BaseModel):
    db_name: str = Field(..., example="your_database")
    db_user: str = Field(..., example="your_user")
    db_password: str = Field(..., example="your_password")
    db_host: str = Field(..., example="localhost")
    db_port: str = Field("5432", example="5432")

class User(BaseModel):
    id: int
    name: str
    email: str

class QueryRequest(BaseModel):
    query: str

class DataAddRequest(BaseModel):
    table_name: str
    data: List[dict]

def get_db_connection(config: DatabaseConfig):
    try:
        return psycopg2.connect(
            dbname=config.db_name,
            user=config.db_user,
            password=config.db_password,
            host=config.db_host,
            port=config.db_port,
            cursor_factory=RealDictCursor
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to the database: {str(e)}")

@router.post("/users/", response_model=List[User], status_code=status.HTTP_200_OK)
def fetch_users(config: DatabaseConfig):
    query = "SELECT id, name, email FROM users;"
    try:
        with get_db_connection(config) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
                return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed during database operation: {str(e)}")

@router.post("/query/", response_model=List[dict], status_code=status.HTTP_200_OK)
def execute_query(config: DatabaseConfig, request: QueryRequest):
    query = request.query
    try:
        with get_db_connection(config) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
                return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed during database operation: {str(e)}")

@router.post("/add_data/", status_code=status.HTTP_201_CREATED)
def add_data(config: DatabaseConfig, request: DataAddRequest):
    table_name = request.table_name
    data = request.data
    try:
        with get_db_connection(config) as conn:
            with conn.cursor() as cur:
                for item in data:
                    columns = ",".join(item.keys())
                    values = ",".join([f"'{val}'" for val in item.values()])
                    query = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"
                    cur.execute(query)
                conn.commit()
                return {"message": "Data added successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed during database operation: {str(e)}")

@router.post("/create_table/", status_code=status.HTTP_201_CREATED)
def create_table(config: DatabaseConfig, table_name: str, columns: List[dict]):
    try:
        with get_db_connection(config) as conn:
            with conn.cursor() as cur:
                query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
                for column in columns:
                    query += f"{column['name']} {column['type']},"
                query = query.rstrip(",") + ");"
                cur.execute(query)
                conn.commit()
                return {"message": "Table created successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed during database operation: {str(e)}")

@router.post("/backup_to_zip/", status_code=status.HTTP_200_OK)
def backup_to_zip(config: DatabaseConfig, filename: str):
    try:
        with get_db_connection(config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
                tables = [table[0] for table in cur.fetchall()]
                with zipfile.ZipFile(filename, "w") as zip_file:
                    for table in tables:
                        cur.execute(f"SELECT * FROM {table};")
                        result = cur.fetchall()
                        with io.StringIO() as f:
                            for row in result:
                                f.write(",".join(str(val) for val in row) + "\n")
                            zip_file.writestr(f"{table}.csv", f.getvalue())
                return {"message": "Backup successful"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed during database operation: {str(e)}")