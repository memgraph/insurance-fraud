import yaml
from gqlalchemy.loaders import ParquetLocalFileSystemImporter


def load_data_memgraph():
    with open("config.yml", 'r') as f:
        translation_mappings = yaml.safe_load(f)
        importer = ParquetLocalFileSystemImporter("dataset/data/", translation_mappings)
        importer.translate(drop_database_on_start=True)


if __name__ == "__main__":
    load_data_memgraph()
