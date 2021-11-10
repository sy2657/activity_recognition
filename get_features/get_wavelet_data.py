# get data from wavelet , oct 5
def get_wavelet_data(root_dir='data-clean', camera_type='_1.mp4', classes=[]):
    dataset=[]
    users=[]
    activities=[]
    raw_files=[]
    smax = 500
    for act in classes:
        files = glob.glob(f'{root_dir}/refrigerator/' + act + f'/*/*{camera_type}.npy')
        for file in files:
            user = int(file.split('/')[-2])
            data = []
            raw_data = np.load(file)
            # trim the data
            trimmed_data= trim(file)
            s0 = np.shape(trimmed_data)[0]    
            
            if s0 >smax:
                trimmed_data= trimmed_data[:smax]
            else:
                z51 = np.zeros(51)
                # append NA or -inf

                minus = smax - s0
                for i in range(minus):
                    trimmed_data= np.vstack((trimmed_data,z51))
            
            # reshape trimmed data
            trim_reshape_data = trimmed_data.reshape(smax, 17,3)
                
            for keypoint_idx, _ in enumerate(keypoints):
                for coordinate in range(3):
                    raw_col = trim_reshape_data[:, keypoint_idx, coordinate]
                    #raw_mom = moment(raw_col, moment=3)
                    cA, cD = pywt.dwt(raw_col, wavelet='db2', mode='constant')
                    print("shape is ", np.shape(cA))
                    data.extend(list(cA))
                    #data.append(raw_mom)
            data=  np.asarray(data)
            dataset.append(data)
            users.append(user)
            activities.append(classes.index(act))
            raw_files.append(file)
    return np.array(dataset), np.array(users), np.array(activities), raw_files
