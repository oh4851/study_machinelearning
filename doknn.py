from numpy import *
import math
import operator

def mat2arr(data_mat):
	return array(map(lambda x:map(float,x),data_mat))

def list2arr(data_list):
	return array(map(float,data_list))

def readdata(filename, ho_ratio):
	fr = open(filename, 'r')
	lines = fr.readlines()
	lnum_test = math.ceil(len(lines) * ho_ratio)
	lnum_train = len(lines) - lnum_test
	colmax = len(lines[0].strip().split('\t'))
	mat_train = []
	lbl_train = []
	mat_test = []
	lbl_test = []
	train_index = 0
	test_index = 0
	split_index = 0

	if ho_ratio != 0:
		split_index = 1.0 / ho_ratio

	for line in lines:
		listFromLine = line.strip().split('\t')
		listFromLine.pop(2)	# remove gender element
		listFromLine.pop(4)	# remove style element
		if ho_ratio == 0 or (train_index + test_index) % split_index != 0:
			mat_train.append(listFromLine[1:colmax])
			lbl_train.append(listFromLine[0])
			train_index += 1
		else:
			mat_test.append(listFromLine[1:colmax])
			lbl_test.append(listFromLine[0])
			test_index += 1

	if ho_ratio == 0:
		return mat_train, lbl_train
	else:
		return mat_train, lbl_train, mat_test, lbl_test
	
	fr.close()

class knn:
	def __init__(self, mat_data,label_data,k):
		if mat_data.__class__.__name__ != 'ndarray':
			mat_data = mat2arr(mat_data)
		self.mat_data = mat_data
		self.label_data = label_data
		self.train_size = mat_data.shape[0]
		self.k = k

	# compare distance from all mat_data rows and choose most closer one
	def predict(self, array_input):
		if array_input.__class__.__name__ != 'ndarray':
			array_input = list2arr(array_input)

		diff_mat = tile(array_input, (self.train_size,1)) - self.mat_data
		pow_diff_mat = diff_mat ** 2
		pow_distances = pow_diff_mat.sum(axis=1)
		distances = pow_distances ** 0.5
		sorted_distances = distances.argsort()

		class_count = {}
		for i in range(self.k):
			kth_label = self.label_data[sorted_distances[i]]
			class_count[kth_label] = class_count.get(kth_label, 0) + 1

		sorted_class_count = sorted(class_count.iteritems(),\
			key=operator.itemgetter(1),reverse=True)

		return sorted_class_count[0][0]
'''
# testing knn
print "=== Testing KNN ==="
simple_mat_1 = [[1.0,1.1] , [1.0,1.0], [0,0], [0,0.1]]
simple_label_1 = ['A','A','B','B']
knn_test = knn(simple_mat_1, simple_label_1, 3)
print "knn predict [0.9,0.9] : " + str(knn_test.predict([0.9,0.9]))
print "knn predict [0.1,0.4] : " + str(knn_test.predict([0.1,0.4]))
'''
# real knn
print "=== Real KNN ==="
mat_train, lbl_train, mat_test, lbl_test = readdata("./horse_10000.dat", 0.1)
knn_real = knn(mat_train, lbl_train, 3)
error_cnt = 0
for i in range(len(mat_test)):
	predicted = knn_real.predict(mat_test[i])
	print "ANSWER: " + lbl_test[i] + " REAL: " + predicted
	if lbl_test[i] != predicted:
		error_cnt += 1

error_ratio = float(error_cnt) / float(len(mat_test))
print "\n=== RESULT ==="
print "Test data size: ", len(mat_test)
print "Test data error: ", error_cnt
print "Fail to predict: ", error_ratio, "[", error_ratio * 100,"%]"