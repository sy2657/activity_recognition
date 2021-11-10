# get data moment version , oct 3
def get_moment_data(root_dir='data-clean', camera_type='_1.mp4', classes=[]):
    dataset=[]
    users=[]
    activities=[]
    raw_files=[]
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
                    #data.extend(list(raw_mom))
                    data.append(raw_mom)
            data= np.asarray(data)
            dataset.append(data)
            users.append(user)
            activities.append(classes.index(act))
            raw_files.append(file)
    return np.array(dataset), np.array(users), np.array(activities), raw_files
