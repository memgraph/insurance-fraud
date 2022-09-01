from dotenv import load_dotenv
import os

import pyarrow as pa
from pyarrow import dataset as ds
from pyarrow import fs

# First, load configuration from environment file
load_dotenv(".env")

BUCKET = "memgraph-fraud-bucket"
DESTINATION_DIR = "storing_parquets"
DESTINATION = f"{BUCKET}/{DESTINATION_DIR}"
s3_access_key = os.getenv("AWS_ACCESS_KEY_ID", "")
s3_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY", "")
s3_region = os.getenv("AWS_REGION", "eu-central-1")


def store_to_s3(
    dataset: ds.dataset,
    dataset_dir: str,
    dataset_name: str,
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

    ds.write_dataset(
        dataset,
        base_dir=dataset_dir,
        basename_template=f"{dataset_name}-{{i}}.parquet",
        filesystem=s3,
        format="parquet",
    )


def main() -> None:
    local_path = "./data/individuals.parquet"

    dataset = ds.dataset(local_path)

    store_to_s3(
        dataset,
        DESTINATION,
        "my-custom-dataset-name",
        region=s3_region,
        access_key=s3_access_key,
        secret_key=s3_secret_key,
    )


if __name__ == "__main__":
    main()
