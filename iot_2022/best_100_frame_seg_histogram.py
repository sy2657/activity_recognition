# improved best 100 frame segment code with histogram 
# make sure scipy v. 1.5 is installed, !pip install scipy==1.5

bin_orig_map = {}
ind=0

for i in range(66): # 1280 total
  for j in range(38): # 720 total
    bin_orig_map[(i,j)] = ind

    ind = ind+1

from scipy import stats

binx = 20*np.arange(65)
biny = 20*np.arange(37)

def best_100_frame_seg_histogram(grey_frames, bin_orig_map):
  # step 1 
  ind = 0

  thres = 150

  frame_coords = {}

  frame_coords_x = {}
  frame_coords_y = {}

  number_diffs = {}

  firstFrame = grey_frames[0]

  for frame in grey_frames:

    if ind==0:
      prev_frame = frame
      ind = ind+1
      continue

    diff = prev_frame - frame
    diff_abs = abs(diff)

    #cv2_imshow(diff_abs)

    frame_delta = cv2.absdiff(firstFrame, frame)

    #if 10 <ind < 16:
      #cv2_imshow(frame_delta)

    # boolean greater than threshold
    boolean_diff = frame_delta > thres #diff_abs > thres

    where_diff = np.where(boolean_diff)

    number_diffs[ind] = len(where_diff[0])

    

    coords = []
    coords_x = []
    coords_y= []
    for (x, y) in zip(where_diff[0], where_diff[1]):
        #print((x, y))
        coords_x.append(x)
        coords_y.append(y)
        coords.append((x,y))

        # compare distance with average?


    # analyze coordinates
    frame_coords[ind] = coords
    frame_coords_x[ind] = coords_x
    frame_coords_y[ind] = coords_y

    ind = ind+1
    prev_frame=frame

  # step 2  
  video_len = len(grey_frames)
  for frame_no in range(1, video_len):
    #coords = frame_coords[frame_no] # choose a frame # 
    #coords_x = frame_coords_x[frame_no]
    #coords_y = frame_coords_y[frame_no]
    len_coords = number_diffs[frame_no]

    # without bin histogram method

    """if len(coords_x) >  10: # nonzero change
      # starting frame return
      return(frame_no)"""

    if len_coords> 10: # nonzero change ; len_coords is how many 
      print(len_coords)
      # change the procedure to determine if the frame is right
      coords_x = frame_coords_x[frame_no]
      coords_y = frame_coords_y[frame_no]
      
      # try return
      #print("shape of coords x is ", np.shape(coords_x))

      #binx = 20*np.arange(65)
      #biny = 20*np.arange(37)
      sb = stats.binned_statistic_2d(coords_x, coords_y, None, 'count', bins=[binx, biny], expand_binnumbers=True)
      bin_arrs = sb[3]

      bin_x = bin_arrs[0]
      bin_y = bin_arrs[1]

      bin_histogram = {}

      for ind in range(len(bin_x)):
        pair = (bin_x[ind], bin_y[ind])
        #print("pair is ", pair)
        orig_index = bin_orig_map[pair]
        if bin_histogram.get(orig_index) ==None:
          bin_histogram[orig_index]=1
        else:
          bin_histogram[orig_index]= bin_histogram[orig_index]+1
      # if the counts within bin_histogram are greater than 100
      tot_v_count =0
      for k in bin_histogram:
        v = bin_histogram[k]
        
        if v > 100:
          #print(v)
          tot_v_count = tot_v_count+1 

      if tot_v_count > 3:
        return(frame_no)
