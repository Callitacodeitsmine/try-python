from flask import Flask, render_template, request
import cv2
import numpy as np

app = Flask(__name__)

@app.route('/')
def form():
   return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
   name = request.form['name']
   photo = request.files['photo']
   company = request.form['company']
   video_choice = request.form.get('video_choice')

   def trying(video_file):
      if video_choice == 'Assamese':
         video_file = 'Video/03_Diabetes and Complications_Assamese.mp4'
      elif video_choice == 'Gujarati':
         video_file = 'Video/03_Diabetes and Complications_Gujarati.mp4'
      elif video_choice == 'Hindi':
         video_file = 'Video/03_Diabetes and Complications_Hindi.mp4'
      elif video_choice == 'Kannada':
         video_file = 'Video/03_Diabetes and Complications_Kannada.mp4'
      elif video_choice == 'Malayalam':
         video_file = 'Video/03_Diabetes and Complications_Malayalam.mp4'
      elif video_choice == 'Marathi':
         video_file = 'Video/03_Diabetes and Complications_Marathi.mp4'
      elif video_choice == 'Tamil':
         video_file = 'Video/03_Diabetes and Complications_Tamil.mp4'
      elif video_choice == 'Telugu':
         video_file = 'Video/03_Diabetes and Complications_Telugu.mp4'
      return video_choice
   video_file = trying(video_choice)

   # Save the uploaded photo to a temporary location
   file_path = 'temp/' + photo.filename
   photo.save(file_path)

   # Load the video
   video = cv2.VideoCapture(video_file)

   # Get the frame count
   frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

   # Get the frame width and height
   frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
   frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

   # Create a video writer
   out = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 30, (frame_width, frame_height))

   # Loop through the frames
   for i in range(frame_count):
      ret, frame = video.read()

      # Add the form data to the frame
      cv2.putText(frame, name, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
      cv2.putText(frame, company, (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
      logo = cv2.imread(file_path)
      frame[:logo.shape[0], :logo.shape[1]] = logo

      # Write the frame to the output video
      out.write(frame)

   # Release the video writer
   out.release()

   # Release the video
   video.release()

   return render_template('submit.html', name=name, photo=photo.filename, company=company)

if __name__ == '__main__':
   app.run(debug=True)