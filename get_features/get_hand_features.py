def get_hand_features(raw_data='', m=84, keypoint1=13, keypoint2=16):
	"""
	Parameters
	----------
	npy_file
	m:
	   without trimmming: m = 84
	   with trimming: m = 51
	keypoint
	coordinate
	Returns
	-------
	"""
	smax=200
	res = []
	data_coord = []
	d1_res =[]
	d2_res =[]
	for coordinate in range(3):
		data1 = raw_data[:, keypoint1, coordinate]
		data1_reshaped = data1.reshape((-1,))
		d1_res.append(data1)
		#print("Data 1 reshape", np.shape(data1_reshaped))
		data2 = raw_data[:, keypoint2, coordinate]
		data2_reshaped = data2.reshape((-1,))   
		#print("data 2 shape ", np.shape(data2))
		d2_res.append(data2)
        # euclidean distance ...
		data_subtract = np.subtract(data1, data2)
		data_coord.append(data_subtract)
		flg = 'stats' #'stats', wavelet, std
		if flg == 'fft':
			fft_features = _get_fft(data, fft_bin=m)
			fft_features = fft_features[0:1 + int(np.ceil((m - 1) / 2))]
		elif flg ==' hand':
			print("hand")
		elif flg == 'std':
			fft_features_1 = [np.mean(data), np.std(data)]
			print("fft features 1 shape ", np.shape(fft_features_1))
			fft_features = list(np.quantile(data, q=[0, 0.25, 0.5, 0.75, 1]))

		#res.append(fft_features)
    # euclidean distance
	eu_dist = np.sqrt(np.square(data_coord[0])+np.square(data_coord[1])+np.square(data_coord[2]))
	#return np.asarray(res).reshape(-1, )
    # reutrn mean, min , max of distances ?
	from scipy.stats import moment
	outputs = []
	eu_data = eu_dist
	eu_features= [np.mean(eu_data), np.std(eu_data)]#, moment(eu_data, moment=3), np.min(eu_data), np.max(eu_data)]
	return eu_features #, d1_res, d2_res
