import cv2  # pip install opencv-python
import glob
import os

def create_video_opencv(image_folder=".", pattern="screenshot*.png",
                        output="timelapse01.mp4", fps=1):
    """Erstellt Video mit OpenCV"""
    images = sorted(glob.glob(os.path.join(image_folder, pattern)))

    if not images:
        print("Keine Bilder gefunden!")
        return

    # Erste Bild laden um Dimensionen zu bekommen
    frame = cv2.imread(images[0])
    height, width, layers = frame.shape

    # Video Writer erstellen
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output, fourcc, fps, (width, height))

    for image_path in images:
        print(f"Füge hinzu: {image_path}")
        frame = cv2.imread(image_path)
        video.write(frame)

    video.release()
    print(f"Video erstellt: {output}")

# Verwendung:

create_video_opencv(fps=2)