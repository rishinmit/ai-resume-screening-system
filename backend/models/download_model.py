from sentence_transformers import SentenceTransformer

# download model from huggingface
model = SentenceTransformer("all-MiniLM-L6-v2")

# save locally
model.save("models/ats_model")

print("Model saved locally in backend/models/ats_model")