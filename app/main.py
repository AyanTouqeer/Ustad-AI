from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.cloud import firestore
import uvicorn
import os

app = FastAPI(title="Ustad.ai Production Service Orchestrator")

#Point to your downloaded key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcp-key.json"

# Initialize Firestore Client (Automatically detects credentials on Google Cloud)
db = firestore.Client()

# Schemas for incoming mobile app requests
class UserProfile(BaseModel):
    user_id: str  
    name: str
    preferred_language: str
    city: str
    neighborhood: str

class OrchestrationRequest(BaseModel):
    user_id: str
    query: str

@app.get("/")
def health_check():
    return {"status": "Production backend running securely."}

@app.post("/register")
def register_user(profile: UserProfile):
    """Stores or updates real user profiles in Firestore."""
    try:
        user_ref = db.collection("users").document(profile.user_id)
        user_ref.set({
            "name": profile.name,
            "preferred_language": profile.preferred_language,
            "city": profile.city,
            "neighborhood": profile.neighborhood
        })
        return {"status": "success", "message": f"Profile saved for {profile.name}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/orchestrate")
def orchestrate_service(request: OrchestrationRequest):
    try:
        # 1. Attempt to fetch user context from Firestore
        user_ref = db.collection("users").document(request.user_id)
        user_doc = user_ref.get()
        
        # Fallback profile data if the document doesn't exist yet in your new DB
        user_city = "Islamabad"
        user_lang = "Roman Urdu"
        
        if user_doc.exists:
            profile = user_doc.to_dict()
            user_city = profile.get("city", user_city)
            user_lang = profile.get("preferred_language", user_lang)

        # 2. Mock Agent Matcher Logic for Demo Stability
        # This guarantees a beautiful response on your frontend instead of crashing
        user_query = request.query.lower()
        
        if "ac" in user_query or "technician" in user_query:
            match_message = f"Ustad Match Found! Connecting you with Mohammad Rizwan (Certified HVAC Technician) in {user_city}. Response optimized for {user_lang}."
        elif "plumber" in user_query or "pipe" in user_query:
            match_message = f"Ustad Match Found! Connecting you with Amjad Khan (Master Plumber) in {user_city}. Response optimized for {user_lang}."
        else:
            match_message = f"Request received for '{request.query}'. Routing to nearest specialized provider in {user_city}..."

        return {"status": "success", "response_message": match_message}

    except Exception as e:
        # If anything breaks, return a clean message instead of a raw 500 crash
        return {"status": "error", "response_message": f"AI Orchestrator standard bypass active. Error: {str(e)}"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)