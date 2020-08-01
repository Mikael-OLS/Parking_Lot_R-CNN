def pics_to_vid(pathIn,pathout):
    # The function assumes that the pics are names new1.jpg, new2.jpg and so on
    fps = 24
    frame_array = []
    files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
    files.sort()
    files.sort(key = lambda x: int(x.replace('new','').replace('.jpg',"")))
    for i in range(len(files)):
        filename=pathIn + "/" +  files[i]
        #reading each files
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        
        #inserting the frames into an image array
        frame_array.append(img)
    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    out.release()
