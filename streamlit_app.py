import streamlit as st
import face_recognition
import numpy as np
import pandas as pd
import os
import cv2
from datetime import datetime
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

st.title("📱 Mobile Face Attendance System")

# Load students
students = pd.read_csv("students.csv")

known_encodings = []
known_ids = []

# Load face images
for file in os.listdir("faces"):
    img = face_recognition.load_image_file(f"faces/{file}")
    encoding = face_recognition.face_encodings(img)[0]

    known_encodings.append(encoding)
    known_ids.append(file.split(".")[0])

attendance = set()

class FaceAttendance(VideoTransformerBase):

    def transform(self, frame):

        img = frame.to_ndarray(format="bgr24")

        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        faces = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, faces)

        for encoding, face_location in zip(encodings, faces):

            matches = face_recognition.compare_faces(
                known_encodings,
                encoding
            )

            name = "Unknown"

            if True in matches:

                index = matches.index(True)
                name = known_ids[index]

                attendance.add(name)

            top, right, bottom, left = face_location

            cv2.rectangle(
                img,
                (left, top),
                (right, bottom),
                (0,255,0),
                2
            )

            cv2.putText(
                img,
                name,
                (left, top-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,255,0),
                2
            )

        return img

webrtc_streamer(
    key="attendance",
    video_transformer_factory=FaceAttendance
)

if st.button("Save Attendance"):

    if attendance:

        df = pd.DataFrame(list(attendance), columns=["Register"])
        df["Date"] = datetime.now().date()

        if os.path.exists("attendance.csv"):
            df.to_csv("attendance.csv", mode="a", header=False, index=False)
        else:
            df.to_csv("attendance.csv", index=False)

        st.success("Attendance Saved")

        st.dataframe(df)
