import torch
import torchvision
import pandas as pd
import cv2

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Set device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load the video
video_path = 'test_video.mp4'
cap = cv2.VideoCapture(video_path)

# Get video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Define the codec for saving the video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_path = 'test_video_detect.mp4'

# Create VideoWriter object
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Perform object detection on the frame
    results = model(frame)

    # Get the detections
    detections = results.pandas().xyxy[0]

    # Filter the detections for specific classes (e.g., cars and person)
    desired_classes = ['car', 'person']
    filtered_detections = detections[detections['name'].isin(desired_classes)]

    # Display the filtered detections
    for idx, row in filtered_detections.iterrows():
        x_min, y_min, x_max, y_max = row[['xmin', 'ymin', 'xmax', 'ymax']]
        x_min, y_min, x_max, y_max = int(x_min), int(y_min), int(x_max), int(y_max)  # Convert coordinates to integers
        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
        class_label = row['name']
        cv2.putText(frame, class_label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Write the frame to the output video
    out.write(frame)

    # Display the frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
