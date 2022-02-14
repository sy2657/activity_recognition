# from above, combine steps 1 and 2 

# improved best 100 frame segment code with histogram 
# make sure scipy v. 1.5 is installed, !pip install scipy==1.5
def best_100_frame_seg_histogram_combined(grey_frames):
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

    #number_diffs[ind] = len(where_diff[0])

    

    coords = []
    coords_x = []
    coords_y= []
    for (x, y) in zip(where_diff[0], where_diff[1]):
        #print((x, y))
        coords_x.append(x)
        coords_y.append(y)
        coords.append((x,y))

        # compare distance with average?

    # direct analysis here 
    len_coords = len(where_diff[0])
    if len_coords> 10:
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

      if tot_v_count > 2:
        print("frame number returned is:", ind)
        return(ind)


    # analyze coordinates
    #frame_coords[ind] = coords
    #frame_coords_x[ind] = coords_x
    #frame_coords_y[ind] = coords_y

    ind = ind+1
    prev_frame=frame

  print("frame number returned is 0")
  return(0) # return if none found
