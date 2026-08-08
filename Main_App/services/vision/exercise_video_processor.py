import os
import cv2
import av
import numpy as np
import mediapipe as mp
import threading

from streamlit_webrtc import VideoProcessorBase
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from detectors.squat import SquatDetector
from detectors.pushup import PushUpDetector
from detectors.biceps_curl import BicepsCurlDetector
from detectors.shoulder_press import ShoulderPressDetector
from detectors.lunges import LungesDetector

from services.config.workout_config import POSE_CONNECTIONS


class VideoProcessorClass(VideoProcessorBase):

    def __init__(self):
        self._lock = threading.Lock()
        self._latest_metrics = None
        self._exercise_type = "Squats"
        self._frame_timestamps_ms = 0

        # =========================================================
        # FIND PROJECT ROOT
        # =========================================================

        current_file = os.path.abspath(__file__)

        # exercise_video_processor.py
        #        ↓
        # vision
        #        ↓
        # services
        #        ↓
        # Main_App
        #        ↓
        # ai-gym-coach (PROJECT ROOT)

        project_root = os.path.abspath(
            os.path.join(
                os.path.dirname(current_file),
                "..",
                "..",
                ".."
            )
        )

        # =========================================================
        # FIND MEDIAPIPE MODEL
        # =========================================================

        possible_model_paths = [
            # Main project root
            os.path.join(
                project_root,
                "ml_models",
                "pose_landmarker_full.task"
            ),

            # If ml_models is inside Main_App
            os.path.join(
                project_root,
                "Main_App",
                "ml_models",
                "pose_landmarker_full.task"
            ),

            # Current working directory
            os.path.join(
                os.getcwd(),
                "ml_models",
                "pose_landmarker_full.task"
            ),

            # Current working directory/Main_App
            os.path.join(
                os.getcwd(),
                "Main_App",
                "ml_models",
                "pose_landmarker_full.task"
            ),
        ]

        model_path = None

        for path in possible_model_paths:
            if os.path.isfile(path):
                model_path = path
                break

        # =========================================================
        # MODEL NOT FOUND ERROR
        # =========================================================

        if model_path is None:
            raise FileNotFoundError(
                "MediaPipe pose model not found.\n\n"
                "Expected file:\n"
                "ml_models/pose_landmarker_full.task\n\n"
                "Searched locations:\n"
                + "\n".join(possible_model_paths)
            )

        # =========================================================
        # MEDIAPIPE POSE LANDMARKER
        # =========================================================

        base_options = python.BaseOptions(
            model_asset_path=model_path
        )

        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            min_pose_detection_confidence=0.7,
            min_pose_presence_confidence=0.7,
            min_tracking_confidence=0.7,
            output_segmentation_masks=False
        )

        self._landmarker = vision.PoseLandmarker.create_from_options(
            options
        )

        # =========================================================
        # EXERCISE DETECTORS
        # =========================================================

        self._detectors = {
            "Squats": SquatDetector(),
            "Push-ups": PushUpDetector(),
            "Biceps Curls (Dumbbell)": BicepsCurlDetector(),
            "Shoulder Press": ShoulderPressDetector(),
            "Lunges": LungesDetector(),
        }

    # =============================================================
    # METRICS
    # =============================================================

    def set_latest_metrics(self, metrics):
        with self._lock:
            self._latest_metrics = metrics.copy()

    def get_latest_metrics(self):
        with self._lock:
            if self._latest_metrics is None:
                return None

            return self._latest_metrics.copy()

    # =============================================================
    # EXERCISE
    # =============================================================

    def set_exercise(self, exercise_type):
        with self._lock:
            self._exercise_type = exercise_type

    def get_exercise(self):
        with self._lock:
            return self._exercise_type

    # =============================================================
    # DRAW SKELETON
    # =============================================================

    def _draw_skeleton(self, img, landmarks):

        h, w = img.shape[:2]

        # Draw connections
        for start_idx, end_idx in POSE_CONNECTIONS:

            p1 = landmarks[start_idx]
            p2 = landmarks[end_idx]

            if (
                p1.visibility > 0.7
                and p2.visibility > 0.7
            ):

                cv2.line(
                    img,
                    (
                        int(p1.x * w),
                        int(p1.y * h)
                    ),
                    (
                        int(p2.x * w),
                        int(p2.y * h)
                    ),
                    (0, 255, 0),
                    4
                )

        # Draw landmarks
        for lm in landmarks:

            if lm.visibility > 0.7:

                cv2.circle(
                    img,
                    (
                        int(lm.x * w),
                        int(lm.y * h)
                    ),
                    6,
                    (255, 0, 0),
                    -1
                )

    # =============================================================
    # NO POSE WARNING
    # =============================================================

    def _draw_no_pose_warnings(self, img):

        cv2.putText(
            img,
            "NO POSE DETECTED",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
            cv2.LINE_AA
        )

        cv2.putText(
            img,
            "PLEASE FACE THE CAMERA",
            (30, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
            cv2.LINE_AA
        )

    # =============================================================
    # EXERCISE OVERLAYS
    # =============================================================

    def _draw_overlays(self, img, metrics, ex_type):

        if ex_type == "Squats":
            self._draw_squats_overlays(img, metrics)

        elif ex_type == "Push-ups":
            self._draw_pushup_overlays(img, metrics)

        elif ex_type == "Biceps Curls (Dumbbell)":
            self._draw_curl_overlays(img, metrics)

        elif ex_type == "Shoulder Press":
            self._draw_press_overlays(img, metrics)

        elif ex_type == "Lunges":
            self._draw_lunge_overlays(img, metrics)

    # =============================================================
    # SQUAT OVERLAY
    # =============================================================

    def _draw_squats_overlays(self, img, metrics):

        h, _ = img.shape[:2]

        cv2.putText(
            img,
            f"DEPTH: {metrics.get('depth_status', 'N/A')}",
            (20, h - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    # =============================================================
    # PUSHUP OVERLAY
    # =============================================================

    def _draw_pushup_overlays(self, img, metrics):

        h, _ = img.shape[:2]

        cv2.putText(
            img,
            (
                f"BODY: {metrics.get('body_alignment', 'N/A')} "
                f"| HIP: {metrics.get('hip_status', 'N/A')}"
            ),
            (20, h - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    # =============================================================
    # BICEPS CURL OVERLAY
    # =============================================================

    def _draw_curl_overlays(self, img, metrics):

        h, _ = img.shape[:2]

        cv2.putText(
            img,
            f"SWING: {metrics.get('swing_status', 'N/A')}",
            (20, h - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    # =============================================================
    # SHOULDER PRESS OVERLAY
    # =============================================================

    def _draw_press_overlays(self, img, metrics):

        h, _ = img.shape[:2]

        cv2.putText(
            img,
            (
                f"EXT: {metrics.get('extension_status', 'N/A')} "
                f"| BACK: {metrics.get('back_arch_status', 'N/A')}"
            ),
            (20, h - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    # =============================================================
    # LUNGE OVERLAY
    # =============================================================

    def _draw_lunge_overlays(self, img, metrics):

        h, _ = img.shape[:2]

        cv2.putText(
            img,
            f"BALANCE: {metrics.get('balance_status', 'N/A')}",
            (20, h - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    # =============================================================
    # RECEIVE CAMERA FRAME
    # =============================================================

    def recv(self, frame):

        # Convert WebRTC frame to OpenCV BGR
        image = frame.to_ndarray(format="bgr24")

        # Mirror camera
        image = cv2.flip(image, 1)

        image = np.asarray(
            image,
            dtype=np.uint8
        )

        # =========================================================
        # CONVERT BGR -> RGB FOR MEDIAPIPE
        # =========================================================

        rgb_image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_image
        )

        # =========================================================
        # TIMESTAMP
        # =========================================================

        self._frame_timestamps_ms += 33

        # =========================================================
        # MEDIAPIPE POSE DETECTION
        # =========================================================

        result = self._landmarker.detect_for_video(
            mp_image,
            self._frame_timestamps_ms
        )

        # =========================================================
        # POSE FOUND
        # =========================================================

        if result.pose_landmarks:

            landmarks = result.pose_landmarks[0]

            # Draw skeleton
            self._draw_skeleton(
                image,
                landmarks
            )

            # Current exercise
            ex_type = self.get_exercise()

            # Get detector
            detector = self._detectors.get(
                ex_type
            )

            if detector:

                # Process exercise
                metrics = detector.process(
                    landmarks
                )

                metrics["pose_detected"] = True

                # Draw exercise information
                self._draw_overlays(
                    image,
                    metrics,
                    ex_type
                )

                # Save metrics
                self.set_latest_metrics(
                    metrics
                )

        # =========================================================
        # NO POSE
        # =========================================================

        else:

            self._draw_no_pose_warnings(
                image
            )

            with self._lock:

                if self._latest_metrics is not None:

                    self._latest_metrics[
                        "pose_detected"
                    ] = False

                else:

                    self._latest_metrics = {
                        "pose_detected": False
                    }

        # =========================================================
        # RETURN VIDEO FRAME
        # =========================================================

        return av.VideoFrame.from_ndarray(
            image,
            format="bgr24"
        )