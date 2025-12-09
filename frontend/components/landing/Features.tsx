"use client";

import React from "react";
import { Activity, Shield, Zap } from "lucide-react";
import { motion } from "framer-motion";
import styles from "../../styles/components/landing/Features.module.css";

export const Features = () => {
    return (
        <section id="features" className={styles.section}>
            <div className={styles.container}>
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.6 }}
                    className={styles.header}
                >
                    <h2 className={styles.subtitle}>Why Zenva?</h2>
                    <h3 className={styles.title}>Your Personal Home Studio</h3>
                </motion.div>

                <motion.div
                    initial="hidden"
                    whileInView="visible"
                    viewport={{ once: true }}
                    variants={{
                        hidden: { opacity: 0 },
                        visible: {
                            opacity: 1,
                            transition: {
                                staggerChildren: 0.2
                            }
                        }
                    }}
                    className={styles.grid}
                >
                    {[
                        {
                            icon: <Activity className="w-6 h-6" />,
                            title: "Real-time Correction",
                            desc: "Our computer vision engine tracks 33 keypoints on your body to ensure perfect form instantly.",
                            iconClass: styles.iconBox1
                        },
                        {
                            icon: <Shield className="w-6 h-6" />,
                            title: "Privacy First",
                            desc: "All processing happens locally in your browser. Your video feed never touches our servers.",
                            iconClass: styles.iconBox2
                        },
                        {
                            icon: <Zap className="w-6 h-6" />,
                            title: "Instant Feedback",
                            desc: "Get audio and visual cues immediately when your posture needs adjustment.",
                            iconClass: styles.iconBox3
                        }
                    ].map((feature, i) => (
                        <motion.div
                            key={i}
                            variants={{
                                hidden: { opacity: 0, y: 20 },
                                visible: { opacity: 1, y: 0 }
                            }}
                            whileHover={{ y: -5 }}
                            className={styles.card}
                        >
                            <div className={`${styles.iconBox} ${feature.iconClass}`}>
                                {feature.icon}
                            </div>
                            <h4 className={styles.cardTitle}>{feature.title}</h4>
                            <p className={styles.cardDesc}>
                                {feature.desc}
                            </p>
                        </motion.div>
                    ))}
                </motion.div>
            </div>
        </section>
    );
};
