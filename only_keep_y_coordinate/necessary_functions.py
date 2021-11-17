# nov 14 only save y coordinate
def get_y_features(raw_data='', m=84, keypoint=7):
    # use windows
    smax=200
    res = []
    flg='windows'
    flg2= 'all6'
    coordinate= 1
    #for coordinate in range(3):
    data = raw_data[:, keypoint, coordinate]
    data = data.reshape((-1,))
    if flg == 'windows':
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
 

# do not use all keypoints
def _get_data(root_dir='data-clean', camera_type='_1.mp4', classes=[]):
	dataset = []
	users = []
	activities = []
	raw_files = []
	for act in classes:
		files = glob.glob(f'{root_dir}/refrigerator/' + act + f'/*/*{camera_type}.npy')
		# files = [f'{root_dir}/data-clean/refrigerator/take_out_item/4/take_out_item_2_1616179391_1.mp4.npy',
		#          f'{root_dir}/data-clean/refrigerator/take_out_item/4/take_out_item_2_1616179391_1.mp4.npy']
		for file in files:
			# print('Processing file', file)
			user = int(file.split('/')[-2])

			data = []
			raw_data = np.load(file)
			for keypoint_idx, _ in enumerate(keypoints2): # do not use all the keypts
				#tmp = get_fft_features(raw_data, keypoint=keypoint_idx)
				tmp = get_y_features(raw_data, keypoint= keypoint_idx)
				data.extend(list(tmp))
			data = np.asarray(data)
			print("data shape is ", np.shape(data))
			dataset.append(data)
			users.append(user)
			activities.append(classes.index(act))
			raw_files.append(file)
		print(act, len(files))

	return np.array(dataset), np.array(users), np.array(activities), raw_files

def get_data(root_dir, cameras=[], classes=[]):
	history = {}
	for i, camera in enumerate(cameras):
		dataset, users, activities, raw_files = _get_data(root_dir, camera_type=camera, classes=classes)
		#dataset, users, activities, raw_files = get_moment_data(root_dir, camera_type=camera, classes=classes)
		history[camera] = (dataset, users, activities, raw_files)

	return history

# main 

cameras=['_1.mp4', '_2.mkv', '_3.mp4']
classes = ['no_interaction', 'open_close_fridge', 'put_back_item', 'take_out_item', 'screen_interaction']
label2idx = {v: i for i, v in enumerate(classes)}
idx2label = {i: v for i, v in enumerate(classes)}

keypoints2 = [13, 16] # left wrist, right wrist
