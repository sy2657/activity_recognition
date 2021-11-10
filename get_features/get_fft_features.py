def get_fft_features(raw_data='', m=84, keypoint=7):
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
	for coordinate in range(3):
		data = raw_data[:, keypoint, coordinate]
		data = data.reshape((-1,))
		flg = 'stats' #'stats', wavelet, std
		if flg == 'fft':
			fft_features = _get_fft(data, fft_bin=m)
			fft_features = fft_features[0:1 + int(np.ceil((m - 1) / 2))]
		elif flg== 'wavelet':
            # trim data? 
            
            # wavelet transform
			cA, cD = pywt.dwt(data, wavelet='db2', mode='constant')
            
            # make all same length 
			s0 = np.shape(cA)[0]  
			trimmed_data = list(cA)
			if s0 >smax:
				trimmed_data= trimmed_data[:smax]
			else:
				minus = smax - s0
				for i in range(minus):
					trimmed_data.append(0)
                    
			print("shape ca is ", s0)
			print("shape trimmed data is ", np.shape(trimmed_data))

            
			fft_features = trimmed_data # cD
		elif flg == 'std':
			fft_features_1 = [np.mean(data), np.std(data)]
			print("fft features 1 shape ", np.shape(fft_features_1))
			fft_features = list(np.quantile(data, q=[0, 0.25, 0.5, 0.75, 1]))
		elif flg == 'moment':
			from scipy.stats import moment
			order1= 3
			order2= 4
			order3 =5
			fft_features= [moment(data, moment=order1), moment(data, moment=order2), moment(data, moment=order3) ] # use diff # or combination of features
            
			# fft_features = list(np.quantile(data, q = [0, 0.25, 0.5, 0.75, 1])) + [np.mean(data), np.std(data)]
		else:
			n = len(data)
			step = int(np.ceil(n / m))
			fft_features = []
			for i in range(0, len(data), step):
				vs = data[i:i + step]
				flg2 = 'all6' # stats
				if flg2 == 'all6':
					tmp = [np.mean(vs), np.std(vs), skew(vs), kurtosis(vs), np.min(vs), np.max(vs)]
					n_feat = len(tmp)
				elif flg2 == 'stats':
					# tmp = list(np.quantile(vs, q = [0, 0.5, 1] )) # [0, 0.25, 0.5, 0.75, 1]+ [np.mean(vs), np.std(vs)]
					# tmp = list(np.quantile(vs, q=[0, 0.5, 1]))
					tmp = [np.mean(vs), np.std(vs)]
					# tmp = [np.mean(vs)]
					n_feat = len(tmp)
				elif flg2:
					tmp = _get_fft(vs)
					tmp = sorted(tmp[0:1 + int(np.ceil((m - 1) / 2))], reverse=True)
					n_feat = 2
				fft_features.extend(tmp[:n_feat])
			fft_features = fft_features + [0] * (n_feat * m - len(fft_features))
		res.append(fft_features)
	return np.asarray(res).reshape(-1, )

