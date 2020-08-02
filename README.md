# Detecting Free Parking Spots Through a R-CNN

## Table of Contents
1. [ Introduction ](#Intro)
2. [ Data ](#Data)
3. [ Trace the Parking Spots ](#spots)
4. [ Identify the cars ](#id)
5. [ Find Free Spots ](#Empty)
6. [ Test on the Video  ](#Test)

<a name="Intro"></a>
## Introduction
Finding a parking space in a crowded lot can be a really tough and irritating challenge. 
It is of both the owner of the parking lot and the visitors interest to streamline the process of finding free parking spots. 
However, many of the solutions requires a lot of eqiupment, such as sensors on each parking space. But what if one solution only requires a simple camera and some machine learning? 

This is the aim - to identify free parking spots through a videoclip. For this project to be concidered a success, it needs to identify the vast majority right and fairly quick.

<a name="Data"></a>
## Data
The data used is a 15 seconds long clip from the website Videezy. Link to video: https://www.videezy.com/abstract/39640-parking-lot-movement. The video shows a parking lot where the time is speed up. The camera does not move and is focused on place. This is important if one would like to use the same techniques as in this project and the reason why will be explained in the next chapter. To get an idea of how the video looks, here is the first frame

![pic1](https://user-images.githubusercontent.com/62875997/89126075-2a443800-d4e3-11ea-8e80-2eea6c87219d.jpg)

As one can see, there are a lot of parking spots, 54 to be exact, but only a few free. This seems to be a perfect video for this project!

<a name="spots"></a>
## Detect parking spots
There are a lot of ways to trace the parking spots. For example, one could create a Region-based Convolutional Neural Networks(R-CNN) that can identify parking spots. However, the white lines of a parking spot are often hardly visible. The techniques we will use is to fix the coordinates of the parking spots by a program called YOLO(You Only Look Once). This program let's you paint the areas of interest on a picture and thereafter give you the coordinates. Here is an example of the program in use

![Skärmklipp 2020-08-02 20 19 49](https://user-images.githubusercontent.com/62875997/89129415-95026d00-d4fd-11ea-9ab4-0222b88abbb8.png)

Now I can just click on save an the YOLO annotation toll will svave a file with the corresponding coordinates that I have marked out. These coordinates will be fixed and used during the whole video. This is the reason for needing the camera to be still. 

<a name="id"></a>
## Identify the cars
To identify the cars a I will use the Mask-RCNN. Simply put, it is a convolutional neural network trained on several datasets, like the COCO dataset, with countless of pictures and videos to identify several objects. Mask-RCNN is built on the top of the Faster-RCNN object detection model. Let's try to use the neural network on the first frame to see if how well it points out the cars. 

![Testing](https://user-images.githubusercontent.com/62875997/89129723-d005a000-d4ff-11ea-9475-f1cacc36676c.png)

Wow, I did not expect it to be this good! All cars were identified. The only flaw is that the model finds trucks that are not in the picture. But for now, it is good enough. 

<a name="Empty"></a>
## Find Free Spots
Now that we can trace the parking spots and the cars, we can find the occupied- and thus also the free parking spots. For this problem, the Intersection over Union will be used.
Intersection over Union is (IoU) an evaluation metric. As you can guess from it's name, it is the ratio of the area of overlap and the area of intersection. Calculating IoU will be done by using a function from MRCNN utils named compute_overlaps, where a threshold of .15 will determined whether a spot is free or not. Is the IoU over .15 - then it is seen as occupied.

<a name="Test"></a>
## Test on the Video 
To test the video, everything we gone through will be used. In total there is X steps:

1: A frame is saved as a picture. 

2: The model tries to identify all the cars on the frame.

3. The IoU is calculated, and the parking spots that are under .15 are painted green whilst the others are painted red.

4. Save pic and repeat step 1-4. Until all frames are painted and saved.

5. Compile all the pics into one video.

Doing this led to the following video(That i made to a GIF, to see full video - Click here):

![ezgif com-gif-maker](https://user-images.githubusercontent.com/62875997/89130464-5a9cce00-d505-11ea-9bcd-2fa19e2cd285.gif)




