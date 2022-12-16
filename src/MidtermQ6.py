#!/usr/bin/env python

# MidtermQ6.py - extract & plot facial expressions from videos with one or two faces
# phat_sumo (ethan payne) - 10/25/22
# ethan dot payne at usu dot edu 

import os
import sys
import argparse
import matplotlib.pyplot as plt
import pandas as pd
from fer import FER
from fer import Video

def analyze_video(input_video, input_file, output_path, two_faces):
	# init detection object
	face_detector = FER(mtcnn=True)

	# The Analyze() function will run analysis on every frame of the input video. 
	# It will create a rectangular box around every image and show the emotion values next to that.
	# Finally, the method will publish a new video that will have a box around the face of the human with live emotion values.
	processing_data = input_video.analyze(face_detector, display=False)

	if (two_faces):
		# We will now convert the analysed information into a dataframe.
		# This will help us import the data as a .CSV file to perform analysis over it later
		vid_df = input_video.to_pandas(processing_data)
		vid_df = input_video.get_emotions(vid_df)

		# We will now work on the dataframe to extract which emotion was prominent in the video
		# angry0 = sum(vid_df.angry0)
		# disgust0 = sum(vid_df.disgust0)
		# fear0 = sum(vid_df.fear0)
		# happy0 = sum(vid_df.happy0)
		# sad0 = sum(vid_df.sad0)
		# surprise0 = sum(vid_df.surprise0)
		# neutral0 = sum(vid_df.neutral0)


		# angry1 = sum(vid_df.angry1)
		# disgust1 = sum(vid_df.disgust1)
		# fear1 = sum(vid_df.fear1)
		# happy1 = sum(vid_df.happy1)
		# sad1 = sum(vid_df.sad1)
		# surprise1 = sum(vid_df.surprise1)
		# neutral1 = sum(vid_df.neutral1)

		# split each face from the pandas dataframe
		columns = [x for x in vid_df.columns if x[-1] == "0"]
		new_columns = [x[:-1] for x in columns]
		first_df = vid_df[columns]
		first_df.columns = new_columns

		columns = [x for x in vid_df.columns if x[-1] == "1"]
		new_columns = [x[:-1] for x in columns]
		second_df = vid_df[columns]
		second_df.columns = new_columns

		# emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
		# emotions_values0 = [angry0, disgust0, fear0, happy0, sad0, surprise0, neutral0]
		# emotions_values1 = [angry1, disgust1, fear1, happy1, sad1, surprise1, neutral1]

		# Plotting the emotions against time in the video
		pltfig0 = first_df.plot(figsize=(20, 8), fontsize=16).get_figure()

		pltfig0.show()

		pltfig0.savefig(f"{output_path}/{input_file.split('.')[0]}-face1-plot.png")

		pltfig1 = second_df.plot(figsize=(20, 8), fontsize=16).get_figure()

		pltfig1.show()

		pltfig1.savefig(f"{output_path}/{input_file.split('.')[0]}-face2-plot.png")
	
	else:
		# We will now convert the analysed information into a dataframe.
		# This will help us import the data as a .CSV file to perform analysis over it later
		vid_df = input_video.to_pandas(processing_data)
		vid_df = input_video.get_first_face(vid_df)
		vid_df = input_video.get_emotions(vid_df)

		# Plotting the emotions against time in the video
		pltfig = vid_df.plot(figsize=(20, 8), fontsize=16).get_figure()

		# We will now work on the dataframe to extract which emotion was prominent in the video
		# angry = sum(vid_df.angry)
		# disgust = sum(vid_df.disgust)
		# fear = sum(vid_df.fear)
		# happy = sum(vid_df.happy)
		# sad = sum(vid_df.sad)
		# surprise = sum(vid_df.surprise)
		# neutral = sum(vid_df.neutral)

		# emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
		# emotions_values = [angry, disgust, fear, happy, sad, surprise, neutral]

		# score_comparisons = pd.DataFrame(emotions, columns = ['Human Emotions'])
		# score_comparisons['Emotion Value from the Video'] = emotions_values
		# score_comparisons

		plt.savefig(f"{output_path}/{input_file.split('.')[0]}-plot.png")

