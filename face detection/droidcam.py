from PIL import Image
import pytesseract

black = (0, 0, 0)
white = (255, 255, 255)
threshold = (160, 160, 160)

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

path = './captured/image150_20240319-060738.jpg'
# Open input image in grayscale mode and get its pixels.
img = Image.open(path).convert("LA")
pixels = img.getdata()


newPixels = []

# Compare each pixel 
for pixel in pixels:
    if pixel < threshold:
        newPixels.append(black)
    else:
        newPixels.append(white)

# Create and save new image.
newImg = Image.new("RGB", img.size)
newImg.putdata(newPixels)
newImg.save("newImage.jpg")

text = pytesseract.image_to_string('newImage.jpg', lang='eng')
print(text)
