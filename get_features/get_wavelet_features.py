# wavelet function version

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
		flg = 'wavelet' #'stats', wavelet, std
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
		elif flg=='angle': # calculate angle btw keypts
			
			angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
			if angle<0:
				angle=angle+360
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
