from tkinter import *
from tkinter import filedialog
import customtkinter
from PIL import ImageTk, Image, ImageFilter
import cv2
import numpy as np
from keras.models import load_model
import login  # Import the login module to access get_username()
import sqlite3

# Load the trained model
# model = load_model('final_model11.h5')
model = load_model(r'C:\Users\ROG\Desktop\HCK\FYP\code2\final_model7.h5')


# Dictionary mapping label indices to emotions
labels_dict = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Neutral', 5: 'Sad', 6: 'Surprise'}

def logout():
    app.destroy()
    login.main()

# Function to detect emotion from an image
def detect_emotion(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)

    for x, y, w, h in faces:
        sub_face_img = gray[y:y+h, x:x+w]
        resized = cv2.resize(sub_face_img, (48, 48))
        normalize = resized / 255.0
        reshaped = np.reshape(normalize, (1, 48, 48, 1))
        result = model.predict(reshaped)
        label_index = np.argmax(result, axis=1)[0]
        emotion_label = labels_dict[label_index]
        accuracy = result[0][label_index]  # Confidence score of the predicted emotion
        accuracy_percent = round(accuracy * 100, 2)

        # Draw rectangle around the detected face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Display emotion label and accuracy
        text = f"{emotion_label}: {accuracy_percent}%"
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

    return frame

# Function to handle file upload button
def upload_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        frame = cv2.imread(file_path)
        frame_with_emotion = detect_emotion(frame)
        cv2.namedWindow("Emotion Detection", cv2.WINDOW_NORMAL)  # Create a window that can be resized
        cv2.resizeWindow("Emotion Detection", frame.shape[1], frame.shape[0])  # Resize to fit the image
        cv2.imshow("Emotion Detection", frame_with_emotion)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# Function to start webcam and detect emotions
def start_webcam():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        frame_with_emotion = detect_emotion(frame)
        cv2.imshow("Emotion Detection", frame_with_emotion)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

# Create CustomTkinter window
app = customtkinter.CTk()
app.geometry("800x600")
app.title('FaceFury')

# Load the Haar cascade for face detection
faceDetect = cv2.CascadeClassifier(r'C:\Users\ROG\Desktop\HCK\FYP\code2\haarcascade_frontalface_default.xml')

# UI components
img1 = customtkinter.CTkLabel(master=app, text="Emotion Detection", font=('Century Gothic', 20))
img1.place(relx=0.5, rely=0.3, anchor=CENTER)

# Button to upload image
upload_button = customtkinter.CTkButton(master=app, width=220, text='Upload Image', corner_radius=6, command=upload_image)
upload_button.place(relx=0.5, rely=0.4, anchor=CENTER)

# Button to start webcam
webcam_button = customtkinter.CTkButton(master=app, width=220, text='Start Webcam', corner_radius=6, command=start_webcam)
webcam_button.place(relx=0.5, rely=0.5, anchor=CENTER)

logout_button = customtkinter.CTkButton(master=app, width=80, text='Logout', corner_radius=6, command=logout)
logout_button.place(relx=1.0, rely=0, anchor=NE, x=-10, y=10)

app.resizable(False, False)
app.mainloop()

