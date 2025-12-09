

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
                'priority': 'high',
                'message': 'Straighten your left leg completely'
            },
            {
                'feature': 'right_knee_angle',
                'ideal': 180,
                'tolerance': 10,
                'priority': 'high',
                'message': 'Straighten your right leg completely'
            },
            {
                'feature': 'spine_angle',
                'ideal': 170,
                'tolerance': 15,
                'priority': 'high',
                'message': 'Stand more upright, lengthen your spine'
            },
            {
                'feature': 'shoulder_level_diff',
                'ideal': 0,
                'tolerance': 0.03,
                'priority': 'medium',
                'message': 'Keep your shoulders level'
            },
            {
                'feature': 'hip_level_diff',
                'ideal': 0,
                'tolerance': 0.03,
                'priority': 'medium',
                'message': 'Keep your hips level'
            }
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
                'priority': 'critical',
                'message': 'Keep your standing leg completely straight'
            },
            {
                'feature': 'raised_knee_angle',
                'ideal': 90,
                'tolerance': 20,
                'priority': 'high',
                'message': 'Bend your raised knee to about 90 degrees'
            },
            {
                'feature': 'spine_angle',
                'ideal': 170,
                'tolerance': 15,
                'priority': 'high',
                'message': 'Keep your spine vertical and upright'
            },
            {
                'feature': 'balance_shift',
                'ideal': 0,
                'tolerance': 0.05,
                'priority': 'medium',
                'message': 'Center your weight over your standing leg'
            }
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
                'priority': 'critical',
                'message': 'Bend your front knee to 90 degrees (knee over ankle)'
            },
            {
                'feature': 'back_knee_angle',
                'ideal': 180,
                'tolerance': 10,
                'priority': 'high',
                'message': 'Keep your back leg completely straight'
            },
            {
                'feature': 'left_elbow_angle',
                'ideal': 180,
                'tolerance': 15,
                'priority': 'medium',
                'message': 'Extend your left arm straight'
            },
            {
                'feature': 'right_elbow_angle',
                'ideal': 180,
                'tolerance': 15,
                'priority': 'medium',
                'message': 'Extend your right arm straight'
            },
            {
                'feature': 'spine_angle',
                'ideal': 90,
                'tolerance': 15,
                'priority': 'high',
                'message': 'Keep your torso upright (perpendicular to ground)'
            },
            {
                'feature': 'foot_distance',
                'ideal': 0.35,
                'min': 0.3,
                'priority': 'medium',
                'message': 'Widen your stance more'
            }
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
                'priority': 'high',
                'message': 'Straighten your left leg more'
            },
            {
                'feature': 'right_knee_angle',
                'ideal': 180,
                'tolerance': 15,
                'priority': 'high',
                'message': 'Straighten your right leg more'
            },
            {
                'feature': 'left_hip_angle',
                'ideal': 90,
                'tolerance': 20,
                'priority': 'critical',
                'message': 'Lift your hips higher to form inverted V'
            },
            {
                'feature': 'spine_alignment',
                'ideal': 180,
                'tolerance': 20,
                'priority': 'high',
                'message': 'Lengthen your spine, push chest toward thighs'
            }
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
                'priority': 'high',
                'message': 'Lift your chest higher, straighten arms more'
            },
            {
                'feature': 'right_elbow_angle',
                'ideal': 150,
                'tolerance': 20,
                'priority': 'high',
                'message': 'Lift your chest higher, straighten arms more'
            },
            {
                'feature': 'spine_curve',
                'ideal': 45,
                'tolerance': 15,
                'priority': 'critical',
                'message': 'Arch your back more to deepen the backbend'
            },
            {
                'feature': 'left_knee_angle',
                'ideal': 180,
                'tolerance': 10,
                'priority': 'medium',
                'message': 'Keep legs straight, pressed to floor'
            },
            {
                'feature': 'right_knee_angle',
                'ideal': 180,
                'tolerance': 10,
                'priority': 'medium',
                'message': 'Keep legs straight, pressed to floor'
            }
        ]
    },
    
    'padmasana': {
        'name': 'Lotus Pose (Padmasana)',
        'description': 'Seated meditation pose with crossed legs',
        'key_points': [
            'Spine straight',
            'Shoulders relaxed',
            'Hips level',
            'Knees toward ground'
        ],
        'checks': [
            {
                'feature': 'spine_angle',
                'ideal': 90,
                'tolerance': 15,
                'priority': 'critical',
                'message': 'Sit up straight, lengthen your spine'
            },
            {
                'feature': 'shoulder_level_diff',
                'ideal': 0,
                'tolerance': 0.03,
                'priority': 'medium',
                'message': 'Level your shoulders, relax them'
            },
            {
                'feature': 'hip_level_diff',
                'ideal': 0,
                'tolerance': 0.03,
                'priority': 'medium',
                'message': 'Keep your hips level on the ground'
            }
        ]
    },
    
    'paschimottanasana': {
        'name': 'Seated Forward Bend (Paschimottanasana)',
        'description': 'Forward fold from seated position',
        'key_points': [
            'Legs straight',
            'Fold from hips',
            'Spine lengthened',
            'Reach toward feet'
        ],
        'checks': [
            {
                'feature': 'left_knee_angle',
                'ideal': 180,
                'tolerance': 10,
                'priority': 'critical',
                'message': 'Keep your left leg straight, press knee down'
            },
            {
                'feature': 'right_knee_angle',
                'ideal': 180,
                'tolerance': 10,
                'priority': 'critical',
                'message': 'Keep your right leg straight, press knee down'
            },
            {
                'feature': 'forward_fold_depth',
                'ideal': 0.2,
                'tolerance': 0.1,
                'priority': 'high',
                'message': 'Fold deeper from your hips, reach toward feet'
            },
            {
                'feature': 'spine_alignment',
                'ideal': 180,
                'tolerance': 30,
                'priority': 'medium',
                'message': 'Lengthen your spine as you fold forward'
            }
        ]
    },
    
    'uttanasana': {
        'name': 'Standing Forward Bend (Uttanasana)',
        'description': 'Forward fold from standing position',
        'key_points': [
            'Legs straight (slight bend okay)',
            'Fold from hips',
            'Head relaxed',
            'Torso toward legs'
        ],
        'checks': [
            {
                'feature': 'left_knee_angle',
                'ideal': 180,
                'tolerance': 10,
                'priority': 'high',
                'message': 'Keep legs straight (slight bend okay)'
            },
            {
                'feature': 'right_knee_angle',
                'ideal': 180,
                'tolerance': 10,
                'priority': 'high',
                'message': 'Keep legs straight (slight bend okay)'
            },
            {
                'feature': 'forward_fold_depth',
                'ideal': 0.3,
                'tolerance': 0.15,
                'priority': 'medium',
                'message': 'Fold deeper, bring torso closer to legs'
            },
            {
                'feature': 'head_position',
                'priority': 'low',
                'message': 'Relax your head and neck completely'
            }
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
                'priority': 'critical',
                'message': 'Form a straight line from head to heels'
            },
            {
                'feature': 'left_elbow_angle',
                'ideal': 180,
                'tolerance': 10,
                'priority': 'high',
                'message': 'Keep arms straight, hands under shoulders'
            },
            {
                'feature': 'right_elbow_angle',
                'ideal': 180,
                'tolerance': 10,
                'priority': 'high',
                'message': 'Keep arms straight, hands under shoulders'
            },
            {
                'feature': 'hip_sag',
                'priority': 'critical',
                'message': 'Engage core, don\'t let hips sag or pike up'
            }
        ]
    },
    
    'dhanurasana': {
        'name': 'Bow Pose (Dhanurasana)',
        'description': 'Deep backbend holding ankles',
        'key_points': [
            'Chest and legs lifted',
            'Holding ankles',
            'Deep arch',
            'Weight on abdomen'
        ],
        'checks': [
            {
                'feature': 'chest_lift',
                'ideal': 0.3,
                'tolerance': 0.1,
                'priority': 'critical',
                'message': 'Lift your chest and legs higher'
            },
            {
                'feature': 'backbend_depth',
                'ideal': 60,
                'tolerance': 20,
                'priority': 'critical',
                'message': 'Deepen your backbend, pull legs up more'
            },
            {
                'feature': 'arm_extension',
                'priority': 'high',
                'message': 'Pull your legs up with your hands'
            }
        ]
    },
    
    'natarajasana': {
        'name': 'Dancer Pose (Natarajasana)',
        'description': 'Standing backbend on one leg',
        'key_points': [
            'Standing leg straight',
            'Back leg lifted high',
            'Torso upright',
            'Balanced'
        ],
        'checks': [
            {
                'feature': 'standing_knee_angle',
                'ideal': 180,
                'tolerance': 10,
                'priority': 'critical',
                'message': 'Keep your standing leg straight'
            },
            {
                'feature': 'raised_leg_height',
                'ideal': 0.4,
                'tolerance': 0.1,
                'priority': 'high',
                'message': 'Lift your back leg higher'
            },
            {
                'feature': 'spine_angle',
                'ideal': 160,
                'tolerance': 20,
                'priority': 'high',
                'message': 'Keep torso upright, chest lifted'
            },
            {
                'feature': 'balance',
                'ideal': 0,
                'tolerance': 0.05,
                'priority': 'medium',
                'message': 'Find balance, focus on fixed point'
            }
        ]
    },
    
    'anjaneyasana': {
        'name': 'Low Lunge (Anjaneyasana)',
        'description': 'Deep lunge with back knee down',
        'key_points': [
            'Front knee 90°',
            'Back leg extended',
            'Torso upright',
            'Hips square'
        ],
        'checks': [
            {
                'feature': 'front_knee_angle',
                'ideal': 90,
                'tolerance': 15,
                'priority': 'critical',
                'message': 'Bend front knee to 90° (knee over ankle)'
            },
            {
                'feature': 'spine_angle',
                'ideal': 90,
                'tolerance': 15,
                'priority': 'high',
                'message': 'Lift your torso upright'
            },
            {
                'feature': 'hip_square',
                'ideal': 0,
                'tolerance': 0.05,
                'priority': 'medium',
                'message': 'Square your hips to face forward'
            },
            {
                'feature': 'back_leg_extension',
                'priority': 'medium',
                'message': 'Extend your back leg fully'
            }
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
                'priority': 'critical',
                'message': 'Keep both legs completely straight'
            },
            {
                'feature': 'right_knee_angle',
                'ideal': 180,
                'tolerance': 10,
                'priority': 'critical',
                'message': 'Keep both legs completely straight'
            },
            {
                'feature': 'arm_alignment',
                'ideal': 180,
                'tolerance': 15,
                'priority': 'high',
                'message': 'Extend arms in one straight line'
            },
            {
                'feature': 'torso_alignment',
                'priority': 'high',
                'message': 'Keep torso in same plane as legs'
            },
            {
                'feature': 'foot_distance',
                'ideal': 0.35,
                'min': 0.35,
                'priority': 'medium',
                'message': 'Widen your stance more'
            }
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
                'priority': 'critical',
                'message': 'Lift your hips higher off the ground'
            },
            {
                'feature': 'left_knee_angle',
                'ideal': 90,
                'tolerance': 15,
                'priority': 'high',
                'message': 'Keep knees at 90°, aligned over ankles'
            },
            {
                'feature': 'right_knee_angle',
                'ideal': 90,
                'tolerance': 15,
                'priority': 'high',
                'message': 'Keep knees at 90°, aligned over ankles'
            },
            {
                'feature': 'spine_curve',
                'priority': 'medium',
                'message': 'Create smooth arch in your spine'
            }
        ]
    },
    
    'salamba sarvangasana': {
        'name': 'Shoulder Stand (Salamba Sarvangasana)',
        'description': 'Inverted pose on shoulders',
        'key_points': [
            'Torso vertical',
            'Legs straight',
            'Supported by hands',
            'Chin tucked'
        ],
        'checks': [
            {
                'feature': 'spine_vertical',
                'ideal': 90,
                'tolerance': 15,
                'priority': 'critical',
                'message': 'Straighten your torso more vertically'
            },
            {
                'feature': 'left_knee_angle',
                'ideal': 180,
                'tolerance': 10,
                'priority': 'high',
                'message': 'Straighten your legs completely'
            },
            {
                'feature': 'right_knee_angle',
                'ideal': 180,
                'tolerance': 10,
                'priority': 'high',
                'message': 'Straighten your legs completely'
            },
            {
                'feature': 'hand_support',
                'priority': 'medium',
                'message': 'Support lower back with hands'
            },
            {
                'feature': 'chin_tuck',
                'priority': 'high',
                'message': 'Keep chin tucked to chest'
            }
        ]
    }
}