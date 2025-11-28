import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import mediapipe as mp
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

pose = mp_pose.Pose(
    static_image_mode=True,
    model_complexity=2,
    enable_segmentation=False,
    min_detection_confidence=0.5
)

def calculate_angle(p1, p2, p3):
    """
    Calculate angle between three points (p1-p2-p3)
    p2 is the vertex (middle point)

    Args:
        p1, p2, p3: landmarks with .x, .y attributes

    Returns:
        angle in degrees
    """
    # Convert to numpy arrays
    a = np.array([p1.x, p1.y])
    b = np.array([p2.x, p2.y])
    c = np.array([p3.x, p3.y])

    # Calculate vectors
    ba = a - b
    bc = c - b

    # Calculate angle using dot product
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))

    return np.degrees(angle)

def calculate_distance(p1, p2):
    """Calculate Euclidean distance between two points"""
    return np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def extract_pose_features(landmarks):
    """
    Extract comprehensive features from pose landmarks

    Returns:
        numpy array of ~50 features
    """
    features = []

    # Get landmark shortcuts
    lm = landmarks.landmark

    # ==================== ANGLE FEATURES ====================

    # Left arm angles
    left_shoulder_angle = calculate_angle(
        lm[mp_pose.PoseLandmark.LEFT_ELBOW],
        lm[mp_pose.PoseLandmark.LEFT_SHOULDER],
        lm[mp_pose.PoseLandmark.LEFT_HIP]
    )
    features.append(left_shoulder_angle)

    left_elbow_angle = calculate_angle(
        lm[mp_pose.PoseLandmark.LEFT_SHOULDER],
        lm[mp_pose.PoseLandmark.LEFT_ELBOW],
        lm[mp_pose.PoseLandmark.LEFT_WRIST]
    )
    features.append(left_elbow_angle)

    # Right arm angles
    right_shoulder_angle = calculate_angle(
        lm[mp_pose.PoseLandmark.RIGHT_ELBOW],
        lm[mp_pose.PoseLandmark.RIGHT_SHOULDER],
        lm[mp_pose.PoseLandmark.RIGHT_HIP]
    )
    features.append(right_shoulder_angle)

    right_elbow_angle = calculate_angle(
        lm[mp_pose.PoseLandmark.RIGHT_SHOULDER],
        lm[mp_pose.PoseLandmark.RIGHT_ELBOW],
        lm[mp_pose.PoseLandmark.RIGHT_WRIST]
    )
    features.append(right_elbow_angle)

    # Left leg angles
    left_hip_angle = calculate_angle(
        lm[mp_pose.PoseLandmark.LEFT_SHOULDER],
        lm[mp_pose.PoseLandmark.LEFT_HIP],
        lm[mp_pose.PoseLandmark.LEFT_KNEE]
    )
    features.append(left_hip_angle)

    left_knee_angle = calculate_angle(
        lm[mp_pose.PoseLandmark.LEFT_HIP],
        lm[mp_pose.PoseLandmark.LEFT_KNEE],
        lm[mp_pose.PoseLandmark.LEFT_ANKLE]
    )
    features.append(left_knee_angle)

    # Right leg angles
    right_hip_angle = calculate_angle(
        lm[mp_pose.PoseLandmark.RIGHT_SHOULDER],
        lm[mp_pose.PoseLandmark.RIGHT_HIP],
        lm[mp_pose.PoseLandmark.RIGHT_KNEE]
    )
    features.append(right_hip_angle)

    right_knee_angle = calculate_angle(
        lm[mp_pose.PoseLandmark.RIGHT_HIP],
        lm[mp_pose.PoseLandmark.RIGHT_KNEE],
        lm[mp_pose.PoseLandmark.RIGHT_ANKLE]
    )
    features.append(right_knee_angle)

    # Spine/torso angles
    spine_angle = calculate_angle(
        lm[mp_pose.PoseLandmark.LEFT_SHOULDER],
        lm[mp_pose.PoseLandmark.LEFT_HIP],
        lm[mp_pose.PoseLandmark.LEFT_KNEE]
    )
    features.append(spine_angle)

    # Neck angle
    neck_angle = calculate_angle(
        lm[mp_pose.PoseLandmark.LEFT_SHOULDER],
        lm[mp_pose.PoseLandmark.NOSE],
        lm[mp_pose.PoseLandmark.LEFT_EAR]
    )
    features.append(neck_angle)

    # ==================== DISTANCE FEATURES ====================

    # Hand distance (for poses with hands together)
    hand_distance = calculate_distance(
        lm[mp_pose.PoseLandmark.LEFT_WRIST],
        lm[mp_pose.PoseLandmark.RIGHT_WRIST]
    )
    features.append(hand_distance)

    # Foot distance (for poses with wide stance)
    foot_distance = calculate_distance(
        lm[mp_pose.PoseLandmark.LEFT_ANKLE],
        lm[mp_pose.PoseLandmark.RIGHT_ANKLE]
    )
    features.append(foot_distance)

    # ==================== RATIO FEATURES (body size normalized) ====================

    # Calculate body height (shoulder to ankle)
    body_height = calculate_distance(
        lm[mp_pose.PoseLandmark.LEFT_SHOULDER],
        lm[mp_pose.PoseLandmark.LEFT_ANKLE]
    )

    # Arm length ratios
    left_arm_length = calculate_distance(
        lm[mp_pose.PoseLandmark.LEFT_SHOULDER],
        lm[mp_pose.PoseLandmark.LEFT_WRIST]
    )
    features.append(left_arm_length / (body_height + 1e-6))

    right_arm_length = calculate_distance(
        lm[mp_pose.PoseLandmark.RIGHT_SHOULDER],
        lm[mp_pose.PoseLandmark.RIGHT_WRIST]
    )
    features.append(right_arm_length / (body_height + 1e-6))

    # ==================== POSITION FEATURES ====================

    # Y-coordinates (height) of key points (normalized)
    features.append(lm[mp_pose.PoseLandmark.LEFT_WRIST].y)
    features.append(lm[mp_pose.PoseLandmark.RIGHT_WRIST].y)
    features.append(lm[mp_pose.PoseLandmark.LEFT_ANKLE].y)
    features.append(lm[mp_pose.PoseLandmark.RIGHT_ANKLE].y)
    features.append(lm[mp_pose.PoseLandmark.NOSE].y)

    # X-coordinates (width) - for left/right alignment
    features.append(lm[mp_pose.PoseLandmark.LEFT_SHOULDER].x)
    features.append(lm[mp_pose.PoseLandmark.RIGHT_SHOULDER].x)

    # ==================== SYMMETRY FEATURES ====================

    # Arm symmetry (difference between left and right)
    arm_symmetry = abs(left_elbow_angle - right_elbow_angle)
    features.append(arm_symmetry)

    # Leg symmetry
    leg_symmetry = abs(left_knee_angle - right_knee_angle)
    features.append(leg_symmetry)

    # Shoulder level difference
    shoulder_level = abs(lm[mp_pose.PoseLandmark.LEFT_SHOULDER].y -
                         lm[mp_pose.PoseLandmark.RIGHT_SHOULDER].y)
    features.append(shoulder_level)

    # Hip level difference
    hip_level = abs(lm[mp_pose.PoseLandmark.LEFT_HIP].y -
                    lm[mp_pose.PoseLandmark.RIGHT_HIP].y)
    features.append(hip_level)

    return np.array(features)

