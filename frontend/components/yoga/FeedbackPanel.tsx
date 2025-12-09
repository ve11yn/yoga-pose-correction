"use client";

import React, { useEffect, useRef } from "react";
import { CheckCircle2, AlertOctagon, Sparkles, Pause, ArrowRight } from "lucide-react";
import { cn } from "./utils";
import styles from "../../styles/components/yoga/FeedbackPanel.module.css";

interface FeedbackPanelProps {
    corrections: string[];
    isSoundEnabled: boolean;
    isActive: boolean;
}

export const FeedbackPanel: React.FC<FeedbackPanelProps> = ({
    corrections,
    isSoundEnabled,
    isActive
}) => {
    // Only show last 2 messages for minimal visual noise
    const recentCorrections = corrections.slice(-2);

    return (
        <div className={styles.container}>
            <div className={styles.feedbackList}>
                {recentCorrections.length > 0 ? (
                    recentCorrections.map((msg, idx) => {
                        const isGood = msg.includes("✅") || msg.includes("Excellent");
                        // Determine classes based on condition
                        const itemClass = isGood ? styles.feedbackItemGood : styles.feedbackItemBad;
                        const iconClass = isGood ? styles.iconCircleGood : styles.iconCircleBad;

                        return (
                            <div
                                key={idx}
                                className={`${styles.feedbackItem} ${itemClass}`}
                            >
                                <div className={`${styles.iconCircle} ${iconClass}`}>
                                    {isGood ? <CheckCircle2 className="w-3 h-3" /> : <AlertOctagon className="w-3 h-3" />}
                                </div>
                                <span className={styles.messageText}>{msg}</span>
                            </div>
                        );
                    })
                ) : (
                    <div className={styles.waitingMessage}>
                        Listening to your body...
                    </div>
                )}
            </div>
        </div>
    );
};
