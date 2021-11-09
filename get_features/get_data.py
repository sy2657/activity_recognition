def get_data_orig(root_dir, cameras=[], classes=[]):
	history = {}
	for i, camera in enumerate(cameras): # _get_data 
		dataset, users, activities, raw_files = _get_data_ang(root_dir, camera_type=camera, classes=classes)
		#dataset, users, activities, raw_files = get_moment_data(root_dir, camera_type=camera, classes=classes)
		history[camera] = (dataset, users, activities, raw_files)
	print("history shape is ", np.shape(history))
	return history
