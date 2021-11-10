def get_data_orig(root_dir, cameras=[], classes=[]):
	history = {}
	for i, camera in enumerate(cameras): # _get_data 
		dataset, users, activities, raw_files = _get_data_ang(root_dir, camera_type=camera, classes=classes)
		#dataset, users, activities, raw_files = get_moment_data(root_dir, camera_type=camera, classes=classes)
		history[camera] = (dataset, users, activities, raw_files)
	print("history shape is ", np.shape(history))
	return history

def get_data_hands(root_dir, cameras=[], classes=[]):
	history = {}
	for i, camera in enumerate(cameras):
		dataset, users, activities, raw_files = _get_data_hands(root_dir, camera_type=camera, classes=classes)
		#dataset, users, activities, raw_files = get_moment_data(root_dir, camera_type=camera, classes=classes)
		history[camera] = (dataset, users, activities, raw_files)

	return history

def get_data(root_dir, cameras=[], classes=[]):
	history = {}
	for i, camera in enumerate(cameras):
		#dataset, users, activities, raw_files = _get_data(root_dir, camera_type=camera, classes=classes)
		dataset, users, activities, raw_files = get_moment_data(root_dir, camera_type=camera, classes=classes)
		history[camera] = (dataset, users, activities, raw_files)

	return history

# get data moment version , oct 3
def get_moment_data(root_dir='data-clean', camera_type='_1.mp4', classes=[]):
	dataset = []
	users = []
	activities = []
	raw_files = []
	for act in classes:
		files = glob.glob(f'{root_dir}/refrigerator/' + act + f'/*/*{camera_type}.npy')
		for file in files:
			user = int(file.split('/')[-2])
			data = []
			raw_data = np.load(file)
			for keypoint_idx, _ in enumerate(keypoints):
                for coordinate in range(3):
                    raw_col = raw_data[:, keypoint_idx, coordinate]
                    raw_mom = moment(raw_col, moment=3)
                    data.extend(list(raw_mom))
			data = np.asarray(data)

			dataset.append(data)
			users.append(user)
			activities.append(classes.index(act))
			raw_files.append(file)
	return np.array(dataset), np.array(users), np.array(activities), raw_files

def get_data_wavelet(root_dir, cameras=[], classes=[]):
	history = {}
	for i, camera in enumerate(cameras):
		#dataset, users, activities, raw_files = _get_data(root_dir, camera_type=camera, classes=classes)
		dataset, users, activities, raw_files = get_wavelet_data(root_dir, camera_type=camera, classes=classes)
		history[camera] = (dataset, users, activities, raw_files)
	return history

def get_data_orig(root_dir, cameras=[], classes=[]):
	history = {}
	for i, camera in enumerate(cameras):
		dataset, users, activities, raw_files = _get_data(root_dir, camera_type=camera, classes=classes)
		#dataset, users, activities, raw_files = get_moment_data(root_dir, camera_type=camera, classes=classes)
		history[camera] = (dataset, users, activities, raw_files)

	return history
