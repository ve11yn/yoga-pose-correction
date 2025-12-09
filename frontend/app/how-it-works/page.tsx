"use client";

import React from "react";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { Camera, Zap, CheckCircle } from "lucide-react";
import { motion } from "framer-motion";
import styles from "../../styles/components/pages/HowItWorksPage.module.css";

export default function HowItWorksPage() {
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
                        <h1 className={styles.heroTitle}>How It <span className={styles.heroHighlight}>Works</span></h1>
                        <p className={styles.heroDesc}>
                            Getting started is easy. No specialized equipment needed—just your device and a little space.
                        </p>
                    </motion.div>

                    <div className={styles.stepsContainer}>
                        {/* Connecting Line (Desktop) */}
                        <motion.div
                            initial={{ scaleX: 0 }}
                            animate={{ scaleX: 1 }}
                            transition={{ duration: 1, delay: 0.5 }}
                            className={styles.connectingLine}
                        />

                        <div className={styles.stepsGrid}>
                            {[
                                {
                                    step: "01",
                                    title: "Set Up Camera",
                                    desc: "Allow camera access and position yourself about 2-3 meters away, ensuring your full body is visible.",
                                    icon: <Camera className="w-8 h-8 text-[#FAF3EF]" />,
                                    iconClass: styles.stepIcon1
                                },
                                {
                                    step: "02",
                                    title: "Select Pose",
                                    desc: "Start moving. The AI automatically detects which yoga pose you are attempting to perform.",
                                    icon: <Zap className="w-8 h-8 text-[#3E5E6B]" />,
                                    iconClass: styles.stepIcon2
                                },
                                {
                                    step: "03",
                                    title: "Get Corrections",
                                    desc: "Receive instant audio and visual feedback if your alignment is off, helping you correct immediately.",
                                    icon: <CheckCircle className="w-8 h-8 text-[#3E5E6B]" />,
                                    iconClass: styles.stepIcon3
                                }
                            ].map((item, i) => (
                                <motion.div
                                    key={i}
                                    initial={{ opacity: 0, y: 30 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ duration: 0.5, delay: 0.2 * (i + 1) }}
                                    className={styles.stepWrapper}
                                >
                                    <div className={`${styles.stepIconWrapper} ${item.iconClass}`}>
                                        {item.icon}
                                        <div className={styles.stepNumber}>
                                            {item.step}
                                        </div>
                                    </div>
                                    <div className={styles.stepContent}>
                                        <h3 className={styles.stepTitle}>{item.title}</h3>
                                        <p className={styles.stepDesc}>
                                            {item.desc}
                                        </p>
                                    </div>
                                </motion.div>
                            ))}
                        </div>
                    </div>
                </div>
            </main>

            <Footer />
        </div>
    );
}
