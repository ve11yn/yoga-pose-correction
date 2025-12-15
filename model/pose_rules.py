"""
Enhanced Pose Correction Rules with Multi-level Validation
"""

POSE_CORRECTION_RULES = {
    'tadasana': {
        'name': 'Mountain Pose (Tadasana)',
        'description': 'Standing pose with body aligned vertically',
        'key_points': [
            'Both legs straight',
            'Spine vertical',
            'Shoulders and hips level',
            'Weight evenly distributed'
        ],
        'checks': [
            {
                'feature': 'left_knee_angle',
                'ideal': 180,
                'tolerance': 10,
                'warning_tolerance': 20,  # Soft warning before critical
                'priority': 'high',
                'message': 'Straighten your left leg completely',
                'warning_message': 'Left leg slightly bent - try to straighten',
                'body_part': 'leg'
            },
            {
                'feature': 'right_knee_angle',
                'ideal': 180,
                'tolerance': 10,
                'warning_tolerance': 20,
                'priority': 'high',
                'message': 'Straighten your right leg completely',
                'warning_message': 'Right leg slightly bent - try to straighten',
                'body_part': 'leg'
            },
            {
                'feature': 'spine_angle',
                'ideal': 170,
                'tolerance': 15,
                'warning_tolerance': 25,
                'priority': 'high',
                'message': 'Stand more upright, lengthen your spine',
                'warning_message': 'Spine alignment could be more vertical',
                'body_part': 'spine'
            },
            {
                'feature': 'shoulder_level_diff',
                'ideal': 0,
                'tolerance': 0.03,
                'warning_tolerance': 0.05,
                'priority': 'medium',
                'message': 'Keep your shoulders level',
                'warning_message': 'Shoulders slightly uneven',
                'body_part': 'shoulders'
            },
            {
                'feature': 'hip_level_diff',
                'ideal': 0,
                'tolerance': 0.03,
                'warning_tolerance': 0.05,
                'priority': 'medium',
                'message': 'Keep your hips level',
                'warning_message': 'Hips slightly uneven',
                'body_part': 'hips'
            },
            {
                'feature': 'weight_distribution',
                'check_type': 'balance',
                'priority': 'low',
                'message': 'Distribute weight evenly on both feet',
                'body_part': 'balance'
            }
        ],
        'common_mistakes': [
            'Locking knees too hard',
            'Leaning forward or back',
            'Tensing shoulders'
        ]
    },
    
    'vriksasana': {
        'name': 'Tree Pose (Vriksasana)',
        'description': 'Balance on one leg with other foot on inner thigh',
        'key_points': [
            'Standing leg straight',
            'Raised knee bent 90°',
            'Spine vertical',
            'Balance centered'
        ],
        'checks': [
            {
                'feature': 'standing_knee_angle',
                'ideal': 180,
                'tolerance': 10,
                'warning_tolerance': 15,
                'priority': 'critical',
                'message': 'Keep your standing leg completely straight',
                'warning_message': 'Standing leg needs to be straighter',
                'body_part': 'leg'
            },
            {
                'feature': 'raised_knee_angle',
                'ideal': 90,
                'tolerance': 20,
                'warning_tolerance': 30,
                'priority': 'high',
                'message': 'Bend your raised knee to about 90 degrees',
                'warning_message': 'Adjust raised knee angle closer to 90°',
                'body_part': 'leg'
            },
            {
                'feature': 'spine_angle',
                'ideal': 170,
                'tolerance': 15,
                'warning_tolerance': 25,
                'priority': 'high',
                'message': 'Keep your spine vertical and upright',
                'warning_message': 'Spine could be more vertical',
                'body_part': 'spine'
            },
            {
                'feature': 'balance_shift',
                'ideal': 0,
                'tolerance': 0.05,
                'warning_tolerance': 0.08,
                'priority': 'medium',
                'message': 'Center your weight over your standing leg',
                'warning_message': 'Weight shifting - find center',
                'body_part': 'balance'
            },
            {
                'feature': 'hip_level_diff',
                'ideal': 0,
                'tolerance': 0.04,
                'warning_tolerance': 0.06,
                'priority': 'medium',
                'message': 'Keep hips level - avoid tilting',
                'warning_message': 'Hips slightly tilted',
                'body_part': 'hips'
            }
        ],
        'common_mistakes': [
            'Bent standing leg',
            'Leaning to side',
            'Placing foot on knee (dangerous!)'
        ]
    },
    
    'virabhadrasana ii': {
        'name': 'Warrior II (Virabhadrasana II)',
        'description': 'Wide-legged stance with front knee bent, arms extended',
        'key_points': [
            'Front knee 90°',
            'Back leg straight',
            'Arms parallel to ground',
            'Torso upright',
            'Wide stance'
        ],
        'checks': [
            {
                'feature': 'front_knee_angle',
                'ideal': 90,
                'tolerance': 15,
                'warning_tolerance': 25,
                'priority': 'critical',
                'message': 'Bend your front knee to 90° (knee over ankle)',
                'warning_message': 'Front knee needs more bend',
                'body_part': 'leg',
                'safety_check': {
                    'min_angle': 70,
                    'max_angle': 110,
                    'warning': 'Knee alignment unsafe - adjust stance'
                }
            },
            {
                'feature': 'back_knee_angle',
                'ideal': 180,
                'tolerance': 10,
                'warning_tolerance': 20,
                'priority': 'high',
                'message': 'Keep your back leg completely straight',
                'warning_message': 'Back leg bending slightly',
                'body_part': 'leg'
            },
            {
                'feature': 'left_elbow_angle',
                'ideal': 180,
                'tolerance': 15,
                'warning_tolerance': 25,
                'priority': 'medium',
                'message': 'Extend your left arm straight',
                'warning_message': 'Left arm could be straighter',
                'body_part': 'arm'
            },
            {
                'feature': 'right_elbow_angle',
                'ideal': 180,
                'tolerance': 15,
                'warning_tolerance': 25,
                'priority': 'medium',
                'message': 'Extend your right arm straight',
                'warning_message': 'Right arm could be straighter',
                'body_part': 'arm'
            },
            {
                'feature': 'spine_angle',
                'ideal': 90,
                'tolerance': 15,
                'warning_tolerance': 25,
                'priority': 'high',
                'message': 'Keep your torso upright (perpendicular to ground)',
                'warning_message': 'Torso leaning - stay more upright',
                'body_part': 'spine'
            },
            {
                'feature': 'foot_distance',
                'ideal': 0.35,
                'min': 0.30,
                'warning_min': 0.25,
                'priority': 'medium',
                'message': 'Widen your stance significantly',
                'warning_message': 'Stance a bit narrow - widen slightly',
                'body_part': 'stance'
            },
            {
                'feature': 'arm_height_parallel',
                'ideal': 0,
                'tolerance': 0.05,
                'warning_tolerance': 0.08,
                'priority': 'low',
                'message': 'Keep arms parallel to ground',
                'warning_message': 'Arms not quite parallel to ground',
                'body_part': 'arm'
            }
        ],
        'common_mistakes': [
            'Knee past toes',
            'Narrow stance',
            'Leaning forward',
            'Collapsed arch'
        ]
    },
    
    'adho mukha svanasana': {
        'name': 'Downward Dog (Adho Mukha Svanasana)',
        'description': 'Inverted V-shape with hands and feet on ground',
        'key_points': [
            'Both legs straight',
            'Hips lifted high',
            'Spine lengthened',
            'Heels reaching toward ground'
        ],
        'checks': [
            {
                'feature': 'left_knee_angle',
                'ideal': 180,
                'tolerance': 15,
                'warning_tolerance': 25,
                'priority': 'high',
                'message': 'Straighten your left leg more',
                'warning_message': 'Left leg could be straighter',
                'body_part': 'leg'
            },
            {
                'feature': 'right_knee_angle',
                'ideal': 180,
                'tolerance': 15,
                'warning_tolerance': 25,
                'priority': 'high',
                'message': 'Straighten your right leg more',
                'warning_message': 'Right leg could be straighter',
                'body_part': 'leg'
            },
            {
                'feature': 'left_hip_angle',
                'ideal': 90,
                'tolerance': 20,
                'warning_tolerance': 30,
                'priority': 'critical',
                'message': 'Lift your hips higher to form inverted V',
                'warning_message': 'Hips need more lift',
                'body_part': 'hips'
            },
            {
                'feature': 'spine_alignment',
                'ideal': 180,
                'tolerance': 20,
                'warning_tolerance': 30,
                'priority': 'high',
                'message': 'Lengthen your spine, push chest toward thighs',
                'warning_message': 'Spine could be longer',
                'body_part': 'spine'
            },
            {
                'feature': 'shoulder_position',
                'check_type': 'alignment',
                'priority': 'medium',
                'message': 'Externally rotate shoulders, broaden upper back',
                'body_part': 'shoulders'
            },
            {
                'feature': 'hand_foot_distance',
                'ideal': 0.5,
                'tolerance': 0.1,
                'priority': 'low',
                'message': 'Adjust hand-foot distance for better V-shape',
                'body_part': 'stance'
            }
        ],
        'common_mistakes': [
            'Hunched shoulders',
            'Bent knees',
            'Hips too low',
            'Weight too forward'
        ]
    },
    
    'bhujangasana': {
        'name': 'Cobra Pose (Bhujangasana)',
        'description': 'Backbend with chest lifted, hips on ground',
        'key_points': [
            'Chest lifted',
            'Arms extended',
            'Legs straight',
            'Shoulders away from ears'
        ],
        'checks': [
            {
                'feature': 'left_elbow_angle',
                'ideal': 150,
                'tolerance': 20,
                'warning_tolerance': 30,
                'priority': 'high',
                'message': 'Lift your chest higher, straighten arms more',
                'warning_message': 'Arms could be straighter for deeper lift',
                'body_part': 'arm'
            },
            {
                'feature': 'right_elbow_angle',
                'ideal': 150,
                'tolerance': 20,
                'warning_tolerance': 30,
                'priority': 'high',
                'message': 'Lift your chest higher, straighten arms more',
                'warning_message': 'Arms could be straighter for deeper lift',
                'body_part': 'arm'
            },
            {
                'feature': 'spine_curve',
                'ideal': 45,
                'tolerance': 15,
                'warning_tolerance': 25,
                'priority': 'critical',
                'message': 'Arch your back more to deepen the backbend',
                'warning_message': 'Backbend could be deeper',
                'body_part': 'spine',
                'safety_check': {
                    'max_angle': 65,
                    'warning': 'Avoid over-arching - protect lower back'
                }
            },
            {
                'feature': 'left_knee_angle',
                'ideal': 180,
                'tolerance': 10,
                'warning_tolerance': 15,
                'priority': 'medium',
                'message': 'Keep legs straight, pressed to floor',
                'warning_message': 'Legs should be flatter on floor',
                'body_part': 'leg'
            },
            {
                'feature': 'right_knee_angle',
                'ideal': 180,
                'tolerance': 10,
                'warning_tolerance': 15,
                'priority': 'medium',
                'message': 'Keep legs straight, pressed to floor',
                'warning_message': 'Legs should be flatter on floor',
                'body_part': 'leg'
            },
            {
                'feature': 'shoulder_ear_distance',
                'min': 0.08,
                'priority': 'medium',
                'message': 'Draw shoulders down away from ears',
                'body_part': 'shoulders'
            }
        ],
        'common_mistakes': [
            'Shoulders hunched',
            'Hips lifting off floor',
            'Arms too bent',
            'Over-arching lower back'
        ]
    },
    
    'phalakasana': {
        'name': 'Plank Pose (Phalakasana)',
        'description': 'Straight body line from head to heels',
        'key_points': [
            'Body forms straight line',
            'Arms straight',
            'Core engaged',
            'Shoulders over wrists'
        ],
        'checks': [
            {
                'feature': 'body_alignment',
                'ideal': 0,
                'tolerance': 0.05,
                'warning_tolerance': 0.08,
                'priority': 'critical',
                'message': 'Form a straight line from head to heels',
                'warning_message': 'Body line not quite straight',
                'body_part': 'body',
                'sub_checks': {
                    'hip_sag': {
                        'max_deviation': -0.05,
                        'message': 'Hips sagging - engage core more'
                    },
                    'hip_pike': {
                        'max_deviation': 0.05,
                        'message': 'Hips too high - lower them slightly'
                    }
                }
            },
            {
                'feature': 'left_elbow_angle',
                'ideal': 180,
                'tolerance': 10,
                'warning_tolerance': 15,
                'priority': 'high',
                'message': 'Keep arms straight, hands under shoulders',
                'warning_message': 'Left arm needs to be straighter',
                'body_part': 'arm'
            },
            {
                'feature': 'right_elbow_angle',
                'ideal': 180,
                'tolerance': 10,
                'warning_tolerance': 15,
                'priority': 'high',
                'message': 'Keep arms straight, hands under shoulders',
                'warning_message': 'Right arm needs to be straighter',
                'body_part': 'arm'
            },
            {
                'feature': 'shoulder_position',
                'check_type': 'vertical_alignment',
                'tolerance': 0.05,
                'priority': 'medium',
                'message': 'Shoulders should be directly over wrists',
                'body_part': 'shoulders'
            },
            {
                'feature': 'neck_alignment',
                'check_type': 'neutral',
                'priority': 'medium',
                'message': 'Keep neck neutral - gaze slightly forward',
                'body_part': 'neck'
            }
        ],
        'common_mistakes': [
            'Hips sagging',
            'Hips too high',
            'Hands too far forward',
            'Shoulders collapsing'
        ]
    },
    
    'utthita trikonasana': {
        'name': 'Extended Triangle (Utthita Trikonasana)',
        'description': 'Triangle shape with both legs straight',
        'key_points': [
            'Both legs straight',
            'Arms in line',
            'Torso parallel to legs',
            'Wide stance'
        ],
        'checks': [
            {
                'feature': 'left_knee_angle',
                'ideal': 180,
                'tolerance': 10,
                'warning_tolerance': 15,
                'priority': 'critical',
                'message': 'Keep both legs completely straight',
                'warning_message': 'Left leg bending slightly',
                'body_part': 'leg'
            },
            {
                'feature': 'right_knee_angle',
                'ideal': 180,
                'tolerance': 10,
                'warning_tolerance': 15,
                'priority': 'critical',
                'message': 'Keep both legs completely straight',
                'warning_message': 'Right leg bending slightly',
                'body_part': 'leg'
            },
            {
                'feature': 'arm_alignment',
                'ideal': 180,
                'tolerance': 15,
                'warning_tolerance': 25,
                'priority': 'high',
                'message': 'Extend arms in one straight line',
                'warning_message': 'Arms not quite in line',
                'body_part': 'arm'
            },
            {
                'feature': 'torso_alignment',
                'check_type': 'planar',
                'priority': 'high',
                'message': 'Keep torso in same plane as legs',
                'warning_message': 'Torso rotating forward or back',
                'body_part': 'torso'
            },
            {
                'feature': 'foot_distance',
                'ideal': 0.35,
                'min': 0.35,
                'warning_min': 0.30,
                'priority': 'medium',
                'message': 'Widen your stance more',
                'warning_message': 'Stance could be wider',
                'body_part': 'stance'
            },
            {
                'feature': 'hip_stack',
                'check_type': 'vertical',
                'priority': 'medium',
                'message': 'Stack hips vertically',
                'body_part': 'hips'
            }
        ],
        'common_mistakes': [
            'Bent front leg',
            'Hips rolling forward',
            'Reaching too far',
            'Collapsed upper shoulder'
        ]
    },
    
    'setu bandha sarvangasana': {
        'name': 'Bridge Pose (Setu Bandha Sarvangasana)',
        'description': 'Hip lift with shoulders on ground',
        'key_points': [
            'Hips lifted high',
            'Knees 90°',
            'Smooth spine arch',
            'Shoulders grounded'
        ],
        'checks': [
            {
                'feature': 'hip_lift',
                'ideal': 0.4,
                'tolerance': 0.1,
                'warning_tolerance': 0.15,
                'priority': 'critical',
                'message': 'Lift your hips higher off the ground',
                'warning_message': 'Hips could be lifted more',
                'body_part': 'hips'
            },
            {
                'feature': 'left_knee_angle',
                'ideal': 90,
                'tolerance': 15,
                'warning_tolerance': 25,
                'priority': 'high',
                'message': 'Keep knees at 90°, aligned over ankles',
                'warning_message': 'Left knee angle needs adjustment',
                'body_part': 'leg'
            },
            {
                'feature': 'right_knee_angle',
                'ideal': 90,
                'tolerance': 15,
                'warning_tolerance': 25,
                'priority': 'high',
                'message': 'Keep knees at 90°, aligned over ankles',
                'warning_message': 'Right knee angle needs adjustment',
                'body_part': 'leg'
            },
            {
                'feature': 'spine_curve',
                'check_type': 'smooth',
                'priority': 'medium',
                'message': 'Create smooth arch in your spine',
                'body_part': 'spine'
            },
            {
                'feature': 'knee_alignment',
                'check_type': 'parallel',
                'tolerance': 0.05,
                'priority': 'medium',
                'message': 'Keep knees hip-width apart and parallel',
                'body_part': 'leg'
            }
        ],
        'common_mistakes': [
            'Knees splaying out',
            'Hips not lifted enough',
            'Feet too far from hips',
            'Neck strain'
        ]
    }
}


# Validation priorities for feedback ordering
PRIORITY_WEIGHTS = {
    'critical': 4,
    'high': 3,
    'medium': 2,
    'low': 1
}

# Body part groupings for coherent feedback
BODY_PARTS = {
    'leg': ['left_knee_angle', 'right_knee_angle', 'standing_knee_angle', 'raised_knee_angle'],
    'arm': ['left_elbow_angle', 'right_elbow_angle', 'arm_alignment'],
    'spine': ['spine_angle', 'spine_alignment', 'spine_curve'],
    'hips': ['hip_level_diff', 'hip_lift', 'hip_stack'],
    'shoulders': ['shoulder_level_diff', 'shoulder_position', 'shoulder_ear_distance'],
    'balance': ['balance_shift', 'weight_distribution'],
    'stance': ['foot_distance', 'hand_foot_distance']
}