import cv2
import matplotlib.pyplot as plt

# This uses MobileNet-SSD v3 weights and config found here: https://github.com/opencv/opencv/wiki/TensorFlow-Object-Detection-API

config_file = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
frozen_model = 'frozen_inference_graph.pb'

model = cv2.dnn_DetectionModel(frozen_model, config_file)

classLabels = []
file_name = 'labels.txt'
with open(file_name, 'rt') as fpt:
	classLabels = fpt.read().rstrip('\n').split('\n')

model.setInputSize(320,320)
model.setInputScale(1.0/127.5)
model.setInputMean((127.5, 127.5, 127.5))
model.setInputSwapRB(True)

for i in range (1, 11):
	if (i < 5):
		img = cv2.imread(f'plantImages/crop_{i}.jpeg')
	else:
		img = cv2.imread(f'plantImages/weed_{i-4}.jpeg')
	ClassIndex, confidence, bbox = model.detect(img, 0.4)

	if len(ClassIndex) >= 1:
		font_scale = 3
		font = cv2.FONT_HERSHEY_PLAIN
		for ClassInd, conf, boxes in zip(ClassIndex.flatten(), confidence.flatten(), bbox):
			cv2.rectangle(img, boxes, (255, 0, 0), 2)
			cv2.putText(img, classLabels[ClassInd-1], (boxes[0]+10, boxes[1]+40), font, fontScale=font_scale, color=(0, 0, 255), thickness=3)

		plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
		plt.show()
	else:
		print(f"Unable to Classify Image #{i}")