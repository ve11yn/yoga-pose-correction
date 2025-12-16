"""
Enhanced Pose Corrector with Visual Body Outline and Alignment Guides
"""

import cv2
import numpy as np
import mediapipe as mp
import pickle
from collections import deque, Counter, defaultdict
from typing import List, Tuple, Dict, Optional
import time

from yoga_pose_classifier import (
    calculate_angle,
    calculate_distance, 
    extract_pose_features,
    process_image
)
from enhanced_pose_rules import POSE_CORRECTION_RULES, PRIORITY_WEIGHTS

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils


class VisualPoseCorrector:
    def __init__(self, 
                 model_path='svm_classifier.pkl',
                 smoothing_window=7,
                 min_confidence=0.70,
                 min_hold_frames=10,
                 max_corrections=3,
                 show_ideal_overlay=True,
                 mirror_display: bool = True):
        """
        Initialize the visual corrector with body outline.
        Args:
            show_ideal_overlay: Show ideal pose overlay as reference
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
        
        # Correction tracking
        self.max_corrections = max_corrections
        self.correction_history = defaultdict(lambda: deque(maxlen=5))
        self.persistent_issues = defaultdict(int)
        self.problem_joints = set()  # Track which joints have issues
        
        # Performance tracking
        self.fps_history = deque(maxlen=30)
        self.last_frame_time = time.time()
        
        # Quality metrics
        self.pose_quality_score = 0.0
        self.quality_history = deque(maxlen=10)
        
        # Visual settings
        self.show_ideal_overlay = show_ideal_overlay
        self.show_alignment_guides = True
        # If True, flip frames horizontally before processing and drawing
        # Useful because MediaPipe labels joints by the subject's anatomical
        # left/right which can look mirrored to the user. Enabling this
        # makes the overlay behave like a mirror (user-right == overlay-right).
        self.mirror_display = mirror_display
        
        print(f"✓ Settings: {smoothing_window}-frame smoothing, {min_confidence:.0%} min confidence")
        print(f"✓ Visual feedback enabled")
        print()
    
    def classify_pose(self, landmarks) -> Tuple[str, float]:
        """Classify pose from MediaPipe landmarks."""
        features = extract_pose_features(landmarks)
        features_scaled = self.scaler.transform(features.reshape(1, -1))
        
        pose_idx = self.model.predict(features_scaled)[0]
        pose_name = self.pose_names[pose_idx]
        
        probabilities = self.model.predict_proba(features_scaled)[0]
        confidence = probabilities[pose_idx]
        
        return pose_name, confidence
    
    def get_smoothed_pose(self) -> Tuple[Optional[str], float]:
        """Get smoothed pose prediction from history buffer."""
        if len(self.pose_history) < 3:
            return None, 0.0
        
        pose_counts = Counter(self.pose_history)
        most_common_pose, count = pose_counts.most_common(1)[0]
        
        if count < len(self.pose_history) * 0.6:
            return None, 0.0
        
        avg_confidence = np.mean([
            conf for pose, conf in zip(self.pose_history, self.confidence_history)
            if pose == most_common_pose
        ])
        
        return most_common_pose, avg_confidence
    
    def check_corrections(self, landmarks, pose_name: str) -> Tuple[List[Dict], float]:
        """Check pose against correction rules and identify problem joints."""
        if pose_name not in POSE_CORRECTION_RULES:
            return [{'type': 'info', 'message': 'Great form!', 'priority': 1}], 1.0
        
        rules = POSE_CORRECTION_RULES[pose_name]
        lm = landmarks.landmark
        corrections = []
        total_checks = 0
        passed_checks = 0
        self.problem_joints.clear()  # Reset for this frame
        
        for check in rules['checks']:
            feature = check['feature']
            priority = check.get('priority', 'medium')
            body_part = check.get('body_part', 'general')
            
            total_checks += 1
            correction_found = False
            
            # KNEE ANGLES
            if feature in ['left_knee_angle', 'right_knee_angle', 'standing_knee_angle', 
                          'raised_knee_angle', 'front_knee_angle', 'back_knee_angle']:
                angle = self._calculate_knee_angle(lm, feature)
                if angle is not None:
                    result = self._check_angle(angle, check)
                    if result:
                        corrections.append({
                            'type': result['type'],
                            'message': result['message'],
                            'priority': PRIORITY_WEIGHTS[priority],
                            'body_part': body_part,
                            'feature': feature,
                            'current': angle,
                            'target': check.get('ideal')
                        })
                        correction_found = True
                        self.persistent_issues[feature] += 1
                        # Mark problem joints
                        if 'left' in feature:
                            self.problem_joints.add('LEFT_KNEE')
                        elif 'right' in feature:
                            self.problem_joints.add('RIGHT_KNEE')
                    else:
                        passed_checks += 1
            
            # ELBOW ANGLES
            elif feature in ['left_elbow_angle', 'right_elbow_angle']:
                angle = self._calculate_elbow_angle(lm, feature)
                if angle is not None:
                    result = self._check_angle(angle, check)
                    if result:
                        corrections.append({
                            'type': result['type'],
                            'message': result['message'],
                            'priority': PRIORITY_WEIGHTS[priority],
                            'body_part': body_part,
                            'feature': feature,
                            'current': angle,
                            'target': check.get('ideal')
                        })
                        correction_found = True
                        self.persistent_issues[feature] += 1
                        # Mark problem joints
                        if 'left' in feature:
                            self.problem_joints.add('LEFT_ELBOW')
                        elif 'right' in feature:
                            self.problem_joints.add('RIGHT_ELBOW')
                    else:
                        passed_checks += 1
            
            # SPINE ANGLE
            elif feature == 'spine_angle':
                spine = calculate_angle(
                    lm[mp_pose.PoseLandmark.LEFT_SHOULDER],
                    lm[mp_pose.PoseLandmark.LEFT_HIP],
                    lm[mp_pose.PoseLandmark.LEFT_KNEE]
                )
                result = self._check_angle(spine, check)
                if result:
                    corrections.append({
                        'type': result['type'],
                        'message': result['message'],
                        'priority': PRIORITY_WEIGHTS[priority],
                        'body_part': body_part,
                        'feature': feature,
                        'current': spine,
                        'target': check.get('ideal')
                    })
                    correction_found = True
                    self.problem_joints.update(['LEFT_SHOULDER', 'LEFT_HIP'])
                else:
                    passed_checks += 1
            
            # SHOULDER LEVEL
            elif feature == 'shoulder_level_diff':
                diff = abs(lm[mp_pose.PoseLandmark.LEFT_SHOULDER].y - 
                          lm[mp_pose.PoseLandmark.RIGHT_SHOULDER].y)
                result = self._check_distance(diff, check)
                if result:
                    corrections.append({
                        'type': result['type'],
                        'message': result['message'],
                        'priority': PRIORITY_WEIGHTS[priority],
                        'body_part': body_part,
                        'feature': feature
                    })
                    correction_found = True
                    self.problem_joints.update(['LEFT_SHOULDER', 'RIGHT_SHOULDER'])
                else:
                    passed_checks += 1
            
            # HIP LEVEL
            elif feature == 'hip_level_diff':
                diff = abs(lm[mp_pose.PoseLandmark.LEFT_HIP].y - 
                          lm[mp_pose.PoseLandmark.RIGHT_HIP].y)
                result = self._check_distance(diff, check)
                if result:
                    corrections.append({
                        'type': result['type'],
                        'message': result['message'],
                        'priority': PRIORITY_WEIGHTS[priority],
                        'body_part': body_part,
                        'feature': feature
                    })
                    correction_found = True
                    self.problem_joints.update(['LEFT_HIP', 'RIGHT_HIP'])
                else:
                    passed_checks += 1
            
            # FOOT DISTANCE
            elif feature == 'foot_distance':
                dist = calculate_distance(
                    lm[mp_pose.PoseLandmark.LEFT_ANKLE],
                    lm[mp_pose.PoseLandmark.RIGHT_ANKLE]
                )
                if 'min' in check:
                    warning_min = check.get('warning_min', check['min'])
                    if dist < check['min']:
                        corrections.append({
                            'type': 'critical',
                            'message': check['message'],
                            'priority': PRIORITY_WEIGHTS[priority],
                            'body_part': body_part,
                            'feature': feature
                        })
                        correction_found = True
                        self.problem_joints.update(['LEFT_ANKLE', 'RIGHT_ANKLE'])
                    elif dist < warning_min:
                        corrections.append({
                            'type': 'warning',
                            'message': check.get('warning_message', check['message']),
                            'priority': PRIORITY_WEIGHTS[priority] - 1,
                            'body_part': body_part,
                            'feature': feature
                        })
                        correction_found = True
                        self.problem_joints.update(['LEFT_ANKLE', 'RIGHT_ANKLE'])
                    else:
                        passed_checks += 1
            
            # BODY ALIGNMENT
            elif feature == 'body_alignment':
                alignment_check = self._check_body_alignment(lm, check)
                if alignment_check:
                    corrections.append({
                        'type': alignment_check['type'],
                        'message': alignment_check['message'],
                        'priority': PRIORITY_WEIGHTS[priority],
                        'body_part': body_part,
                        'feature': feature
                    })
                    correction_found = True
                    self.problem_joints.update(['LEFT_HIP', 'RIGHT_HIP'])
                else:
                    passed_checks += 1
            
            if not correction_found and feature in self.persistent_issues:
                self.persistent_issues[feature] = max(0, self.persistent_issues[feature] - 1)
        
        # Calculate quality score
        quality_score = passed_checks / total_checks if total_checks > 0 else 0.0
        self.quality_history.append(quality_score)
        self.pose_quality_score = np.mean(self.quality_history)
        
        if not corrections:
            return [{'type': 'success', 'message': '✅ Excellent form!', 'priority': 0}], quality_score
        
        corrections.sort(key=lambda x: (
            -x['priority'],
            -self.persistent_issues.get(x.get('feature', ''), 0)
        ))
        
        grouped = self._group_corrections_by_body_part(corrections)
        
        return grouped[:self.max_corrections], quality_score
    
    def _draw_enhanced_skeleton(self, frame, landmarks, quality_score):
        """Draw enhanced skeleton with color-coded joints and alignment guides."""
        h, w, _ = frame.shape
        lm = landmarks.landmark
        
        # Define connections with better grouping
        body_connections = [
            # Torso
            ('LEFT_SHOULDER', 'RIGHT_SHOULDER'),
            ('LEFT_SHOULDER', 'LEFT_HIP'),
            ('RIGHT_SHOULDER', 'RIGHT_HIP'),
            ('LEFT_HIP', 'RIGHT_HIP'),
            
            # Left arm
            ('LEFT_SHOULDER', 'LEFT_ELBOW'),
            ('LEFT_ELBOW', 'LEFT_WRIST'),
            
            # Right arm
            ('RIGHT_SHOULDER', 'RIGHT_ELBOW'),
            ('RIGHT_ELBOW', 'RIGHT_WRIST'),
            
            # Left leg
            ('LEFT_HIP', 'LEFT_KNEE'),
            ('LEFT_KNEE', 'LEFT_ANKLE'),
            
            # Right leg
            ('RIGHT_HIP', 'RIGHT_KNEE'),
            ('RIGHT_KNEE', 'RIGHT_ANKLE'),
        ]
        
        # Draw connections (bones)
        for connection in body_connections:
            start_name, end_name = connection
            start_idx = getattr(mp_pose.PoseLandmark, start_name)
            end_idx = getattr(mp_pose.PoseLandmark, end_name)
            
            start_point = lm[start_idx]
            end_point = lm[end_idx]
            
            # Check if either joint has problems
            has_problem = start_name in self.problem_joints or end_name in self.problem_joints
            
            # Color based on quality and problems
            if has_problem:
                color = (0, 100, 255)  # Orange for problem areas
                thickness = 3
            elif quality_score > 0.8:
                color = (0, 255, 0)  # Green for good form
                thickness = 2
            elif quality_score > 0.6:
                color = (0, 255, 255)  # Yellow for okay form
                thickness = 2
            else:
                color = (0, 165, 255)  # Orange for poor form
                thickness = 2
            
            start_coords = (int(start_point.x * w), int(start_point.y * h))
            end_coords = (int(end_point.x * w), int(end_point.y * h))
            
            cv2.line(frame, start_coords, end_coords, color, thickness)
        
        # Draw joints (circles)
        for landmark_name in mp_pose.PoseLandmark.__members__:
            if landmark_name in ['LEFT_EYE', 'RIGHT_EYE', 'LEFT_EAR', 'RIGHT_EAR',
                                'MOUTH_LEFT', 'MOUTH_RIGHT', 'NOSE',
                                'LEFT_EYE_INNER', 'LEFT_EYE_OUTER',
                                'RIGHT_EYE_INNER', 'RIGHT_EYE_OUTER',
                                'LEFT_PINKY', 'RIGHT_PINKY',
                                'LEFT_INDEX', 'RIGHT_INDEX',
                                'LEFT_THUMB', 'RIGHT_THUMB',
                                'LEFT_HEEL', 'RIGHT_HEEL',
                                'LEFT_FOOT_INDEX', 'RIGHT_FOOT_INDEX']:
                continue  # Skip facial landmarks and extra hand/foot points
            
            landmark_idx = getattr(mp_pose.PoseLandmark, landmark_name)
            point = lm[landmark_idx]
            coords = (int(point.x * w), int(point.y * h))
            
            # Determine joint color
            if landmark_name in self.problem_joints:
                joint_color = (0, 0, 255)  # Red for problem joints
                radius = 8
                thickness = -1  # Filled
            elif quality_score > 0.8:
                joint_color = (0, 255, 0)  # Green
                radius = 5
                thickness = -1
            else:
                joint_color = (0, 255, 255)  # Yellow
                radius = 5
                thickness = -1
            
            cv2.circle(frame, coords, radius, joint_color, thickness)
            
            # Draw outer ring for problem joints
            if landmark_name in self.problem_joints:
                cv2.circle(frame, coords, radius + 3, (0, 0, 255), 2)
    
    def _draw_alignment_guides(self, frame, landmarks):
        """Draw alignment guides for better posture reference."""
        h, w, _ = frame.shape
        lm = landmarks.landmark
        
        # Vertical alignment line (center of body)
        left_shoulder = lm[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        center_x = int((left_shoulder.x + right_shoulder.x) / 2 * w)
        
        # Draw vertical center line
        cv2.line(frame, (center_x, 0), (center_x, h), (100, 100, 100), 1, cv2.LINE_AA)
        
        # Horizontal lines for shoulder and hip alignment
        shoulder_y = int((left_shoulder.y + right_shoulder.y) / 2 * h)
        left_hip = lm[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = lm[mp_pose.PoseLandmark.RIGHT_HIP]
        hip_y = int((left_hip.y + right_hip.y) / 2 * h)
        
        # Check if shoulders are level
        shoulder_diff = abs(left_shoulder.y - right_shoulder.y)
        shoulder_color = (0, 255, 0) if shoulder_diff < 0.03 else (0, 165, 255)
        cv2.line(frame, (0, shoulder_y), (w, shoulder_y), shoulder_color, 1, cv2.LINE_AA)
        
        # Check if hips are level
        hip_diff = abs(left_hip.y - right_hip.y)
        hip_color = (0, 255, 0) if hip_diff < 0.03 else (0, 165, 255)
        cv2.line(frame, (0, hip_y), (w, hip_y), hip_color, 1, cv2.LINE_AA)
        
        # Draw angle indicators for key joints with problems
        if 'LEFT_KNEE' in self.problem_joints or 'RIGHT_KNEE' in self.problem_joints:
            self._draw_angle_indicator(frame, landmarks, 'knee')
        
        if 'LEFT_ELBOW' in self.problem_joints or 'RIGHT_ELBOW' in self.problem_joints:
            self._draw_angle_indicator(frame, landmarks, 'elbow')
    
    def _draw_angle_indicator(self, frame, landmarks, joint_type):
        """Draw angle arc indicator at problem joints."""
        h, w, _ = frame.shape
        lm = landmarks.landmark
        
        if joint_type == 'knee':
            # Draw for both knees if they have problems
            if 'LEFT_KNEE' in self.problem_joints:
                hip = lm[mp_pose.PoseLandmark.LEFT_HIP]
                knee = lm[mp_pose.PoseLandmark.LEFT_KNEE]
                ankle = lm[mp_pose.PoseLandmark.LEFT_ANKLE]
                angle = calculate_angle(hip, knee, ankle)
                
                knee_coords = (int(knee.x * w), int(knee.y * h))
                cv2.putText(frame, f"{angle:.0f}°", 
                          (knee_coords[0] + 10, knee_coords[1] - 10),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            
            if 'RIGHT_KNEE' in self.problem_joints:
                hip = lm[mp_pose.PoseLandmark.RIGHT_HIP]
                knee = lm[mp_pose.PoseLandmark.RIGHT_KNEE]
                ankle = lm[mp_pose.PoseLandmark.RIGHT_ANKLE]
                angle = calculate_angle(hip, knee, ankle)
                
                knee_coords = (int(knee.x * w), int(knee.y * h))
                cv2.putText(frame, f"{angle:.0f}°", 
                          (knee_coords[0] + 10, knee_coords[1] - 10),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
        elif joint_type == 'elbow':
            if 'LEFT_ELBOW' in self.problem_joints:
                shoulder = lm[mp_pose.PoseLandmark.LEFT_SHOULDER]
                elbow = lm[mp_pose.PoseLandmark.LEFT_ELBOW]
                wrist = lm[mp_pose.PoseLandmark.LEFT_WRIST]
                angle = calculate_angle(shoulder, elbow, wrist)
                
                elbow_coords = (int(elbow.x * w), int(elbow.y * h))
                cv2.putText(frame, f"{angle:.0f}°", 
                          (elbow_coords[0] + 10, elbow_coords[1] - 10),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            
            if 'RIGHT_ELBOW' in self.problem_joints:
                shoulder = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                elbow = lm[mp_pose.PoseLandmark.RIGHT_ELBOW]
                wrist = lm[mp_pose.PoseLandmark.RIGHT_WRIST]
                angle = calculate_angle(shoulder, elbow, wrist)
                
                elbow_coords = (int(elbow.x * w), int(elbow.y * h))
                cv2.putText(frame, f"{angle:.0f}°", 
                          (elbow_coords[0] + 10, elbow_coords[1] - 10),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
    def _calculate_knee_angle(self, lm, feature: str) -> Optional[float]:
        """Calculate knee angle based on feature name."""
        if feature == 'left_knee_angle' or feature == 'standing_knee_angle':
            return calculate_angle(
                lm[mp_pose.PoseLandmark.LEFT_HIP],
                lm[mp_pose.PoseLandmark.LEFT_KNEE],
                lm[mp_pose.PoseLandmark.LEFT_ANKLE]
            )
        elif feature == 'right_knee_angle' or feature == 'raised_knee_angle':
            return calculate_angle(
                lm[mp_pose.PoseLandmark.RIGHT_HIP],
                lm[mp_pose.PoseLandmark.RIGHT_KNEE],
                lm[mp_pose.PoseLandmark.RIGHT_ANKLE]
            )
        elif feature == 'front_knee_angle':
            left_angle = calculate_angle(
                lm[mp_pose.PoseLandmark.LEFT_HIP],
                lm[mp_pose.PoseLandmark.LEFT_KNEE],
                lm[mp_pose.PoseLandmark.LEFT_ANKLE]
            )
            right_angle = calculate_angle(
                lm[mp_pose.PoseLandmark.RIGHT_HIP],
                lm[mp_pose.PoseLandmark.RIGHT_KNEE],
                lm[mp_pose.PoseLandmark.RIGHT_ANKLE]
            )
            return min(left_angle, right_angle)
        elif feature == 'back_knee_angle':
            left_angle = calculate_angle(
                lm[mp_pose.PoseLandmark.LEFT_HIP],
                lm[mp_pose.PoseLandmark.LEFT_KNEE],
                lm[mp_pose.PoseLandmark.LEFT_ANKLE]
            )
            right_angle = calculate_angle(
                lm[mp_pose.PoseLandmark.RIGHT_HIP],
                lm[mp_pose.PoseLandmark.RIGHT_KNEE],
                lm[mp_pose.PoseLandmark.RIGHT_ANKLE]
            )
            return max(left_angle, right_angle)
        return None
    
    def _calculate_elbow_angle(self, lm, feature: str) -> Optional[float]:
        """Calculate elbow angle based on feature name."""
        if feature == 'left_elbow_angle':
            return calculate_angle(
                lm[mp_pose.PoseLandmark.LEFT_SHOULDER],
                lm[mp_pose.PoseLandmark.LEFT_ELBOW],
                lm[mp_pose.PoseLandmark.LEFT_WRIST]
            )
        elif feature == 'right_elbow_angle':
            return calculate_angle(
                lm[mp_pose.PoseLandmark.RIGHT_SHOULDER],
                lm[mp_pose.PoseLandmark.RIGHT_ELBOW],
                lm[mp_pose.PoseLandmark.RIGHT_WRIST]
            )
        return None
    
    def _check_angle(self, angle: float, check: Dict) -> Optional[Dict]:
        """Check if angle meets requirements with two-tier validation."""
        ideal = check.get('ideal', 180)
        tolerance = check.get('tolerance', 10)
        warning_tolerance = check.get('warning_tolerance', tolerance * 1.5)
        
        deviation = abs(angle - ideal)
        
        if 'safety_check' in check:
            safety = check['safety_check']
            if 'min_angle' in safety and angle < safety['min_angle']:
                return {'type': 'critical', 'message': safety['warning']}
            if 'max_angle' in safety and angle > safety['max_angle']:
                return {'type': 'critical', 'message': safety['warning']}
        
        if deviation > tolerance:
            return {'type': 'critical', 'message': check['message']}
        elif deviation > tolerance * 0.7:
            return {'type': 'warning', 'message': check.get('warning_message', check['message'])}
        
        return None
    
    def _check_distance(self, distance: float, check: Dict) -> Optional[Dict]:
        """Check if distance meets requirements."""
        tolerance = check.get('tolerance', 0.05)
        
        if distance > tolerance:
            return {'type': 'critical', 'message': check['message']}
        elif distance > tolerance * 0.7:
            return {'type': 'warning', 'message': check.get('warning_message', check['message'])}
        
        return None
    
    def _check_body_alignment(self, lm, check: Dict) -> Optional[Dict]:
        """Check body alignment for plank pose."""
        shoulder_y = (lm[mp_pose.PoseLandmark.LEFT_SHOULDER].y + 
                     lm[mp_pose.PoseLandmark.RIGHT_SHOULDER].y) / 2
        hip_y = (lm[mp_pose.PoseLandmark.LEFT_HIP].y + 
                lm[mp_pose.PoseLandmark.RIGHT_HIP].y) / 2
        
        tolerance = check.get('tolerance', 0.05)
        
        if hip_y > shoulder_y + tolerance:
            if 'sub_checks' in check and 'hip_sag' in check['sub_checks']:
                return {'type': 'critical', 'message': check['sub_checks']['hip_sag']['message']}
            return {'type': 'critical', 'message': check['message']}
        
        elif hip_y < shoulder_y - tolerance:
            if 'sub_checks' in check and 'hip_pike' in check['sub_checks']:
                return {'type': 'critical', 'message': check['sub_checks']['hip_pike']['message']}
            return {'type': 'critical', 'message': check['message']}
        
        return None
    
    def _group_corrections_by_body_part(self, corrections: List[Dict]) -> List[Dict]:
        """Group similar corrections for clearer feedback."""
        grouped = []
        seen_parts = set()
        
        for corr in corrections:
            body_part = corr.get('body_part', 'general')
            
            if body_part in ['leg', 'arm'] and body_part in seen_parts:
                for existing in grouped:
                    if existing.get('body_part') == body_part and existing['type'] == corr['type']:
                        existing['message'] = existing['message'].replace('left', 'both').replace('right', 'both')
                        break
            else:
                grouped.append(corr)
                seen_parts.add(body_part)
        
        return grouped
    
    def calculate_fps(self) -> float:
        """Calculate current FPS."""
        current_time = time.time()
        fps = 1.0 / (current_time - self.last_frame_time + 1e-6)
        self.last_frame_time = current_time
        self.fps_history.append(fps)
        return np.mean(self.fps_history)
    
    def process_frame(self, frame):
        """Process frame with enhanced visual feedback."""
        # Optionally mirror the displayed frame so the overlay matches
        # the user's mirror-like expectation (user-right == overlay-right).
        if getattr(self, 'mirror_display', True):
            frame = cv2.flip(frame, 1)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        with mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as pose_detector:
            
            results = pose_detector.process(frame_rgb)
            fps = self.calculate_fps()
            
            if not results.pose_landmarks:
                self._draw_info(frame, "No pose detected", [], 0.0, fps, 
                              "Move into camera view", 0.0)
                return frame, None, [], 0.0, fps
            
            # Classify pose first
            raw_pose, raw_confidence = self.classify_pose(results.pose_landmarks)
            self.pose_history.append(raw_pose)
            self.confidence_history.append(raw_confidence)
            
            smoothed_pose, avg_confidence = self.get_smoothed_pose()
            
            if smoothed_pose is None:
                self._draw_info(frame, "Detecting...", [], 0.0, fps, 
                              f"Buffer: {len(self.pose_history)}/{self.smoothing_window}", 0.0)
                return frame, "Detecting...", [], 0.0, fps
            
            if avg_confidence < self.min_confidence:
                self._draw_info(frame, "Uncertain", ["Move into clearer pose"], 
                              avg_confidence, fps, "Low confidence", 0.0)
                return frame, "Uncertain", ["Move into clearer pose"], avg_confidence, fps
            
            # Check stability
            if smoothed_pose == self.current_stable_pose:
                self.pose_hold_count += 1
            else:
                self.current_stable_pose = smoothed_pose
                self.pose_hold_count = 1
                self.persistent_issues.clear()
            
            if self.pose_hold_count < self.min_hold_frames:
                status = f"Stabilizing ({self.pose_hold_count}/{self.min_hold_frames})"
                # Draw basic skeleton while stabilizing
                self._draw_enhanced_skeleton(frame, results.pose_landmarks, 0.5)
                self._draw_info(frame, smoothed_pose, [], avg_confidence, fps, status, 0.0)
                return frame, smoothed_pose, [], avg_confidence, fps
            
            # Pose is stable - check corrections and draw enhanced visual feedback
            corrections, quality_score = self.check_corrections(results.pose_landmarks, smoothed_pose)
            
            # Draw enhanced skeleton with problem highlighting
            self._draw_enhanced_skeleton(frame, results.pose_landmarks, quality_score)
            
            # Draw alignment guides
            if self.show_alignment_guides:
                self._draw_alignment_guides(frame, results.pose_landmarks)
            
            self._draw_info(frame, smoothed_pose, corrections, avg_confidence, 
                          fps, "✓ Locked", quality_score)
            
            return frame, smoothed_pose, corrections, avg_confidence, fps
    
    def _draw_info(self, frame, pose_name, corrections, confidence, fps, status, quality_score):
        """Draw enhanced information overlay on frame."""
        h, w = frame.shape[:2]
        
        # Semi-transparent background
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, min(280, h)), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.35, frame, 0.65, 0, frame)
        
        y = 30
        
        # Pose name with background
        pose_text = f"Pose: {pose_name}"
        color = (0, 255, 0) if "✓" in status else (0, 255, 255)
        cv2.putText(frame, pose_text, (10, y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        y += 35
        
        # Confidence and Quality on same line
        if confidence > 0:
            conf_color = (0, 255, 0) if confidence > 0.85 else (0, 255, 255)
            cv2.putText(frame, f"Confidence: {confidence:.0%}", (10, y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.55, conf_color, 2)
            
            # Quality score with visual bar
            if quality_score > 0:
                quality_color = (
                    (0, 255, 0) if quality_score > 0.8 else
                    (0, 255, 255) if quality_score > 0.6 else
                    (0, 165, 255)
                )
                
                # Draw quality bar
                bar_x = w - 200
                bar_y = y - 15
                bar_w = 150
                bar_h = 15
                
                # Background bar
                cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h), 
                            (50, 50, 50), -1)
                # Fill bar
                fill_w = int(bar_w * quality_score)
                cv2.rectangle(frame, (bar_x, bar_y), (bar_x + fill_w, bar_y + bar_h), 
                            quality_color, -1)
                # Border
                cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h), 
                            (200, 200, 200), 1)
                
                # Quality text
                cv2.putText(frame, f"Form: {quality_score:.0%}", 
                          (bar_x, bar_y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 
                          quality_color, 1)
            y += 30
        
        # Status
        status_color = (0, 255, 0) if "✓" in status else (255, 255, 0)
        cv2.putText(frame, f"Status: {status}", (10, y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, status_color, 1)
        y += 30
        
        # Legend for visual indicators
        if "✓" in status and quality_score < 1.0:
            cv2.putText(frame, "Legend: ", (10, y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)
            cv2.circle(frame, (80, y - 5), 5, (0, 0, 255), -1)
            cv2.putText(frame, "Problem", (90, y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
            cv2.circle(frame, (180, y - 5), 5, (0, 255, 0), -1)
            cv2.putText(frame, "Good", (190, y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
            y += 25
        
        # Corrections with enhanced formatting
        if corrections and "✓" in status:
            cv2.putText(frame, "Corrections:", (10, y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            y += 25
            
            for i, correction in enumerate(corrections[:self.max_corrections]):
                corr_type = correction.get('type', 'info')
                message = correction.get('message', '')
                
                # Icon and color based on severity
                if '✅' in message or corr_type == 'success':
                    text_color = (0, 255, 0)
                    prefix = "✅ "
                elif corr_type == 'critical':
                    text_color = (0, 100, 255)
                    prefix = "⚠️ "
                elif corr_type == 'warning':
                    text_color = (0, 200, 255)
                    prefix = "⚡ "
                else:
                    text_color = (200, 200, 200)
                    prefix = "• "
                
                text = f"{prefix}{message}"
                
                # Add angle info if available
                if 'current' in correction and 'target' in correction:
                    text += f" ({correction['current']:.0f}°→{correction['target']}°)"
                
                # Word wrap for long messages
                max_width = w - 30
                words = text.split()
                line = ""
                for word in words:
                    test_line = line + word + " "
                    text_size = cv2.getTextSize(test_line, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)[0]
                    if text_size[0] < max_width:
                        line = test_line
                    else:
                        cv2.putText(frame, line, (15, y),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.45, text_color, 1)
                        y += 20
                        line = word + " "
                
                if line:
                    cv2.putText(frame, line, (15, y),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.45, text_color, 1)
                y += 22
        
        # FPS and controls (bottom right)
        fps_text = f"FPS: {fps:.1f}"
        cv2.putText(frame, fps_text, (w - 100, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        controls_y = h - 60
        cv2.putText(frame, "Controls: Q=Quit | S=Screenshot | R=Reset | G=Toggle Guides",
                   (10, controls_y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (150, 150, 150), 1)


def main():
    """Main function with enhanced visual feedback."""
    print("\n" + "="*70)
    print("  VISUAL YOGA POSE CORRECTION WITH BODY OUTLINE")
    print("="*70)
    print()
    
    try:
        corrector = VisualPoseCorrector('svm_classifier.pkl')
    except FileNotFoundError:
        print("Error: svm_classifier.pkl not found!")
        return
    
    print("Opening webcam...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    # Set camera properties for better quality
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    print("✓ Webcam opened")
    print()
    print("Visual Features:")
    print("  • Color-coded skeleton (Green=Good, Yellow=OK, Orange=Problem)")
    print("  • Red circles highlight problem joints")
    print("  • Alignment guides show posture reference")
    print("  • Angle indicators display on problem joints")
    print()
    print("Controls:")
    print("  'q' - Quit")
    print("  's' - Save screenshot")
    print("  'r' - Reset correction tracking")
    print("  'g' - Toggle alignment guides")
    print()
    print("Starting...\n")
    
    frame_count = 0
    
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            frame, pose, corrections, conf, fps = corrector.process_frame(frame)
            frame_count += 1
            
            cv2.imshow('Visual Yoga Pose Correction - Enhanced Feedback', frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                print("\nQuitting...")
                break
            elif key == ord('s'):
                filename = f'yoga_visual_{frame_count}.jpg'
                cv2.imwrite(filename, frame)
                print(f"📸 Screenshot saved: {filename}")
            elif key == ord('r'):
                corrector.persistent_issues.clear()
                corrector.problem_joints.clear()
                print("🔄 Correction tracking reset")
            elif key == ord('g'):
                corrector.show_alignment_guides = not corrector.show_alignment_guides
                status = "ON" if corrector.show_alignment_guides else "OFF"
                print(f"📐 Alignment guides: {status}")
    
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        
        print(f"\n{'='*70}")
        print("SESSION COMPLETE")
        print(f"{'='*70}")
        print(f"Total frames: {frame_count}")
        if corrector.fps_history:
            print(f"Average FPS: {np.mean(corrector.fps_history):.1f}")
        if corrector.quality_history:
            print(f"Average Form Quality: {np.mean(corrector.quality_history):.0%}")
        print()


if __name__ == "__main__":
    main()