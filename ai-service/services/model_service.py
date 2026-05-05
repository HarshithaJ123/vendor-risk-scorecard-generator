from sentence_transformers import SentenceTransformer

# 🔥 Load model only once at startup
print("🔄 Loading sentence transformer model...")

model = SentenceTransformer('all-MiniLM-L6-v2')

print("✅ Model loaded successfully!")

def get_model():
    return model