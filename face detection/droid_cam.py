import os
import cv2
import time
import easyocr
import shutil
from PIL import Image, ImageEnhance, ImageFilter

if not os.path.exists('./captured'):
	os.mkdir('./captured')
if not os.path.exists('new_img'):
	os.mkdir('new_img')

ip_address = '192.168.43.1'
port = '4747'
video = 880 * 580

url = f'http://{ip_address}:{port}/mjpegfeed{video}?'

left = 100
upper = 1000
right = 500
lower = 1000

cap = cv2.VideoCapture(url)
frame_count = 0

while True:
	ret, frame = cap.read()
	
	if not ret:
		break
	
	# Incrémentez le compteur de trames
	# Incrementing the counter
	frame_count += 1
	
	# Si le compteur de trames correspond à 5 secondes (à 30 FPS)
	# if the counter is 5 secondes (by 30 FPS)
	if frame_count == 5 * 30:
		# Capturer l'image
		# Capture the image
		
		cv2.imwrite("./captured/image{}_{}.jpg".format(frame_count, time.strftime("%Y%m%d-%H%M%S")), frame)
		frame_count = 0  # Reinitialise the counter
		
	
	# Affichez la vidéo en direct
	# show the video on live
	cv2.imshow('Video', frame)
	
	# Quitter la boucle si la touche 'q' est enfoncée
	# press q to leave the loop
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# Libérez la vidéo et détruisez toutes les fenêtres OpenCV
# free the video and destroy all the OpenCV windows
cap.release()
cv2.destroyAllWindows()

path_cap = './captured/'
for i in os.listdir(path_cap):
	if os.path.isfile(os.path.join(path_cap, i)):
		print(i)
		time.sleep(2)
		
		# path = "C:/Users/jorda/Pictures/Screenshots/Capture d'écran 2024-03-10 082143.png"
		img = Image.open(f'./captured/{str(i)}')
		time.sleep(1)
		img = img.convert('RGBA')
		img_cropped = img.crop((left, upper, right, lower))
		time.sleep(1)
		pix = img.load()
		
		time.sleep(2)
		img.save('./new_img/image{}.png'.format(time.strftime("%H%M%S")))


for imgs in os.listdir('new_img'):
	if os.path.isfile(os.path.join('./new_img', imgs)):
		# time.sleep(2)
		paths = f'./new_img/{imgs}'
		# print(paths)
		
		reader = easyocr.Reader(['en'], gpu=False)
		result = reader.readtext(paths, detail=0)
		print(f'easyocr text from {paths}: {result}\n')

shutil.rmtree('./captured')
shutil.rmtree('./new_img')
print("\nFile successfully deleted.")

