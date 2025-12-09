from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import sys
import os
import pickle
import numpy as np
import mediapipe as mp

# Add model directory to path so we can import modules from it
current_dir = os.path.dirname(os.path.abspath(__file__))
model_dir = os.path.join(current_dir, '..', 'model')
sys.path.append(model_dir)

# Import from the model directory
try:
    from yoga_pose_classifier import extract_pose_features, calculate_angle, calculate_distance
    from pose_rules import POSE_CORRECTION_RULES
except ImportError as e:
    print(f"Error importing model modules: {e}")
    # We will handle this gracefully in the endpoints

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize MediaPipe Pose for constant/enum access
mp_pose = mp.solutions.pose

# Load Model (Global variable)
model_data = None

def load_model():
    global model_data
    model_path = os.path.join(model_dir, 'svm_classifier.pkl')
    if os.path.exists(model_path):
        try:
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
            print("Model loaded successfully")
        except Exception as e:
            print(f"Failed to load model: {e}")
    else:
        print(f"Model file not found at {model_path}")

load_model()

# Data models
class LandmarkPoint(BaseModel):
    x: float
    y: float
    z: float
    visibility: float

class PoseData(BaseModel):
    landmarks: List[LandmarkPoint]

class PredictionResponse(BaseModel):
    pose_name: str
    confidence: float
    corrections: List[str]

# Helper class to mimic MediaPipe landmark object
class LandmarkObject:
    def __init__(self, x, y, z, visibility):
        self.x = x
        self.y = y
        self.z = z
        self.visibility = visibility

class LandmarkListWrapper:
    def __init__(self, landmarks: List[LandmarkPoint]):
        self.landmark = [LandmarkObject(l.x, l.y, l.z, l.visibility) for l in landmarks]

@app.get("/")
async def root():
    return {"status": "ok", "model_loaded": model_data is not None}

