import argparse, time, cv2
from loguru import logger
from src.road_incident_detection.video import open_source
from src.road_incident_detection.detectors.motion import MotionIncidentDetector

def parse_args():
    p = argparse.ArgumentParser(description="Road Incident Detection — baseline")
    p.add_argument("--source", default="0", help="Video source: 0 for webcam or path to file")
    p.add_argument("--min-area", type=int, default=8000, help="Min contour area to consider")
    p.add_argument("--sustain-frames", type=int, default=30, help="Frames to sustain before flagging incident")
    p.add_argument("--save", action="store_true", help="Save annotated output to runs/annotated.mp4")
    p.add_argument("--display", action="store_true", help="Display window")
    return p.parse_args()

def main():
    args = parse_args()
    source = int(args.source) if args.source.isdigit() else args.source
    cap = open_source(source)
    det = MotionIncidentDetector(min_area=args.min_area, sustain_frames=args.sustain_frames)

    out = None
    if args.save:
        import os
        os.makedirs("runs", exist_ok=True)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        w  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps= cap.get(cv2.CAP_PROP_FPS) or 25.0
        out = cv2.VideoWriter("runs/annotated.mp4", fourcc, fps, (w, h))

    logger.info("Starting stream...")
    t0 = time.time(); frames = 0
    incidents = 0

    while True:
        ret, frame = cap.read()
        if not ret: break

        incident, boxes = det.process(frame)
        for (x,y,w,h) in boxes:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)

        if incident:
            incidents += 1
            cv2.putText(frame, f"INCIDENT #{incidents}", (20,40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,255), 2)

        if out is not None:
            out.write(frame)
        if args.display:
            cv2.imshow("Road Incident Detection", frame)
            if cv2.waitKey(1) & 0xFF == 27:  # ESC
                break

        frames += 1

    cap.release()
    if out is not None:
        out.release()
    if args.display:
        cv2.destroyAllWindows()

    elapsed = max(1e-6, time.time() - t0)
    logger.info(f"Done. Frames={frames}, Incidents flagged={incidents}, FPS~{frames/elapsed:.2f}")

if __name__ == "__main__":
    main()
