import numpy as np 
import pandas as pd 

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data
import csv
from torch.autograd import Variable

from sklearn.model_selection import train_test_split

class CNN(nn.Module):
	def __init__(self):
		super(CNN, self).__init__()
		self.conv1 = nn.Conv2d(1, 32, kernel_size=5)
		self.conv2 = nn.Conv2d(32, 32, kernel_size=5)
		self.conv3 = nn.Conv2d(32,64, kernel_size=5)
		self.fc1 = nn.Linear(3*3*64, 256)
		self.fc2 = nn.Linear(256, 7) # edit based on classes

	def forward(self, x):
		x = F.relu(self.conv1(x))
		#x = F.dropout(x, p=0.5, training=self.training)
		x = F.relu(F.max_pool2d(self.conv2(x), 2))
		x = F.dropout(x, p=0.5, training=self.training)
		x = F.relu(F.max_pool2d(self.conv3(x),2))
		x = F.dropout(x, p=0.5, training=self.training)
		x = x.view(-1,3*3*64 )
		x = F.relu(self.fc1(x))
		x = F.dropout(x, training=self.training)
		x = self.fc2(x)
		return F.log_softmax(x, dim=1)


def fit(model, train_loader):
	optimizer = torch.optim.Adam(model.parameters())#,lr=0.001, betas=(0.9,0.999))
	error = nn.CrossEntropyLoss()
	EPOCHS = 5
	model.train()
	for epoch in range(EPOCHS):
		correct = 0
		for batch_idx, (X_batch, y_batch) in enumerate(train_loader):
			breakpoint()
			var_X_batch = Variable(X_batch).float()
			var_y_batch = Variable(y_batch)
			optimizer.zero_grad()
			output = model(var_X_batch)
			loss = error(output, var_y_batch)
			loss.backward()
			optimizer.step()

			# Total correct predictions
			predicted = torch.max(output.data, 1)[1] 
			correct += (predicted == var_y_batch).sum()
			#print(correct)
			if batch_idx % 50 == 0:
				print('Epoch : {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}\t Accuracy:{:.3f}%'.format(
					epoch, batch_idx*len(X_batch), len(train_loader.dataset), 100.*batch_idx / len(train_loader), loss.data[0], float(correct*100) / float(BATCH_SIZE*(batch_idx+1))))


def evaluate(model):
#model = mlp
	correct = 0 
	for test_imgs, test_labels in test_loader:
		#print(test_imgs.shape)
		test_imgs = Variable(test_imgs).float()
		output = model(test_imgs)
		predicted = torch.max(output,1)[1]
		correct += (predicted == test_labels).sum()
	print("Test accuracy:{:.3f}% ".format( float(correct) / (len(test_loader)*BATCH_SIZE)))


def main():
	ydf = pd.read_csv('y.csv')
	Y = ydf['Label'].values
	for i in range(len(Y)):
		if (Y[i] == 4) or (Y[i] == 5):
			Y[i] = 1
		if Y[i] > 5:
			Y[i] -= 2
	
	X = []
	with open("X0.csv", 'r', newline='') as myfile:
		rr = csv.reader(myfile)
		for x in rr:
			x = [int(x_temp) for x_temp in x]
			x = np.reshape(x, (1,28,28))
			X.append(x)
	
	with open("X1.csv", 'r', newline='') as myfile:
		rr = csv.reader(myfile)
		for x in rr:
			x = [int(x_temp) for x_temp in x]
			x = np.reshape(x, (1,28,28))
			X.append(x)
			
	with open("X2.csv", 'r', newline='') as myfile:
		rr = csv.reader(myfile)
		for x in rr:
			x = [int(x_temp) for x_temp in x]
			x = np.reshape(x, (1,28,28))
			X.append(x)
			
	with open("X3.csv", 'r', newline='') as myfile:
		rr = csv.reader(myfile)
		for x in rr:
			x = [int(x_temp) for x_temp in x]
			x = np.reshape(x, (1,28,28))
			X.append(x)
	"""
	with open("X1.csv", 'r', newline='') as myfile:
		breakpoint()
		rr = csv.reader(myfile)
		for x in rr:
			im = []
			for x_temp in x:
				im.append(x_temp.strip("[]").replace("\n","").split(" "))
			X.append(im)
	with open("X2.csv", 'r', newline='') as myfile:
		rr = csv.reader(myfile)
		for x in rr:
			im = []
			for x_temp in x:
				im.append(x_temp.strip("[]").replace("\n","").split(" "))
			X.append(im)
	"""

	BATCH_SIZE = 32

	print('X shape', len(X))
	print('Y shape', len(Y))


	X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.15)

	torch_X_train = torch.FloatTensor(X_train)
	torch_y_train = torch.from_numpy(y_train).type(torch.FloatTensor) 	
	torch_X_test = torch.FloatTensor(X_test)
	torch_y_test = torch.from_numpy(y_test).type(torch.FloatTensor) 

	# torch_X_train_tensor = torch.tensor(torch_X_train, dtype=torch.long, device='cpu')
	# torch_y_train_tensor = torch.tensor(torch_y_train, dtype=torch.long, device='cpu')

	# torch_X_test_tensor = torch.tensor(torch_X_test, dtype=torch.long, device='cpu')
	# torch_y_test_tensor = torch.tensor(torch_y_test, dtype=torch.long, device='cpu')

	# Pytorch train and test sets
	train = torch.utils.data.TensorDataset(torch_X_train,torch_y_train)
	test = torch.utils.data.TensorDataset(torch_X_test,torch_y_test)

	# data loader
	train_loader = torch.utils.data.DataLoader(train, batch_size = BATCH_SIZE, shuffle = False)
	test_loader = torch.utils.data.DataLoader(test, batch_size = BATCH_SIZE, shuffle = False)

	cnn = CNN()
	
	print(cnn)

	it = iter(train_loader)
	X_batch, y_batch = next(it)
	print(cnn.forward(X_batch).shape)

	fit(cnn,train_loader) # train

	evaluate(cnn) # eval


if __name__ == "__main__":
	main()
