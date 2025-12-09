"use client";

import React from "react";
import { Activity } from "lucide-react";
import { cn } from "./utils";
import styles from "../../styles/components/yoga/PoseStatusCard.module.css";

interface PoseStatusCardProps {
    currentPose: string;
    confidence: number;
}

export const PoseStatusCard: React.FC<PoseStatusCardProps> = ({ currentPose, confidence }) => {
    return (
        <div className={styles.card}>
            <div className={styles.column}>
                <span className={styles.label}>Detected Pose</span>
                <span className={styles.value}>{currentPose}</span>
            </div>

            <div className={styles.separator} />

            <div className={styles.columnEnd}>
                <span className={styles.labelWider}>Match</span>
                <div className={styles.matchContainer}>
                    <span className={styles.valueSmall}>{Math.round(confidence * 100)}%</span>
                    <div className={`${styles.matchDot} ${confidence > 0.8 ? styles.matchDotGood : styles.matchDotBad}`} />
                </div>
            </div>
        </div>
    );
};
