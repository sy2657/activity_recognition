# combine into this function
def best_100_frame_seg(grey_frames):
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

    """if ind==14:
      print("where diff is ", where_diff)
      print("len of where diff is", len(where_diff[0]))"""
    

    """coords = []
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
    frame_coords_y[ind] = coords_y"""

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

    if len_coords> 10: # nonzero change
      return(frame_no)
