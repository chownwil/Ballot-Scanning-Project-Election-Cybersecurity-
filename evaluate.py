from keras.models import load_model
import cv2
import numpy as np

model = load_model('cnn2_model')

#FIX ME change filepath
img = cv2.imread("bubbles_final/014081_0_0_3.jpg", cv2.IMREAD_GRAYSCALE) 

bubbles = []

bubbles.append(img)

X = [cv2.resize(bubble, (28, 28)) for bubble in bubbles]

X = [np.reshape(x, (28,28,1)) for x in X]

X_data = np.array(X)
# breakpoint()

X_data = X_data.astype('float32')
X_data /= 255

pred_probs = model.predict(X_data)
pred_labels = pred_probs.argmax(axis=-1)

print(pred_probs)
print(pred_labels)

# 0 - not filled in
# 1 - fully filled in
# 2 - X mark
# 3  - Check
# 4 - fully bubbled and crossed out
# 5 - bad data
# 6 - other