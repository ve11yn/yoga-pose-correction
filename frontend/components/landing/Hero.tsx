"use client";

import React from "react";
import Link from "next/link";
import { ArrowRight, Play, Activity, CheckCircle } from "lucide-react";
import { motion } from "framer-motion";
import styles from "../../styles/components/landing/Hero.module.css";

export const Hero = () => {
    return (
        <section className={styles.heroSection}>
            {/* Creative Background Elements: Zen Stones & Aurora */}
            <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 150, repeat: Infinity, ease: "linear" }}
                className={styles.heroBackgroundCircle1}
            />
            <motion.div
                animate={{ rotate: -360 }}
                transition={{ duration: 200, repeat: Infinity, ease: "linear" }}
                className={styles.heroBackgroundCircle2}
            />

            <div className={styles.heroDot1} />
            <div className={styles.heroDot2} />

            <div className={styles.heroContainer}>
                {/* Left Content */}
                <motion.div
                    initial={{ opacity: 0, y: 30, filter: "blur(10px)" }}
                    animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
                    transition={{ duration: 0.8 }}
                    className={styles.heroLeftContent}
                >
                    <motion.div
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.2 }}
                        className={styles.heroBadge}
                    >
                        <span className="w-2 h-2 rounded-full bg-[#3E5E6B] animate-pulse" />
                        <span className="tracking-wide">AI-POWERED YOGA ASSISTANT</span>
                    </motion.div>

                    <h1 className={styles.heroTitle}>
                        Find Your <br />
                        <span className={styles.heroTitleGradient}>Flow</span>
                        State.
                    </h1>

                    <motion.p
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.4 }}
                        className={styles.heroDescription}
                    >
                        Correct your form in real-time with our privacy-first AI. <br />
                        <span className="font-medium text-[#3E5E6B]">No equipment. Just you and your breath.</span>
                    </motion.p>

                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.6 }}
                        className={styles.heroCtaGroup}
                    >
                        <Link href="/practice" className={`${styles.heroBtnPrimary} group`}>
                            <span className="relative z-10 flex items-center gap-2">Start Practice <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" /></span>
                            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000" />
                        </Link>

                        <button className={`${styles.heroBtnSecondary} group`}>
                            <div className="w-8 h-8 rounded-full bg-[#3E5E6B] flex items-center justify-center group-hover:scale-110 transition-transform text-[#FAF3EF]">
                                <Play className="w-3 h-3 fill-current ml-0.5" />
                            </div>
                            <span>Watch Demo</span>
                        </button>
                    </motion.div>
                </motion.div>

                {/* Right Illustration: Artistic Composition */}
                <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 1, delay: 0.2, type: "spring" }}
                    className={styles.heroRightIllustration}
                >
                    {/* Floating Glass Card - Smaller Scale & Tilted */}
                    <motion.div
                        initial={{ rotate: 6 }}
                        animate={{ y: [-15, 15, -15], rotateX: [2, -2, 2], rotateY: [-2, 2, -2], rotate: 6 }}
                        transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
                        className={styles.heroCardGlass}
                    >
                        <div className={styles.heroCardInner}>
                            <img
                                src="/landing_image.webp"
                                alt="Yoga Practice"
                                style={{
                                    width: '100%',
                                    height: '100%',
                                    objectFit: 'cover',
                                    borderRadius: '32px'
                                }}
                            />
                        </div>
                    </motion.div>

                    {/* Floating Feedback Badge - Top Left (Replaces Calories) */}
                    <motion.div
                        animate={{ y: [-10, 10, -10] }}
                        transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
                        className={styles.heroFeedbackBadge}
                    >
                        <div className="w-10 h-10 rounded-full bg-[#94B7D1]/30 flex items-center justify-center text-[#3E5E6B] shrink-0">
                            <CheckCircle className="w-5 h-5" />
                        </div>
                        <div>
                            <div className="text-[10px] font-bold text-[#3E5E6B]/50 uppercase tracking-widest">Feedback</div>
                            <div className="text-sm font-bold text-[#3E5E6B] tracking-tight">Spine Aligned Perfectly</div>
                        </div>
                    </motion.div>

                    {/* Decorative Elements around card */}
                    <div className={styles.heroDecoBlob1} />
                    <div className={styles.heroDecoBlob2} />
                </motion.div>

            </div>
        </section>
    );
};
