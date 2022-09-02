# Import environment config
from pathlib import Path
from dotenv import load_dotenv

# Import the library needed for graph data handling
# GQLAlchemy is the Object Graph Mapper (OGM) - a link between graph database objects and Python objects.
from gqlalchemy.loaders import ParquetS3FileSystemImporter
import os
import yaml

# First, load configuration from environment file
load_dotenv(".env")

# Define a graph DB connector
mg_host = os.getenv("MG_HOST", "localhost")
mg_port = int(os.getenv("MG_PORT", "7687"))
# db = Memgraph(mg_host, mg_port)


BUCKET = "insurance-data-bucket"
s3_access_key = os.getenv("AWS_ACCESS_KEY_ID", "")
s3_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY", "")
s3_region = os.getenv("AWS_REGION", "eu-west-1")


PATH_TO_CONFIG_YAML = "./config.yml"
PARQUET_FILE_EXTENSION = "parquet"


def main() -> None:
    with Path(PATH_TO_CONFIG_YAML).open("r") as f_:
        data_configuration = yaml.safe_load(f_)

    translator = S3Translator(
        bucket_name=BUCKET,
        data_configuration=data_configuration,        
        access_key=s3_access_key,
        secret_key=s3_secret_key,
        region=s3_region,
    )

    translator.translate(drop_database_on_start=True)


if __name__ == "__main__":
    main()
