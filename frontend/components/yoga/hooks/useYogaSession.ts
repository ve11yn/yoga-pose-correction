import { useState, useRef, useEffect, useCallback } from "react";
import Webcam from "react-webcam";
import axios from "axios";

// Constants
const API_URL = "http://localhost:8000/classify";

export interface YogaStats {
    fps: number;
    sessionTime: number;
}

export function useYogaSession() {
    const webcamRef = useRef<Webcam>(null);
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const poseRef = useRef<any>(null);
    const requestRef = useRef<number>(0);
    const lastTimeRef = useRef<number>(0);
    const isLoopRunning = useRef<boolean>(false);

    // State
    const [isActive, setIsActive] = useState(false);
    const [currentPose, setCurrentPose] = useState<string>("Waiting...");
    const [confidence, setConfidence] = useState<number>(0);
    const [corrections, setCorrections] = useState<string[]>([]);
    const [stats, setStats] = useState<YogaStats>({ fps: 0, sessionTime: 0 });
    const [isSoundEnabled, setIsSoundEnabled] = useState(true);

    // TTS Refs
    const lastSpokenTimeRef = useRef<number>(0);
    const lastSpokenMessageRef = useRef<string>("");

    // Timer Effect
    useEffect(() => {
        let interval: NodeJS.Timeout;
        if (isActive) {
            interval = setInterval(() => {
                setStats(prev => ({ ...prev, sessionTime: prev.sessionTime + 1 }));
            }, 1000);
        }
        return () => clearInterval(interval);
    }, [isActive]);

    // TTS Effect
    useEffect(() => {
        if (!isSoundEnabled) {
            window.speechSynthesis.cancel();
            return;
        }

        if (corrections.length === 0) return;

        const now = Date.now();
        const activeCorrection = corrections.find(c => !c.includes("✅") && !c.includes("Excellent") && !c.includes("posture perfect"));

        if (activeCorrection) {
            if (activeCorrection !== lastSpokenMessageRef.current || (now - lastSpokenTimeRef.current > 5000)) {
                const utterance = new SpeechSynthesisUtterance(activeCorrection);
                utterance.rate = 1.1;
                window.speechSynthesis.cancel();
                window.speechSynthesis.speak(utterance);

                lastSpokenMessageRef.current = activeCorrection;
                lastSpokenTimeRef.current = now;
            }
        }
    }, [corrections, isSoundEnabled]);

    // Canvas Drawing Logic
    const drawLandmarks = (ctx: CanvasRenderingContext2D, landmarks: any[], w: number, h: number) => {
        ctx.strokeStyle = "#00FF00";
        ctx.lineWidth = 2;
        ctx.fillStyle = "#FF0000";

        for (const lm of landmarks) {
            const cx = lm.x * w;
            const cy = lm.y * h;
            ctx.beginPath();
            ctx.arc(cx, cy, 4, 0, 2 * Math.PI);
            ctx.fill();
        }
    };

    // MediaPipe Results Handler
    const onResults = useCallback(async (results: any) => {
        // Calculate FPS
        const now = Date.now();
        if (lastTimeRef.current === 0) {
            lastTimeRef.current = now;
        }
        const delta = now - lastTimeRef.current;
        if (delta > 0) {
            setStats(prev => ({ ...prev, fps: Math.round(1000 / delta) }));
        }
        lastTimeRef.current = now;

        if (canvasRef.current && webcamRef.current?.video) {
            const videoWidth = webcamRef.current.video.videoWidth;
            const videoHeight = webcamRef.current.video.videoHeight;

            canvasRef.current.width = videoWidth;
            canvasRef.current.height = videoHeight;

            const canvasCtx = canvasRef.current.getContext("2d");
            if (canvasCtx) {
                canvasCtx.save();
                canvasCtx.clearRect(0, 0, videoWidth, videoHeight);

                if (results.poseLandmarks) {
                    drawLandmarks(canvasCtx, results.poseLandmarks, videoWidth, videoHeight);

                    try {
                        const response = await axios.post(API_URL, {
                            landmarks: results.poseLandmarks
                        });
                        const data = response.data;
                        setCurrentPose(data.pose_name);
                        setConfidence(data.confidence);
                        setCorrections(data.corrections);
                    } catch (err) {
                        console.error("API Error", err);
                    }
                }
                canvasCtx.restore();
            }
        }
    }, []);

    // Initialize MediaPipe
    useEffect(() => {
        isLoopRunning.current = isActive;

        const loadPose = async () => {
            try {
                const mediapipe = await import("@mediapipe/pose");
                const pose = new mediapipe.Pose({
                    locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`,
                });

                pose.setOptions({
                    modelComplexity: 1,
                    smoothLandmarks: true,
                    enableSegmentation: false,
                    minDetectionConfidence: 0.5,
                    minTrackingConfidence: 0.5,
                });

                pose.onResults(onResults);
                poseRef.current = pose;

                detect();
            } catch (e) {
                console.error("Failed to load Pose", e);
            }
        };

        const detect = async () => {
            if (!isLoopRunning.current) return;

            if (webcamRef.current?.video?.readyState === 4 && poseRef.current) {
                try {
                    await poseRef.current.send({ image: webcamRef.current.video });
                } catch (error) {
                    console.warn("Pose send error:", error);
                }
            }

            if (isLoopRunning.current) {
                requestRef.current = requestAnimationFrame(detect);
            }
        };

        if (isActive) {
            if (!poseRef.current) loadPose();
            else detect();
        } else {
            if (requestRef.current) cancelAnimationFrame(requestRef.current);
            if (poseRef.current) {
                poseRef.current.close().then(() => poseRef.current = null);
            }
        }

        return () => {
            isLoopRunning.current = false;
            if (requestRef.current) cancelAnimationFrame(requestRef.current);
            if (poseRef.current) {
                poseRef.current.close();
                poseRef.current = null;
            }
        };
    }, [isActive, onResults]);

    return {
        webcamRef,
        canvasRef,
        isActive,
        setIsActive,
        currentPose,
        confidence,
        corrections,
        stats,
        isSoundEnabled,
        toggleSound: () => setIsSoundEnabled(prev => !prev)
    };
}
