import chromadb
from sentence_transformers import SentenceTransformer

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create DB client
client = chromadb.Client()

# Create collection
collection = client.get_or_create_collection(name="vendor_knowledge")

def initialize_chroma():
    if collection.count() == 0:
        seed_documents()

# Seed documents
def seed_documents():
    docs = [
        "Vendors must follow ISO 27001 compliance.",
        "High risk vendors require quarterly audits.",
        "Data encryption must be applied at rest and in transit.",
        "Third-party vendors must sign NDA agreements.",
        "Vendor access should follow least privilege principle.",
        "Regular security assessments are mandatory.",
        "Incident response plans must be defined.",
        "GDPR compliance is required for EU data.",
        "Logs must be monitored continuously.",
        "Vendor risk score should be updated monthly."
    ]

    embeddings = model.encode(docs).tolist()

    collection.add(
        documents=docs,
        embeddings=embeddings,
        ids=[f"doc_{i}" for i in range(len(docs))]
    )

# Query relevant knowledge
def query_knowledge(text):
    embedding = model.encode([text]).tolist()

    results = collection.query(query_texts=[text],n_results=2)

    return results["documents"][0]