import React, { RefObject } from "react";
import Webcam from "react-webcam";
import { Camera, Volume2, VolumeX, ArrowRight, Pause } from "lucide-react";
import { formatTime, cn } from "./utils";
import styles from "../../styles/components/yoga/CameraView.module.css";

interface CameraViewProps {
    isActive: boolean;
    webcamRef: RefObject<Webcam>;
    canvasRef: RefObject<HTMLCanvasElement>;
    fps: number;
    sessionTime: number;
    isSoundEnabled: boolean;
    onToggleSound: () => void;
    onStart: () => void;
    onStop: () => void;
}

export const CameraView: React.FC<CameraViewProps> = ({
    isActive,
    webcamRef,
    canvasRef,
    fps,
    sessionTime,
    isSoundEnabled,
    onToggleSound,
    onStart,
    onStop
}) => {
    return (
        <div className={`${styles.cameraContainer} ${isActive ? styles.cameraContainerActive : styles.cameraContainerInactive}`}>
            {isActive ? (
                <>
                    {/* Camera Feed */}
                    <div className={styles.cameraFeedWrapper}>
                        <Webcam
                            ref={webcamRef}
                            className={styles.webcam}
                            mirrored
                            videoConstraints={{
                                facingMode: "user",
                                aspectRatio: 16 / 9
                            }}
                        />
                        <canvas
                            ref={canvasRef}
                            className={styles.canvas}
                        />
                    </div>

                    {/* Gradient Overlay for Text Readability */}
                    <div className={styles.gradientOverlay} />

                    {/* HUD Controls - Minimal Bottom Bar */}
                    <div className={styles.hudControls}>
                        {/* Timer Pill */}
                        <div className={styles.leftControls}>
                            <div className={styles.timerPill}>
                                <div className={styles.timerDot} />
                                <span className={styles.timerText}>{formatTime(sessionTime)}</span>
                            </div>
                            <button
                                onClick={onStop}
                                className={styles.endSessionBtn}
                            >
                                <Pause className="w-3 h-3" />
                                End Session
                            </button>
                        </div>

                        {/* Right Controls */}
                        <div className={styles.rightControls}>
                            <div className={styles.fpsBadge}>
                                {fps} FPS
                            </div>
                            <button
                                onClick={onToggleSound}
                                className={styles.soundBtn}
                            >
                                {isSoundEnabled ? <Volume2 className="w-5 h-5" /> : <VolumeX className="w-5 h-5" />}
                            </button>
                        </div>
                    </div>
                </>
            ) : (
                <div className={styles.inactiveContainer}>
                    {/* Creative Noise Texture */}
                    <div className={styles.noiseTexture} />

                    {/* Background Pulse Effect - Aurora Style */}
                    <div className={styles.backgroundPulseWrapper}>
                        <div className={styles.pulseBlob1} />
                        <div className={styles.pulseBlob2} />
                    </div>

                    <div className={styles.contentWrapper}>
                        {/* Icon Circle - Floating Zen Stone */}
                        <div className={styles.iconCircle}>
                            <Camera className="w-10 h-10 text-[#3E5E6B]" />
                        </div>

                        {/* Typography - Creative */}
                        <h3 className={styles.title}>
                            Find Your <br />
                            <span className={styles.titleGradient}>Center</span>
                        </h3>

                        <p className={styles.description}>
                            Position your device. Take a deep breath. <br />
                            <span className="font-medium text-[#3E5E6B]">Let the AI guide you.</span>
                        </p>

                        {/* CTA Button - Creative Glass */}
                        <button
                            onClick={onStart}
                            className={`${styles.ctaButton} group`}
                        >
                            <span className={styles.ctaContent}>
                                Begin Practice <ArrowRight className="w-5 h-5 text-[#FAF3EF]" />
                            </span>

                            {/* Inner Glow */}
                            <div className={styles.ctaGlow} />
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};
