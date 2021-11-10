# get data, get data ang (angle), get data hands, get fft 

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
			for keypoint_idx, _ in enumerate(keypoints):
				tmp = get_fft_features(raw_data, keypoint=keypoint_idx)
				#print("tmp shape is ", np.shape(tmp))
				data.extend(list(tmp))
			data = np.asarray(data)
			print("data shape is ", np.shape(data))
			dataset.append(data)
			users.append(user)
			activities.append(classes.index(act))
			raw_files.append(file)
		print(act, len(files))

	return np.array(dataset), np.array(users), np.array(activities), raw_files

def _get_data(root_dir='', camera_type='_1.mp4', classes=[], m=10):
	dataset = []
	users = []
	activities = []
	raw_files = []
	duration = []
	for act in classes:
		files = glob.glob(f'{root_dir}/refrigerator/' + act + f'/*/*{camera_type}.npy')
		#files = glob.glob(f'{root_dir}/data-clean/refrigerator/' + act + f'/*/*{camera_type}.npy')
		for file in files:
			# print('Processing file', file)
			user = int(file.split('/')[-2])

			data = []
			raw_data = np.load(file)
			duration.append(len(raw_data))
			if camera_type == '_1.mp4':
				fps = 10
				min_frames = 286  # number of frames
				max_frames = 477  # number of frames
				if raw_data.shape[0] < min_frames or raw_data.shape[0] > max_frames:
					print(len(raw_data), file)
					continue
			elif camera_type == '_2.mkv':  # fps = 30
				fps = 30
				min_frames = 466  # number of frames
				max_frames = 708  # number of frames
				if raw_data.shape[0] < min_frames or raw_data.shape[0] > max_frames:
					print(len(raw_data), file)
					continue
			elif camera_type == '_3.mp4':  # fps = 3
				min_frames = 76  # number of frames
				max_frames = 95  # number of frames
				if raw_data.shape[0] < min_frames or raw_data.shape[0] > max_frames:
					print(len(raw_data), file)
					continue

			data = get_fft_features(raw_data, m=m, file=file)
			data = np.asarray(data)

			dataset.append(data)
			users.append(user)
			activities.append(classes.index(act))
			raw_files.append(file)
		#print(act, len(files))
	#print(f'***{camera_type}, n_frames: {np.quantile(duration, q=[0, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 1])}\n')

	return np.array(dataset), np.array(users), np.array(activities), raw_files

def _get_data_ang(root_dir='data-clean', camera_type='_1.mp4', classes=[]):
	dataset = []
	users = []
	activities = []
	raw_files = []
	for act in classes:
		files = glob.glob(f'{root_dir}/refrigerator/' + act + f'/*/*{camera_type}.npy')
		for file in files:
			#print('Processing file', file)
			user = int(file.split('/')[-2])

			data = []
			raw_data = np.load(file)
            # change to specific keypts
			keypts = [13, 16] # left wrist, right wrist, [5,6,7,8,9,10]
			#for keypoint_idx in keypts:
			tmp = get_ang_features(raw_data) #, keypoint=keypoint_idx)
			data.extend(list(tmp))
			data = np.asarray(data)
			print("data shape is ", np.shape(data))
			dataset.append(data)
			users.append(user)
			activities.append(classes.index(act))
			raw_files.append(file)
		print(act, len(files))
	return np.array(dataset), np.array(users), np.array(activities), raw_files

def _get_data_hands(root_dir='data-clean', camera_type='_1.mp4', classes=[]):
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
            # change to specific keypts
			keypts = [13, 16] # left wrist, right wrist, [5,6,7,8,9,10]
			#for keypoint_idx in keypts:
			tmp = get_hand_features(raw_data) #, keypoint=keypoint_idx)
			data.extend(list(tmp))
			"""for keypoint_idx, _ in enumerate(keypoints):
				tmp = get_fft_features(raw_data, keypoint=keypoint_idx)
				#print("tmp shape is ", np.shape(tmp))
				data.extend(list(tmp))"""
			data = np.asarray(data)
			print("data shape is ", np.shape(data))
			dataset.append(data)
			users.append(user)
			activities.append(classes.index(act))
			raw_files.append(file)
		print(act, len(files))

	return np.array(dataset), np.array(users), np.array(activities), raw_files

def _get_fft(vs, fft_bin=None, fft_type='magnitude'):
	out = np.fft.fft(vs, n=fft_bin)
	if fft_type == 'phase':
		out = np.angle(out)  # phase
	else:
		# fft_type =='magnitude':
		out = np.abs(out)
	return list(out)

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
            # change to specific keypts
			keypts = [13, 16] # left wrist, right wrist, [5,6,7,8,9,10]
			for keypoint_idx in keypts:
				tmp = get_fft_features(raw_data, keypoint=keypoint_idx)
				data.extend(list(tmp))
			"""for keypoint_idx, _ in enumerate(keypoints):
				tmp = get_fft_features(raw_data, keypoint=keypoint_idx)
				#print("tmp shape is ", np.shape(tmp))
				data.extend(list(tmp))"""
			data = np.asarray(data)
			print("data shape is ", np.shape(data))
			dataset.append(data)
			users.append(user)
			activities.append(classes.index(act))
			raw_files.append(file)
		print(act, len(files))

	return np.array(dataset), np.array(users), np.array(activities), raw_files