def get_fft_features(raw_data='', m=84, keypoint=7, file=''):
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
	# print(file)

	flg = 'hand_direction'
	if flg == 'hand_direction':
		# start, end = trim(raw_data[:, -3])
		x, y = 0, 3
		head = raw_data[:, 10, x:y]
		left_shoulder = raw_data[:, 11, x:y]
		right_shoulder = raw_data[:, 14, x:y]
		left_elbow = raw_data[:, 12, x:y]
		right_elbow = raw_data[:, 15, x:y]
		left_wrist = raw_data[:, 13, x:y]
		right_wrist = raw_data[:, 16, x:y]

		d = right_wrist - left_wrist
		d2 = right_shoulder - left_shoulder
		d3 = right_elbow - left_elbow

		d11 = right_wrist[1:, :] - right_wrist[:-1, :]
		d22 = right_shoulder[1:, :] - right_shoulder[:-1, :]
		d33 = right_elbow[1:, :] - right_elbow[:-1, :]

		d111 = left_wrist[1:, :] - left_wrist[:-1, :]
		d222 = left_shoulder[1:, :] - left_shoulder[:-1, :]
		d333 = left_elbow[1:, :] - left_elbow[:-1, :]

		p = 3
		# res = stats(d ** p) + stats(d2 ** p) + stats(d3 ** p) + stats(d11 ** p) + stats(d22 ** p) + stats(d33 ** p) + stats(d111 ** p) + stats(d222 ** p) + stats(d333 ** p)
		res = [len(raw_data)]
		for i in range(11, 17):
			# 	# res += stats(raw_data[:, i, x:y], dim=1) #+ stats(raw_data[1:, i, x:y]-raw_data[:-1, i, x:y])
			res += stats(raw_data[:, i, x:y])
			for s in range(1, 50, 5):
				# res+= stats(raw_data[::s, i, x:y])
				res += stats(raw_data[s:, i, x:y] - raw_data[:-s, i, x:y])

		feature_name = []
		return res

	n = raw_data.shape[0]
	# only right keypoints
	raw_data = raw_data[:, [11, 12, 13, 14, 15, 16], :].reshape((n, -1))
	# raw_data = raw_data[:, :, :].reshape((n, -1))
	# raw_data = raw_data[:, [14, 16], :].reshape((n, -1))

	# raw_data = raw_data.reshape((n, 51))
	res = []

	for i in range(raw_data.shape[1]):
		data = raw_data[:, i]
		# data = raw_data[:, i]
		# # data = data[1:] - data[:-1] # difference
		# # print(data[:10], data[-10:])
		# data = data[start: end]
		flg = 'fft'
		if flg == 'fft':
			fft_features = _get_fft(data, fft_bin=m)
		# fft_features = fft_features[0:1 + int(np.ceil((m - 1) / 2))]
		elif flg == 'std':
			fft_features = [np.mean(data), np.std(data)]
			# fft_features = list(np.quantile(data, q=[0, 0.25, 0.5, 0.75, 1]))
			# fft_features = list(np.quantile(data, q = [0, 0.25, 0.5, 0.75, 1])) + [np.mean(data), np.std(data)]
			fft_features = list(np.quantile(data, q=[v * 0.01 for v in range(0, 100, 5)])) + [np.mean(data),
			                                                                                  np.std(data), skew(data),
			                                                                                  kurtosis(data),
			                                                                                  np.min(data),
			                                                                                  np.max(data)]
		elif flg == 'skew':
			# fft_features = [np.min(data), np.max(data)]
			# fft_features = [np.mean(data), np.std(data)]
			# fft_features = [skew(data)]
			# fft_features = [np.std(data)]
			# fft_features = [np.min(data), np.mean(data), np.std(data),  np.max(data)]
			fft_features = [np.mean(data), np.std(data), skew(data), kurtosis(data), np.min(data), np.max(data)]
		elif flg == 'hand_direction':
			fft_features = [np.max(data) - np.min(data), np.mean(data), np.std(data)]
		elif flg == 'top10':
			fft_features = sorted(data, reverse=True)[:50]
		# fft_features = sorted(data, key=lambda x:abs(x), reverse=True)[:50]
		else:
			n = len(data)
			step = int(np.ceil(n / m))
			fft_features = []
			for i in range(0, len(data), step):
				vs = data[i:i + step]
				flg2 = 'stats'
				if flg2 == 'stats':
					# tmp = list(np.quantile(vs, q = [0, 0.5, 1] )) # [0, 0.25, 0.5, 0.75, 1]+ [np.mean(vs), np.std(vs)]
					# tmp = list(np.quantile(vs, q=[0, 0.5, 1]))
					tmp = [np.mean(data), np.std(data), skew(data), kurtosis(data), np.min(data), np.max(data)]
					# tmp = [np.mean(vs)]
					n_feat = len(tmp)
				elif flg2:
					tmp = _get_fft(vs)
					tmp = sorted(tmp[0:1 + int(np.ceil((m - 1) / 2))], reverse=True)
					n_feat = 2
				fft_features.extend(tmp[:n_feat])
			fft_features = fft_features + [0] * (n_feat * m - len(fft_features))
		res.append(fft_features)
	return np.asarray(res).reshape(-1, )
