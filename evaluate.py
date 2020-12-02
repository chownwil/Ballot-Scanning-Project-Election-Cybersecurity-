from keras.models import load_model
import cv2


model = load_model('cnn2_model')

#FIX ME change filepath
img = cv2.imread("00/00/000001.jpg", cv2.IMREAD_GRAYSCALE)

#FIX ME add bubble positions
bubble_positions = [ [657, 291], [657, 365], [657, 439], [657, 513], [657, 589], [557, 664], [657, 746], [657, 827] ]

bubbles = []

for t in bubble_positions:
	x=t[0]
	y=t[1]
	bubbles.append(img[y:y+40,x:x+60])

X = [cv2.resize(bubbble, (28, 28)) for bubble in bubbles]

X_data = np.array(X)

X_data = X_data.astype('float32')
X_data /= X_data/255

model.predict(X_test)
pred_labels = pred_probs.argmax(axis=-1)

print(pred_labels)