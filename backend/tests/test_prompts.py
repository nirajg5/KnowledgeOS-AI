from backend.retrival.pageindex_client import (
    KnowledgePageIndex
)

DOC_ID = "pi-cmr932c9200wc01o3obvtxs9e"

client = KnowledgePageIndex()

status = client.get_status(DOC_ID)

print(status)