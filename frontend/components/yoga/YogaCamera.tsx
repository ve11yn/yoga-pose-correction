"use client";

import React from "react";
import { useYogaSession } from "./hooks/useYogaSession";
import { CameraView } from "./CameraView";
import { PoseStatusCard } from "./PoseStatusCard";
import { FeedbackPanel } from "./FeedbackPanel";
import styles from "../../styles/components/yoga/YogaCamera.module.css";

export default function YogaCam() {
    const {
        webcamRef,
        canvasRef,
        isActive,
        setIsActive,
        currentPose,
        confidence,
        corrections,
        stats,
        isSoundEnabled,
        toggleSound
    } = useYogaSession();

    return (
        <div className={styles.yogaCameraContainer}>
            {/* Ambient Background - Relaxing & Fluid */}
            <div className={styles.yogaBackgroundWrapper}>
                <div className={styles.yogaBlob1} />
                <div className={styles.yogaBlob2} />
            </div>

            {/* Main Camera Layer */}
            <div className={`${styles.cameraLayer} ${isActive ? styles.cameraLayerActive : styles.cameraLayerInactive}`}>
                <CameraView
                    isActive={isActive}
                    webcamRef={webcamRef as React.RefObject<import("react-webcam").default>}
                    canvasRef={canvasRef as React.RefObject<HTMLCanvasElement>}
                    fps={stats.fps}
                    sessionTime={stats.sessionTime}
                    isSoundEnabled={isSoundEnabled}
                    onToggleSound={toggleSound}
                    onStart={() => setIsActive(true)}
                    onStop={() => setIsActive(false)}
                />

                {/* Overlays Wrapper - Inside the relative container so they float ON component */}
                {isActive && (
                    <>
                        {/* Top Center: Pose Status (Dynamic Pill) */}
                        <div className={styles.poseStatusWrapper}>
                            <PoseStatusCard
                                currentPose={currentPose}
                                confidence={confidence}
                            />
                        </div>

                        {/* Bottom Left: AI Feedback (Floating Stream) */}
                        <div className={styles.feedbackWrapper}>
                            <div className={styles.feedbackInner}>
                                <FeedbackPanel
                                    corrections={corrections}
                                    isSoundEnabled={isSoundEnabled}
                                    isActive={isActive}
                                />
                            </div>
                        </div>
                    </>
                )}
            </div>
        </div>
    );
}