def process_image(image_path):
    """
    Process a single image and extract pose features.
    Returns:
        features (numpy array) or None if pose not detected
    """
    image = cv2.imread(image_path)
    if image is None:
        return None

    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Run MediaPipe
    results = pose.process(img_rgb)

    # If no pose → skip image
    if not results.pose_landmarks:
        return None

    # Extract features from landmarks
    features = extract_pose_features(results.pose_landmarks)

    return features

def load_dataset(dataset_path):
    X = []
    y = []
    pose_names = []

    # Get all pose folders
    pose_folders = sorted([f for f in os.listdir(dataset_path)
                          if os.path.isdir(os.path.join(dataset_path, f))])

    print(f"\nFound {len(pose_folders)} pose classes:")
    for i, pose in enumerate(pose_folders):
        print(f"   {i}: {pose}")

    # Process each pose class
    for pose_idx, pose_name in enumerate(pose_folders):
        pose_path = os.path.join(dataset_path, pose_name)
        image_files = [f for f in os.listdir(pose_path)
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

        print(f"\nProcessing {pose_name}: {len(image_files)} images...")

        success_count = 0
        for img_file in image_files:
            img_path = os.path.join(pose_path, img_file)
            features = process_image(img_path)

            if features is not None:
                X.append(features)
                y.append(pose_idx)
                success_count += 1

        print(f"Successfully processed: {success_count}/{len(image_files)} images")
        pose_names.append(pose_name)

    X = np.array(X)
    y = np.array(y)

    print(f"\nDataset loaded: {X.shape[0]} samples, {X.shape[1]} features")

    return X, y, pose_names

import cv2
import matplotlib.pyplot as plt

def draw_landmarks_with_names(image_rgb, results):
    """Draw skeleton + keypoint labels on the image."""
    if not results.pose_landmarks:
        return image_rgb

    lm = results.pose_landmarks.landmark

    # Draw skeleton
    mp_drawing.draw_landmarks(
        image_rgb,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS
    )

    # Draw keypoint names
    h, w = image_rgb.shape[:2]
    for i, landmark in enumerate(lm):
        cx, cy = int(landmark.x * w), int(landmark.y * h)
        name = mp_pose.PoseLandmark(i).name
        cv2.putText(image_rgb, name, (cx+5, cy-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255,0,0), 1)
    return image_rgb