@app.post("/classify", response_model=PredictionResponse)
async def classify_pose(data: PoseData):
    if model_data is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Wrap landmarks to match what extract_pose_features expects
        wrapped_landmarks = LandmarkListWrapper(data.landmarks)
        
        # 1. Extract features
        features = extract_pose_features(wrapped_landmarks)
        
        # 2. Normalize features
        scaler = model_data['scaler']
        features_scaled = scaler.transform(features.reshape(1, -1))
        
        # 3. Predict Pose
        model = model_data['model']
        pose_names = model_data['pose_names']
        
        pose_idx = model.predict(features_scaled)[0]
        pose_name = pose_names[pose_idx]
        
        # 4. Get Confidence
        probabilities = model.predict_proba(features_scaled)[0]
        confidence = float(probabilities[pose_idx])
        
        print(f"Pred: {pose_name} ({confidence:.2f})") # Debug log
        
        # 5. Check Corrections
        corrections = check_corrections_logic(wrapped_landmarks, pose_name, confidence)
        
        return PredictionResponse(
            pose_name=pose_name,
            confidence=confidence,
            corrections=corrections
        )
        
    except Exception as e:
        print(f"Error processing pose: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def check_corrections_logic(landmarks, pose_name: str, confidence: float) -> List[str]:
    """
    Re-implementation of check_corrections from correction.py to start from wrapper.
    Ideally we should import this logic if it was a standalone function, 
    but it's a method of RealtimePoseCorrector class in correction.py.
    We'll replicate the logic here or refactor correction.py to check our constraints.
    Constraint: 'only integrated'. We shouldn't change correction.py.
    So we interpret 'integrated' as using the rules defined in pose_rules.py.
    """
    corrections = []
    
    if pose_name not in POSE_CORRECTION_RULES:
        return ["Great form! Keep it up."]
    
    rules = POSE_CORRECTION_RULES[pose_name]
    lm = landmarks.landmark
    
    for check in rules['checks']:
        feature = check['feature']
        message = check['message']
        
        val = 0
        tolerance = check.get('tolerance', 10) # default tolerance
        ideal = check.get('ideal', 0)
        
        # KNEE ANGLES
        if feature == 'left_knee_angle':
            val = calculate_angle(
                lm[mp_pose.PoseLandmark.LEFT_HIP],
                lm[mp_pose.PoseLandmark.LEFT_KNEE],
                lm[mp_pose.PoseLandmark.LEFT_ANKLE]
            )
            # Tolerance usually in degrees
            tolerance = check.get('tolerance', 10)
            if abs(val - ideal) > tolerance:
                corrections.append(f"{message} (Current: {int(val)}°, Ideal: {ideal}°)")
                
        elif feature == 'right_knee_angle':
            val = calculate_angle(
                lm[mp_pose.PoseLandmark.RIGHT_HIP],
                lm[mp_pose.PoseLandmark.RIGHT_KNEE],
                lm[mp_pose.PoseLandmark.RIGHT_ANKLE]
            )
            tolerance = check.get('tolerance', 10)
            if abs(val - ideal) > tolerance:
                corrections.append(f"{message} (Current: {int(val)}°, Ideal: {ideal}°)")

        # ELBOW ANGLES
        elif feature == 'left_elbow_angle':
            val = calculate_angle(
                lm[mp_pose.PoseLandmark.LEFT_SHOULDER],
                lm[mp_pose.PoseLandmark.LEFT_ELBOW],
                lm[mp_pose.PoseLandmark.LEFT_WRIST]
            )
            tolerance = check.get('tolerance', 15)
            if abs(val - ideal) > tolerance:
                corrections.append(f"{message} (Current: {int(val)}°, Ideal: {ideal}°)")
                
        elif feature == 'right_elbow_angle':
            val = calculate_angle(
                lm[mp_pose.PoseLandmark.RIGHT_SHOULDER],
                lm[mp_pose.PoseLandmark.RIGHT_ELBOW],
                lm[mp_pose.PoseLandmark.RIGHT_WRIST]
            )
            tolerance = check.get('tolerance', 15)
            if abs(val - ideal) > tolerance:
                corrections.append(f"{message} (Current: {int(val)}°, Ideal: {ideal}°)")

        # SPINE ANGLE
        elif feature == 'spine_angle':
            val = calculate_angle(
                lm[mp_pose.PoseLandmark.LEFT_SHOULDER],
                lm[mp_pose.PoseLandmark.LEFT_HIP],
                lm[mp_pose.PoseLandmark.LEFT_KNEE]
            )
            tolerance = check.get('tolerance', 15)
            if abs(val - ideal) > tolerance:
                corrections.append(f"{message} (Current: {int(val)}°, Ideal: {ideal}°)")

        # SHOULDER LEVEL
        elif feature == 'shoulder_level_diff':
            val = abs(lm[mp_pose.PoseLandmark.LEFT_SHOULDER].y - 
                      lm[mp_pose.PoseLandmark.RIGHT_SHOULDER].y)
            threshold = check.get('tolerance', 0.03)
            if val > threshold:
                corrections.append(message)

        # HIP LEVEL
        elif feature == 'hip_level_diff':
            val = abs(lm[mp_pose.PoseLandmark.LEFT_HIP].y - 
                      lm[mp_pose.PoseLandmark.RIGHT_HIP].y)
            threshold = check.get('tolerance', 0.03)
            if val > threshold:
                corrections.append(message)

        # FOOT DISTANCE
        elif feature == 'foot_distance':
            val = calculate_distance(
                lm[mp_pose.PoseLandmark.LEFT_ANKLE],
                lm[mp_pose.PoseLandmark.RIGHT_ANKLE]
            )
            min_dist = check.get('min', 0.3)
            if val < min_dist:
                corrections.append(message)

    # Only show "perfect" if no corrections AND confidence is high (>80%)
    if not corrections and confidence > 0.8:
        corrections.append("✅ posture perfect!")
    elif not corrections:
        # No corrections but low confidence - encourage better positioning
        corrections.append("Good form! Try to hold the pose more steadily.")
        
    return corrections

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
