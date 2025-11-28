import cv2
import numpy as np
import mediapipe as mp
import pickle
from collections import deque, Counter
from typing import List, Tuple, Dict, Optional
import time

from yoga_pose_classifier import (
    calculate_angle,
    calculate_distance, 
    extract_pose_features,
    process_image
)
from pose_rules import POSE_CORRECTION_RULES

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils


class RealtimePoseCorrector:
    def __init__(self, 
                 model_path='svm_classifier.pkl',
                 smoothing_window=7,
                 min_confidence=0.70,
                 min_hold_frames=10):
        """
        Initialize the corrector.
        Args:
            model_path: Path to trained SVM model pickle file
            smoothing_window: Number of frames to average predictions (default: 7)
            min_confidence: Minimum confidence to accept prediction (default: 0.70)
            min_hold_frames: Frames needed before showing corrections (default: 10)
        """
        print("Loading model...")
        with open(model_path, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.scaler = data['scaler']
            self.pose_names = data['pose_names']
        
        print(f"✓ Model loaded: {len(self.pose_names)} poses")
        
        # Temporal smoothing
        self.smoothing_window = smoothing_window
        self.pose_history = deque(maxlen=smoothing_window)
        self.confidence_history = deque(maxlen=smoothing_window)
        
        # Confidence filtering
        self.min_confidence = min_confidence
        
        # Pose stability
        self.min_hold_frames = min_hold_frames
        self.current_stable_pose = None
        self.pose_hold_count = 0
        
        # Performance tracking
        self.fps_history = deque(maxlen=30)
        self.last_frame_time = time.time()
        
        print(f"✓ Settings: {smoothing_window}-frame smoothing, {min_confidence:.0%} min confidence")
        print()
    
    def classify_pose(self, landmarks) -> Tuple[str, float]:
        """
        Classify pose from MediaPipe landmarks.
        
        Args:
            landmarks: MediaPipe pose landmarks
            
        Returns:
            (pose_name, confidence)
        """
        # Extract features using your function
        features = extract_pose_features(landmarks)
        
        # Normalize
        features_scaled = self.scaler.transform(features.reshape(1, -1))
        
        # Predict
        pose_idx = self.model.predict(features_scaled)[0]
        pose_name = self.pose_names[pose_idx]
        
        # Get confidence
        probabilities = self.model.predict_proba(features_scaled)[0]
        confidence = probabilities[pose_idx]
        
        return pose_name, confidence
    
    def get_smoothed_pose(self) -> Tuple[Optional[str], float]:
        """
        Get smoothed pose prediction from history buffer.
        
        Returns:
            (smoothed_pose_name, average_confidence) or (None, 0.0)
        """
        if len(self.pose_history) < 3:
            return None, 0.0
        
        # Count votes
        pose_counts = Counter(self.pose_history)
        most_common_pose, count = pose_counts.most_common(1)[0]
        
        # Must appear in >60% of frames
        if count < len(self.pose_history) * 0.6:
            return None, 0.0
        
        # Calculate average confidence for this pose
        avg_confidence = np.mean([
            conf for pose, conf in zip(self.pose_history, self.confidence_history)
            if pose == most_common_pose
        ])
        
        return most_common_pose, avg_confidence
    
    def check_corrections(self, landmarks, pose_name: str) -> List[str]:
        """
        Check pose against correction rules.
        
        Args:
            landmarks: MediaPipe pose landmarks
            pose_name: Detected pose name
            
        Returns:
            List of correction messages
        """
        corrections = []
        
        # Check if we have rules for this pose
        if pose_name not in POSE_CORRECTION_RULES:
            return ["Great form!"]
        
        rules = POSE_CORRECTION_RULES[pose_name]
        lm = landmarks.landmark
        
        # Check each rule
        for check in rules['checks']:
            feature = check['feature']
            priority = check.get('priority', 'medium')
            message = check['message']
            
            # KNEE ANGLES
            if feature in ['left_knee_angle', 'right_knee_angle']:
                if feature == 'left_knee_angle':
                    angle = calculate_angle(
                        lm[mp_pose.PoseLandmark.LEFT_HIP],
                        lm[mp_pose.PoseLandmark.LEFT_KNEE],
                        lm[mp_pose.PoseLandmark.LEFT_ANKLE]
                    )
                else:
                    angle = calculate_angle(
                        lm[mp_pose.PoseLandmark.RIGHT_HIP],
                        lm[mp_pose.PoseLandmark.RIGHT_KNEE],
                        lm[mp_pose.PoseLandmark.RIGHT_ANKLE]
                    )
                
                ideal = check.get('ideal', 180)
                tolerance = check.get('tolerance', 10)
                
                if abs(angle - ideal) > tolerance:
                    corrections.append(f"{message} (now: {angle:.0f}°, target: {ideal}°)")
            
            # ELBOW ANGLES
            elif feature in ['left_elbow_angle', 'right_elbow_angle']:
                if feature == 'left_elbow_angle':
                    angle = calculate_angle(
                        lm[mp_pose.PoseLandmark.LEFT_SHOULDER],
                        lm[mp_pose.PoseLandmark.LEFT_ELBOW],
                        lm[mp_pose.PoseLandmark.LEFT_WRIST]
                    )
                else:
                    angle = calculate_angle(
                        lm[mp_pose.PoseLandmark.RIGHT_SHOULDER],
                        lm[mp_pose.PoseLandmark.RIGHT_ELBOW],
                        lm[mp_pose.PoseLandmark.RIGHT_WRIST]
                    )
                
                ideal = check.get('ideal', 180)
                tolerance = check.get('tolerance', 15)
                
                if abs(angle - ideal) > tolerance:
                    corrections.append(f"{message} (now: {angle:.0f}°, target: {ideal}°)")
            
            # SPINE ANGLE
            elif feature == 'spine_angle':
                spine = calculate_angle(
                    lm[mp_pose.PoseLandmark.LEFT_SHOULDER],
                    lm[mp_pose.PoseLandmark.LEFT_HIP],
                    lm[mp_pose.PoseLandmark.LEFT_KNEE]
                )
                
                ideal = check.get('ideal', 170)
                tolerance = check.get('tolerance', 15)
                
                if abs(spine - ideal) > tolerance:
                    corrections.append(f"{message} (now: {spine:.0f}°, target: {ideal}°)")
            
            # SHOULDER LEVEL
            elif feature == 'shoulder_level_diff':
                diff = abs(lm[mp_pose.PoseLandmark.LEFT_SHOULDER].y - 
                          lm[mp_pose.PoseLandmark.RIGHT_SHOULDER].y)
                
                threshold = check.get('tolerance', 0.03)
                
                if diff > threshold:
                    corrections.append(message)
            
            # HIP LEVEL
            elif feature == 'hip_level_diff':
                diff = abs(lm[mp_pose.PoseLandmark.LEFT_HIP].y - 
                          lm[mp_pose.PoseLandmark.RIGHT_HIP].y)
                
                threshold = check.get('tolerance', 0.03)
                
                if diff > threshold:
                    corrections.append(message)
            
            # FOOT DISTANCE
            elif feature == 'foot_distance':
                dist = calculate_distance(
                    lm[mp_pose.PoseLandmark.LEFT_ANKLE],
                    lm[mp_pose.PoseLandmark.RIGHT_ANKLE]
                )
                
                min_dist = check.get('min', 0.3)
                
                if dist < min_dist:
                    corrections.append(message)
        
        # If no corrections, pose is good!
        if not corrections:
            corrections.append("✅ Excellent form!")
        
        return corrections
    
    def calculate_fps(self) -> float:
        """Calculate current FPS."""
        current_time = time.time()
        fps = 1.0 / (current_time - self.last_frame_time + 1e-6)
        self.last_frame_time = current_time
        self.fps_history.append(fps)
        return np.mean(self.fps_history)
    
    def process_frame(self, frame):
        """
        Process a single video frame.
        
        Args:
            frame: OpenCV BGR image
            
        Returns:
            annotated_frame: Frame with overlays
            pose_name: Detected pose (or status message)
            corrections: List of corrections
            confidence: Confidence score
            fps: Current FPS
        """
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Use video-optimized MediaPipe settings
        with mp_pose.Pose(
            static_image_mode=False,      # Video mode (tracking)
            model_complexity=1,            # Balanced speed/accuracy
            smooth_landmarks=True,         # Reduce jitter
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as pose_detector:
            
            results = pose_detector.process(frame_rgb)
            fps = self.calculate_fps()
            
            # No pose detected
            if not results.pose_landmarks:
                cv2.putText(frame, "No pose detected", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                cv2.putText(frame, f"FPS: {fps:.1f}", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                return frame, None, [], 0.0, fps
            
            # Draw skeleton
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
            )
            
            # Classify pose
            raw_pose, raw_confidence = self.classify_pose(results.pose_landmarks)
            
            # Add to history
            self.pose_history.append(raw_pose)
            self.confidence_history.append(raw_confidence)
            
            # Get smoothed prediction
            smoothed_pose, avg_confidence = self.get_smoothed_pose()
            
            # Warming up
            if smoothed_pose is None:
                self._draw_info(frame, "Detecting...", [], 0.0, fps, 
                              f"Buffer: {len(self.pose_history)}/{self.smoothing_window}")
                return frame, "Detecting...", [], 0.0, fps
            
            # Low confidence
            if avg_confidence < self.min_confidence:
                self._draw_info(frame, "Uncertain", ["Move into clearer pose"], 
                              avg_confidence, fps, "Low confidence")
                return frame, "Uncertain", ["Move into clearer pose"], avg_confidence, fps
            
            # Check stability
            if smoothed_pose == self.current_stable_pose:
                self.pose_hold_count += 1
            else:
                self.current_stable_pose = smoothed_pose
                self.pose_hold_count = 1
            
            # Not held long enough
            if self.pose_hold_count < self.min_hold_frames:
                status = f"Stabilizing ({self.pose_hold_count}/{self.min_hold_frames})"
                self._draw_info(frame, smoothed_pose, [], avg_confidence, fps, status)
                return frame, smoothed_pose, [], avg_confidence, fps
            
            # Pose is stable - check corrections!
            corrections = self.check_corrections(results.pose_landmarks, smoothed_pose)
            
            self._draw_info(frame, smoothed_pose, corrections, avg_confidence, fps, "✓ Locked")
            
            return frame, smoothed_pose, corrections, avg_confidence, fps
    
    def _draw_info(self, frame, pose_name, corrections, confidence, fps, status):
        """Draw information overlay on frame."""
        h, w = frame.shape[:2]
        
        # Semi-transparent background
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, 220), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        
        y = 30
        
        # Pose name
        color = (0, 255, 0) if "✓" in status else (0, 255, 255)
        cv2.putText(frame, f"Pose: {pose_name}", (10, y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        y += 30
        
        # Confidence
        if confidence > 0:
            conf_color = (0, 255, 0) if confidence > 0.85 else (0, 255, 255)
            cv2.putText(frame, f"Confidence: {confidence:.0%}", (10, y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, conf_color, 2)
            y += 25
        
        # Status
        status_color = (0, 255, 0) if "✓" in status else (255, 255, 0)
        cv2.putText(frame, f"Status: {status}", (10, y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, status_color, 1)
        y += 30
        
        # Corrections
        if corrections and "✓" in status:
            cv2.putText(frame, "Feedback:", (10, y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            y += 25
            
            for i, correction in enumerate(corrections[:3]):  # Max 3
                if '✅' in correction:
                    text_color = (0, 255, 0)
                    text = correction
                else:
                    text_color = (0, 200, 255)
                    text = f"{i+1}. {correction}"
                
                cv2.putText(frame, text, (15, y),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.45, text_color, 1)
                y += 22
        
        # FPS (top right)
        fps_text = f"FPS: {fps:.1f}"
        text_size = cv2.getTextSize(fps_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)[0]
        cv2.putText(frame, fps_text, (w - text_size[0] - 10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)


def main():
    """Main function to run real-time pose correction."""
    print("\n" + "="*60)
    print("  REAL-TIME YOGA POSE CORRECTION")
    print("="*60)
    print()
    
    # Initialize corrector
    try:
        corrector = RealtimePoseCorrector('svm_classifier.pkl')
    except FileNotFoundError:
        print("Error: svm_classifier.pkl not found!")
        print("   Make sure the model file is in the same directory.")
        return
    
    # Open webcam
    print("Opening webcam...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    print("✓ Webcam opened")
    print()
    print("Controls:")
    print("  'q' - Quit")
    print("  's' - Save screenshot")
    print()
    print("Starting...\n")
    
    frame_count = 0
    
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            
            # Process frame
            frame, pose, corrections, conf, fps = corrector.process_frame(frame)
            frame_count += 1
            
            # Display
            cv2.imshow('Yoga Pose Correction - Press Q to quit', frame)
            
            # Handle keys
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                print("\nQuitting...")
                break
            elif key == ord('s'):
                filename = f'yoga_correction_{frame_count}.jpg'
                cv2.imwrite(filename, frame)
                print(f"📸 Screenshot saved: {filename}")
    
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        
        print(f"\n{'='*60}")
        print("SESSION COMPLETE")
        print(f"{'='*60}")
        print(f"Total frames processed: {frame_count}")
        if corrector.fps_history:
            print(f"Average FPS: {np.mean(corrector.fps_history):.1f}")
        print()


if __name__ == "__main__":
    main()