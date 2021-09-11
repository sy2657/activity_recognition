# sept 8 input is activity and persons

persons = [1,2,3,4,5] #[2,3,4,5,7]


x_tot= {}
y_tot= {}
z_tot= {}

x_std = {}
y_std={}
z_std={}

#maxs =[]
smax_t = 500

# same as above but save matrices after knowing the max # rows/frames
for p in persons:
    # make map of matrix results
    matmap = {}
    
    rootdir = rootdir4+"/"+str(p)

    nfiles= 0
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            npath = os.path.join(subdir, file)
            
            
            if file.endswith(("1.mp4.npy")):
                print(npath)
                nfiles=nfiles+1
                
                trimmed_res = trim(npath)
                # shape
                s0 = np.shape(trimmed_res)[0]
                
                if s0 > smax_t:
                    trimmed_res = trimmed_res[:smax_t]
                
                if s0 < smax_t:
                    z51 = np.zeros(51)
                    # append NA or -inf

                    minus = smax_t - s0
                    for i in range(minus):
                        trimmed_res= np.vstack((trimmed_res,z51))
                    
                
                matmap[nfiles] = trimmed_res
    
    xseries_tot =[]
    yseries_tot =[]
    zseries_tot =[]
    
    numvideos = nfiles

    for i in range(1, numvideos): #numvideos):

        video_mat = matmap[i]

        xseries=[]
        yseries=[]
        zseries =[]
        for row in video_mat:
        # use indices to locate keypt x,y,z 
            rowx= row[kypt_loc]
            rowy= row[kypt_y]
            rowz= row[kypt_z]
            xseries.append(rowx)
            yseries.append(rowy)
            zseries.append(rowz)

        # take average

        #print("xseries prev", xseries_tot)
        #print("xseries curr", xseries )
        
        xseries_tot.append(xseries)
        yseries_tot.append(yseries)
        zseries_tot.append(zseries)

    
    """samp_data_x = np.array(xseries_tot)
    xaved = np.average(samp_data_x, axis=0)
    
    stdx = np.std(samp_data_x, axis=0)
    
    samp_data_y = np.array(yseries_tot)
    yaved = np.average(samp_data_y, axis=0)
    
    stdy = np.std(samp_data_y, axis=0)
    
    samp_data_z = np.array(zseries_tot)
    zaved = np.average(samp_data_z, axis=0)
    
    stdz = np.std(samp_data_z, axis=0)"""

    x_tot[p] = xseries_tot
    y_tot[p] = yseries_tot
    z_tot[p] = zseries_tot
    
    """x_std[p] = stdx
    y_std[p] = stdy
    z_std[p] = stdz"""
        
                
