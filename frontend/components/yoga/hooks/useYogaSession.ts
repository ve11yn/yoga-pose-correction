import { useState, useRef, useEffect, useCallback } from "react";
import Webcam from "react-webcam";
import axios from "axios";

// Constants
const API_URL = process.env.NEXT_PUBLIC_API_URL
  ? `${process.env.NEXT_PUBLIC_API_URL}/classify`
  : "http://localhost:8000/classify";

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
  const lastFpsUpdateTimeRef = useRef<number>(0);
  const isLoopRunning = useRef<boolean>(false);
  const lastApiCallTimeRef = useRef<number>(0);
  const isApiProcessingRef = useRef<boolean>(false);

  // State
  const [isActive, setIsActive] = useState(false);
  const [currentPose, setCurrentPose] = useState<string>("Waiting...");
  const [confidence, setConfidence] = useState<number>(0);
  const [corrections, setCorrections] = useState<string[]>([]);
  const [stats, setStats] = useState<YogaStats>({ fps: 0, sessionTime: 0 });
  const [isSoundEnabled, setIsSoundEnabled] = useState(true);
  const [apiError, setApiError] = useState<string | null>(null);

  // TTS Refs
  const lastSpokenTimeRef = useRef<number>(0);
  const lastSpokenMessageRef = useRef<string>("");

  // Recording Refs
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const recordedChunksRef = useRef<Blob[]>([]);

  // Recording State
  const [isRecording, setIsRecording] = useState(false);

  // Initial Health Check
  useEffect(() => {
    // Check if backend is reachable once on mount
    axios.get(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/`)
      .then(res => {
        if (res.data.status === "ok") {
          console.log("Backend Connected", res.data);
          setApiError(null);
        }
      })
      .catch(err => {
        const msg = "Cannot connect to AI Server. Is it running?";
        console.error(msg, err);
        setApiError(msg);
      });
  }, []);

  // Timer Effect
  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isActive) {
      interval = setInterval(() => {
        setStats((prev) => ({ ...prev, sessionTime: prev.sessionTime + 1 }));
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

    // Get the most recent correction (last one in array)
    // This ensures we only speak what's currently most relevant
    const latestCorrection = corrections[corrections.length - 1];

    // Check if it's a positive message
    const isPositive =
      latestCorrection.includes("✅") ||
      latestCorrection.includes("Excellent") ||
      latestCorrection.includes("posture perfect");

    // Speak if:
    // 1. It's a new message (different from last spoken)
    // 2. OR enough time has passed (5s for corrections, 10s for positive feedback)
    const timeSinceLastSpoken = now - lastSpokenTimeRef.current;
    const cooldownTime = isPositive ? 10000 : 5000; // 10s for positive, 5s for corrections

    const isNewMessage = latestCorrection !== lastSpokenMessageRef.current;
    const isCooldownExpired = timeSinceLastSpoken > cooldownTime;

    if (isNewMessage || isCooldownExpired) {
      // If it's a NEW message, cancel ongoing speech immediately
      // This ensures audio switches to new feedback right away
      if (isNewMessage) {
        window.speechSynthesis.cancel();
      }

      const utterance = new SpeechSynthesisUtterance(latestCorrection);
      utterance.rate = 1.1;
      window.speechSynthesis.speak(utterance);

      lastSpokenMessageRef.current = latestCorrection;
      lastSpokenTimeRef.current = now;
    }
  }, [corrections, isSoundEnabled]);

  // Canvas Drawing Logic - Draw skeleton with connections (mirrored)
  const drawLandmarks = (ctx: CanvasRenderingContext2D, landmarks: any[], w: number, h: number) => {
    // Define MediaPipe Pose connections (skeleton structure)
    const POSE_CONNECTIONS = [
      [0, 1], [1, 2], [2, 3], [3, 7], [0, 4], [4, 5], [5, 6], [6, 8],
      [9, 10], [11, 12], [11, 13], [13, 15], [15, 17], [15, 19], [15, 21],
      [17, 19], [12, 14], [14, 16], [16, 18], [16, 20], [16, 22], [18, 20],
      [11, 23], [12, 24], [23, 24], [23, 25], [24, 26], [25, 27], [26, 28],
      [27, 29], [28, 30], [29, 31], [30, 32], [27, 31], [28, 32]
    ];

    // Mirror the canvas horizontally
    ctx.translate(w, 0);
    ctx.scale(-1, 1);

    // Draw connections (lines) - Blue color
    ctx.strokeStyle = "#0099FF"; // Blue lines
    ctx.lineWidth = 3;

    for (const [startIdx, endIdx] of POSE_CONNECTIONS) {
      if (landmarks[startIdx] && landmarks[endIdx]) {
        const start = landmarks[startIdx];
        const end = landmarks[endIdx];

        ctx.beginPath();
        ctx.moveTo(start.x * w, start.y * h);
        ctx.lineTo(end.x * w, end.y * h);
        ctx.stroke();
      }
    }

    // Draw keypoints (small dots) - Blue color
    ctx.fillStyle = "#0099FF"; // Blue dots
    for (const lm of landmarks) {
      const cx = lm.x * w;
      const cy = lm.y * h;
      ctx.beginPath();
      ctx.arc(cx, cy, 3, 0, 2 * Math.PI);
      ctx.fill();
    }
  };


  // MediaPipe Results Handler
  const onResults = useCallback(
    async (results: any) => {
      // Calculate FPS
      const now = Date.now();
      // Initialize if needed
      if (lastTimeRef.current === 0) lastTimeRef.current = now;
      if (lastFpsUpdateTimeRef.current === 0) lastFpsUpdateTimeRef.current = now;

      const delta = now - lastTimeRef.current;
      lastTimeRef.current = now;

      // Only update React state for FPS every 500ms to verify/avoid excessive re-renders
      if (now - lastFpsUpdateTimeRef.current >= 500) {
        if (delta > 0) {
          const currentFps = Math.round(1000 / delta);
          setStats((prev) => ({ ...prev, fps: currentFps }));
        }
        lastFpsUpdateTimeRef.current = now;
      }

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
            drawLandmarks(
              canvasCtx,
              results.poseLandmarks,
              videoWidth,
              videoHeight
            );

            // Throttle API calls to prevent lag
            // Only send if:
            // 1. Enough time has passed (200ms = 5 FPS cap for classification)
            // 2. No other request is currently processing
            const now = Date.now();
            if (now - lastApiCallTimeRef.current >= 200 && !isApiProcessingRef.current) {
              isApiProcessingRef.current = true;
              lastApiCallTimeRef.current = now;

              // Explicitly map landmarks to ensure clean JSON object with no missing fields
              const formattedLandmarks = results.poseLandmarks.map((lm: any) => ({
                x: lm.x,
                y: lm.y,
                z: lm.z,
                visibility: lm.visibility ?? 0.0,
              }));

              // Don't await this! Let it run in background so we don't block rendering
              axios.post(API_URL, {
                landmarks: formattedLandmarks,
              }, { timeout: 5000 }) // 5s timeout
                .then((response) => {
                  const data = response.data;
                  setCurrentPose(data.pose_name);
                  setConfidence(data.confidence);
                  setCorrections(data.corrections);
                  setApiError(null);
                })
                .catch((err) => {
                  console.error("API Error Details:", err.response?.data || err.message);
                  if (err.code === "ERR_NETWORK") {
                    setApiError("Backend disconnected");
                  } else {
                    setApiError(`API Error: ${err.response?.data?.detail || err.message}`);
                  }
                })
                .finally(() => {
                  isApiProcessingRef.current = false;
                });
            }
          } else {
            // No pose detected - reset to default state
            // Only reset if we truly lost the pose for a bit to avoid flickering
            if (!isApiProcessingRef.current) {
              setCurrentPose("Waiting...");
              setConfidence(0);
              setCorrections([]);
            }
          }
          canvasCtx.restore();
        }
      }
    },
    [isActive, isRecording]
  );

  // Reset state when session stops
  useEffect(() => {
    if (!isActive) {
      // Aggressively stop all audio - use multiple methods for reliability
      // Method 1: Pause first
      window.speechSynthesis.pause();

      // Method 2: Cancel
      window.speechSynthesis.cancel();

      // Method 3: Resume then cancel again (clears queue in some browsers)
      window.speechSynthesis.resume();
      window.speechSynthesis.cancel();

      // Method 4: Force with setTimeout
      setTimeout(() => {
        window.speechSynthesis.cancel();
      }, 0);

      setTimeout(() => {
        window.speechSynthesis.cancel();
      }, 100);

      // Reset state
      setCurrentPose("Waiting...");
      setConfidence(0);
      setCorrections([]);
      setStats({ fps: 0, sessionTime: 0 });

      // Reset TTS refs
      lastSpokenTimeRef.current = 0;
      lastSpokenMessageRef.current = "";

      // Stop recording if active
      if (isRecording && mediaRecorderRef.current) {
        mediaRecorderRef.current.stop();
        setIsRecording(false);
      }
    }
  }, [isActive, isRecording]);

  // Initialize MediaPipe
  useEffect(() => {
    isLoopRunning.current = isActive;

    const loadPose = async () => {
      try {
        const mediapipe = await import("@mediapipe/pose");
        const pose = new mediapipe.Pose({
          locateFile: (file) =>
            `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`,
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
        poseRef.current.close().then(() => (poseRef.current = null));
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

  // Recording Functions
  const startRecording = useCallback(() => {
    if (!webcamRef.current?.stream) {
      console.error("No webcam stream available");
      return;
    }

    try {
      recordedChunksRef.current = [];
      const stream = webcamRef.current.stream;

      const options = { mimeType: "video/webm;codecs=vp9" };
      const mediaRecorder = new MediaRecorder(stream, options);

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          recordedChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(recordedChunksRef.current, {
          type: "video/webm",
        });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `yoga-session-${new Date()
          .toISOString()
          .slice(0, 19)
          .replace(/:/g, "-")}.webm`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      };

      mediaRecorderRef.current = mediaRecorder;
      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error("Error starting recording:", error);
    }
  }, []);

  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  }, [isRecording]);

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
    toggleSound: () => setIsSoundEnabled((prev) => !prev),
    isRecording,
    startRecording,
    stopRecording,
    apiError
  };
}
