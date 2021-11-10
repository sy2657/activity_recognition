# oct 31 
# angle feats, and combinations of them
def get_ang_features(raw_data='', m=84, keypoint=7, file=''):
    x, y = 0, 3
    head = raw_data[:, 10, x:y]
    left_shoulder = raw_data[:, 11, x:y]
    right_shoulder = raw_data[:, 14, x:y]
    left_elbow = raw_data[:, 12, x:y]
    right_elbow = raw_data[:, 15, x:y]
    left_wrist = raw_data[:, 13, x:y]
    right_wrist = raw_data[:, 16, x:y]
    
    # test by printing one
    #print("left shoulder is", left_shoulder)
    #print("shape is ", np.shape(left_shoulder))
    
    # data angles between two different keypts
    
    # left shoulder and left elbow
    # 3 different landmarks : head, left shoulder, left elbow; left shoulder, left elbow, left wrist
    
    nrows = np.shape(raw_data)[0]
    angles=[]
    for i in range(nrows):
        # calc angles
        #  math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        # left shoulder, left elbow, left wrist
        x1 = left_shoulder[i][0]
        y1 = left_shoulder[i][1]
        
        x2 = left_elbow[i][0]
        y2 = left_elbow[i][1]
        
        x3= left_wrist[i][0]
        y3= left_wrist[i][1]
        
        angle= math.degrees(math.atan2(y3-y2, x3-x2) - math.atan2(y1-y2, x1-x2))
        angles.append(angle)
        # right shoulder, right elbow, right wrist
    
    # process stats of data
    data = angles
    n = len(data)
    m=10
    step = int(np.ceil(n / m))
    features = []
    for i in range(0, len(data), step):
        vs = data[i:i + step]
        temp = [np.mean(vs), np.std(vs), skew(vs), kurtosis(vs), np.min(vs), np.max(vs)]
        features.extend(temp)
    res = []
    res.append(features)
    return np.asarray(res).reshape(-1, )
    #return angles # left_shoulder
