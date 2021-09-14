# sept 11: average over all persons
# set max frame # to 1000


persons = [2,3,4,5,7, 8,9] # [1,2]


x_tot= {}
y_tot= {}
z_tot= {}

x_std = {}
y_std={}
z_std={}

x_person_to_ave = []
y_person_to_ave = []
z_person_to_ave = []

x_std_all =[]
y_std_all =[]
z_std_all =[]

smax_t = 1000   
# same as above but save matrices after knowing the max # rows/frames
for p in persons:
    # make map of matrix results
    matmap = {}
    
    rootdir = rootdir3+"/"+str(p)

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
                
                sh = np.shape(trimmed_res)
                print("shape is", sh)
                
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

        """if i==1:
            xseries_tot = xseries
            yseries_tot = yseries
            zseries_tot = zseries
            continue"""

        # take average

        #print("xseries prev", xseries_tot)
        #print("xseries curr", xseries )
        
        xseries_tot.append(xseries)
        yseries_tot.append(yseries)
        zseries_tot.append(zseries)
    
    samp_data_x = np.array(xseries_tot)
    xaved = np.average(samp_data_x, axis=0)
    
    stdx = np.std(samp_data_x, axis=0)
    
    samp_data_y = np.array(yseries_tot)
    yaved = np.average(samp_data_y, axis=0)
    
    stdy = np.std(samp_data_y, axis=0)
    
    samp_data_z = np.array(zseries_tot)
    zaved = np.average(samp_data_z, axis=0)
    
    stdz = np.std(samp_data_z, axis=0)

    x_tot[p] = xaved
    y_tot[p] = yaved
    z_tot[p] = zaved
    
    x_std[p] = stdx
    y_std[p] = stdy
    z_std[p] = stdz
    
    x_person_to_ave.append(xaved)
    y_person_to_ave.append(yaved)
    z_person_to_ave.append(zaved)
    
    x_std_all.append(stdx)
    y_std_all.append(stdy)
    z_std_all.append(stdz)


# average over all persons
x_to_ave_samp = np.array(x_person_to_ave)
y_to_ave_samp = np.array(y_person_to_ave)
z_to_ave_samp = np.array(z_person_to_ave)

x_allperson_aved = np.average(x_to_ave_samp, axis=0)
y_allperson_aved = np.average(y_to_ave_samp, axis=0)
z_allperson_aved = np.average(z_to_ave_samp, axis=0)

x_to_ave_std = np.array(x_std_all)
y_to_ave_std = np.array(y_std_all)
z_to_ave_std = np.array(z_std_all)

x_std_aved =np.average(x_to_ave_std, axis=0)
y_std_aved=np.average(y_to_ave_std, axis=0)
z_std_aved=np.average(z_to_ave_std, axis=0)

std_x_aved = np.std(x_to_ave_samp, axis=0)
std_y_aved = np.std(y_to_ave_samp, axis=0)
std_z_aved = np.std(z_to_ave_samp, axis=0)