if __name__ == "__main__": 

	output_path = "q6-output"

	parser = argparse.ArgumentParser(description="process video files to extract human expression")
	parser.add_argument("input_file", type=str, 
										   help="video file to process")
	parser.add_argument("--output", "-o", type=str, required=False, default=output_path,
										   help=f"output directory for videos and plots [default: {output_path}]")
	parser.add_argument("--two-faces", "-t", dest="two_faces", action="store_true", default=False,
										 help="enable two-face processing [default: first face only]")
	args = parser.parse_args(sys.argv[1:])

	input_file = args.input_file
	output_path = args.output.removesuffix('/')
	two_faces = args.two_faces

	input_video = None
	# load videos in as Video objects
	# video_one = Video(video_file=file_one, outdir="q6-output")
	# video_two = Video(video_file=file_two, outdir="q6-output")
	if (two_faces):
		input_video = Video(video_file=input_file, outdir=output_path, first_face_only=False)
	else: 
		input_video = Video(video_file=input_file, outdir=output_path)

	# split file name from it's path and it's extension for naming the output plot
	input_file = input_file.split('/')[-1].split('.')[0]

	# analyze_video(video, input_file, output_path, two_faces)

	# init detection object
	face_detector = FER(mtcnn=True)

	# The Analyze() function will run analysis on every frame of the input video. 
	# It will create a rectangular box around every image and show the emotion values next to that.
	# Finally, the method will publish a new video that will have a box around the face of the human with live emotion values.
	processing_data = input_video.analyze(face_detector, display=False)

	if (two_faces):
		# We will now convert the analysed information into a dataframe.
		# This will help us import the data as a .CSV file to perform analysis over it later
		vid_df = input_video.to_pandas(processing_data)
		vid_df = input_video.get_emotions(vid_df)

		# We will now work on the dataframe to extract which emotion was prominent in the video
		# angry0 = sum(vid_df.angry0)
		# disgust0 = sum(vid_df.disgust0)
		# fear0 = sum(vid_df.fear0)
		# happy0 = sum(vid_df.happy0)
		# sad0 = sum(vid_df.sad0)
		# surprise0 = sum(vid_df.surprise0)
		# neutral0 = sum(vid_df.neutral0)


		# angry1 = sum(vid_df.angry1)
		# disgust1 = sum(vid_df.disgust1)
		# fear1 = sum(vid_df.fear1)
		# happy1 = sum(vid_df.happy1)
		# sad1 = sum(vid_df.sad1)
		# surprise1 = sum(vid_df.surprise1)
		# neutral1 = sum(vid_df.neutral1)

		# split each face from the pandas dataframe
		columns = [x for x in vid_df.columns if x[-1] == "0"]
		new_columns = [x[:-1] for x in columns]
		first_df = vid_df[columns]
		first_df.columns = new_columns

		columns = [x for x in vid_df.columns if x[-1] == "1"]
		new_columns = [x[:-1] for x in columns]
		second_df = vid_df[columns]
		second_df.columns = new_columns

		# emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
		# emotions_values0 = [angry0, disgust0, fear0, happy0, sad0, surprise0, neutral0]
		# emotions_values1 = [angry1, disgust1, fear1, happy1, sad1, surprise1, neutral1]

		# Plotting the emotions against time in the video
		pltfig0 = first_df.plot(figsize=(20, 8), fontsize=16).get_figure()

		pltfig0.show()

		pltfig0.savefig(f"{output_path}/{input_file.split('.')[0]}-face1-plot.png")

		pltfig1 = second_df.plot(figsize=(20, 8), fontsize=16).get_figure()

		pltfig1.show()

		pltfig1.savefig(f"{output_path}/{input_file.split('.')[0]}-face2-plot.png")
	
	else:
		# We will now convert the analysed information into a dataframe.
		# This will help us import the data as a .CSV file to perform analysis over it later
		vid_df = input_video.to_pandas(processing_data)
		vid_df = input_video.get_first_face(vid_df)
		vid_df = input_video.get_emotions(vid_df)

		# Plotting the emotions against time in the video
		pltfig = vid_df.plot(figsize=(20, 8), fontsize=16).get_figure()

		# We will now work on the dataframe to extract which emotion was prominent in the video
		# angry = sum(vid_df.angry)
		# disgust = sum(vid_df.disgust)
		# fear = sum(vid_df.fear)
		# happy = sum(vid_df.happy)
		# sad = sum(vid_df.sad)
		# surprise = sum(vid_df.surprise)
		# neutral = sum(vid_df.neutral)

		# emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
		# emotions_values = [angry, disgust, fear, happy, sad, surprise, neutral]

		# score_comparisons = pd.DataFrame(emotions, columns = ['Human Emotions'])
		# score_comparisons['Emotion Value from the Video'] = emotions_values
		# score_comparisons

		plt.savefig(f"{output_path}/{input_file.split('.')[0]}-plot.png")
