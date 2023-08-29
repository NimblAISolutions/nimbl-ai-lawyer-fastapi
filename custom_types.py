from enum import Enum


class Sources(str, Enum):
    # 1k chunk size, no overlap
    pinecone_small = "pinecone_small"
    # 5k chunk size, 1k overlap
    pinecone_large = "pinecone_large"
    # 1k chunk size, no overlap
    zilliz_small = "zilliz_small"
    # 5k chunk size, 1k overlap
    zilliz_large = "zilliz_large"

    zilliz_laws = "zilliz_laws"
