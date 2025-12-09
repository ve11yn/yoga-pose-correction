"use client";

import React from "react";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { Target, Smartphone } from "lucide-react";
import { motion } from "framer-motion";
import styles from "../../styles/components/pages/FeaturesPage.module.css";

export default function FeaturesPage() {
    return (
        <div className={styles.pageContainer}>
            <Navbar />

            <main className={styles.main}>
                <div className={styles.wrapper}>
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6 }}
                        className={styles.heroSection}
                    >
                        <h1 className={styles.heroTitle}>Powerful Features for <br /> <span className={styles.heroSubtitle}>Better Practice</span></h1>
                        <p className={styles.heroDesc}>
                            Discover how our AI technology transforms your home yoga sessions into professional-grade classes.
                        </p>
                    </motion.div>

                    <div className={styles.grid}>
                        <motion.div
                            initial={{ opacity: 0, x: -50 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.6, delay: 0.2 }}
                            className={styles.card}
                        >
                            <div className={`${styles.iconBox} ${styles.iconBox1}`}>
                                <Target className="w-8 h-8" />
                            </div>
                            <h3 className={styles.cardTitle}>Precision Tracking</h3>
                            <p className={styles.cardDesc}>
                                Utilizes advanced MediaPipe technology to track 33 key body landmarks in real-time. Our system understands the geometry of your body to provide accurate pose recognition.
                            </p>
                            <ul className={styles.featuresList}>
                                {["33 Keypoints Analysis", "Sub-millimeter accuracy", "30+ FPS Performance"].map((item, i) => (
                                    <li key={i} className={styles.featureItem}>
                                        <div className={`${styles.dot} ${styles.dot1}`} /> {item}
                                    </li>
                                ))}
                            </ul>
                        </motion.div>
                        <motion.div
                            initial={{ opacity: 0, x: 50 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.6, delay: 0.4 }}
                            className={styles.card}
                        >
                            <div className={`${styles.iconBox} ${styles.iconBox2}`}>
                                <Smartphone className="w-8 h-8" />
                            </div>
                            <h3 className={styles.cardTitle}>Voice Assistant</h3>
                            <p className={styles.cardDesc}>
                                Don't look at the screen. Our integrated Text-to-Speech engine provides gentle audio cues so you can maintain your flow and focus on your breath.
                            </p>
                            <ul className={styles.featuresList}>
                                {["Hands-free guidance", "Intelligent repetition prevention", "Natural voice feedback"].map((item, i) => (
                                    <li key={i} className={styles.featureItem}>
                                        <div className={`${styles.dot} ${styles.dot2}`} /> {item}
                                    </li>
                                ))}
                            </ul>
                        </motion.div>
                    </div>
                </div>
            </main>

            <Footer />
        </div>
    );
}
