import pyarrow.dataset as ds
from pyarrow import fs
from typing import List, Dict
from dotenv import load_dotenv
from gqlalchemy import QueryBuilder
import os


load_dotenv(".env")

BUCKET_NAME = "memgraph-parquet"
FILE_NAME = "userdata1.parquet"
ADDITIONAL_FILE_NAME = "users.parquet"

ALL_PARQUET_FILES = f"{BUCKET_NAME}"
SINGLE_PARQUET_FILE = f"{ALL_PARQUET_FILES}/{FILE_NAME}"
ADDITIONAL_PARQUET_FILE = f"{ALL_PARQUET_FILES}/{ADDITIONAL_FILE_NAME}"

DColumn = ds.field
DExpression = ds.Expression

query_builder = QueryBuilder()


def write_node_to_mg(label: str, data: Dict[str, object]):
    query_builder.create().node(labels=label, **data)


def write_relationship_to_mg(
    from_node: str,
    to_node: str,
    from_label: str,
    to_label: str,
    relationship_label: str,
    relationship_data: Dict[str, object],
):
    query_builder.match().node(
        labels=from_label, id=from_node, variable="a"
    ).match().node(labels=to_label, id=to_node, variable="b").create().node(
        variable="a"
    ).to(
        relationship_label, **relationship_data
    ).node(
        variable="b"
    )


def execute_query():
    global query_builder
    list(query_builder.execute())
    query_builder = QueryBuilder()


def load_from_S3(
    source: str,
    columns: List[str] = None,
    filter: DExpression = None,
    region: str = None,
    access_key: str = None,
    secret_key: str = None,
    session_token: str = None,
) -> None:
    s3 = fs.S3FileSystem(
        region=region,
        access_key=access_key,
        secret_key=secret_key,
        session_token=session_token,
    )
    dataset = ds.dataset(source, filesystem=s3)

    for batch in dataset.to_batches(
        columns=columns,
        filter=filter,
    ):
        batch_list = batch.to_pylist()
        for item in batch_list:
            write_node_to_mg("item", item)


def main() -> None:
    load_from_S3(
        source=ALL_PARQUET_FILES,
        columns=["first_name", "last_name", "salary"],
        filter=(DColumn("first_name") == "Mark") | (DColumn("salary") > 2000),
        region="eu-central-1",
        access_key=os.getenv("AWS_ACCESS_KEY_ID", ""),
        secret_key=os.getenv("AWS_SECRET_ACCESS_KEY", ""),
    )
    pass


if __name__ == "__main__":
    main()
