# Import environment config
from pathlib import Path
from dotenv import load_dotenv

# Import the library needed for graph data handling
# GQLAlchemy is the Object Graph Mapper (OGM) - a link between graph database objects and Python objects.
from gqlalchemy import Memgraph
from gqlalchemy.loaders import ParquetLocalFileSystemImporter
import os
import yaml

# First, load configuration from environment file
load_dotenv(".env")

# Define a graph DB connector
mg_host = os.getenv("MG_HOST", "localhost")
mg_port = int(os.getenv("MG_PORT", "7687"))
db = Memgraph(mg_host, mg_port)

PATH_TO_CONFIG_YAML = "./config.yml"

def main() -> None:
    with Path(PATH_TO_CONFIG_YAML).open("r") as f_:
        data_configuration = yaml.safe_load(f_)

    translator = ParquetLocalFileSystemImporter(
        path="./dataset/data/",
        data_configuration=data_configuration,
        memgraph=db
    )

    translator.translate(drop_database_on_start=True)


if __name__ == "__main__":
    main()
