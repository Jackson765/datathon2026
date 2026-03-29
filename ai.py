import cv2
from ultralytics import YOLO
import torch

# 1. Check for your 3050 Ti GPU
device = '0' if torch.cuda.is_available() else 'cpu'
print(f"🚀 Running on: {'NVIDIA RTX 3050 Ti' if device == '0' else 'CPU'}")

# 2. Load the Brains (Ensure 'best.pt' is in this folder!)
try:
    choking_model = YOLO('best.pt')  # Your custom model
    pose_model = YOLO('yolov8n-pose.pt') # Official skeleton model
except Exception as e:
    print(f"❌ Error: Could not find your model file. Is 'best.pt' in this folder? \n{e}")
    exit()

# 3. Access Local Webcam
cap = cv2.VideoCapture(0)

print("✅ System Live. Press 'q' to exit.")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # --- DETECTION 1: CHOKING (Object Detection) ---
    # We use .to(device) to force it onto your 3050 Ti
    choking_results = choking_model.predict(source=frame, conf=0.75, device=device, verbose=False)
    annotated_frame = choking_results[0].plot()

    # --- DETECTION 2: FALLING (Pose Logic) ---
    pose_results = pose_model.predict(source=frame, conf=0.5, device=device, verbose=False)
    
    if len(pose_results[0].boxes) > 0:
        for box in pose_results[0].boxes:
            # Get box coordinates
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            w = x2 - x1
            h = y2 - y1
            
            # If the bounding box is wider than it is tall, trigger Fall Alert
            if w > h:
                cv2.rectangle(annotated_frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 4)
                cv2.putText(annotated_frame, "!!! FALL DETECTED !!!", (int(x1), int(y1)-15), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    # 4. Show the Live Feed
    cv2.imshow("Datathon 2026 - Emergency AI", annotated_frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()