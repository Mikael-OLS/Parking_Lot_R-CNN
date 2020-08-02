# Detecting Free Parking Spots Through a R-CNN

## Table of Contents
1. [ Introduction ](#Intro)
2. [ Data ](#Data)
3. [ Trace the Parking Spots ](#spots)
4. [ Identify cars ](#Legality)
 01.  [ Intersection ](#Variable)
 02.  [ Summary ](#Geographical)

<a name="Intro"></a>
## Introduction
Finding a parking space in a crowded lot can be a really tough and irritating challenge. 
It is of both the owner of the parking lot and the visitors interest to streamline the process of finding free parking spots. 
However, many of the solutions requires a lot of eqiupment, such as sensors on each parking space. But what if one solution only requires a simple camera and some machine learning? 

This is the aim of - to identify free parking spots through a videoclip. For this project to be concidered a success, it needs to identify the vast majority right and fairly quick.

<a name="Data"></a>
## Data
The data used is a 15 seconds long clip from the website Videezy. Link to video: https://www.videezy.com/abstract/39640-parking-lot-movement. The video shows a parking lot where the time is speed up. The camera does not move and is focused on place. This is important if one would like to use the same techniques as in this project and the reason why will be explained in the next chapter. To get an idea of how the video looks, here is the first frame

![pic1](https://user-images.githubusercontent.com/62875997/89126075-2a443800-d4e3-11ea-8e80-2eea6c87219d.jpg)

As one can see, there are a lot of parking spots, 54 to be exact, but only a few free. This seems to be a perfect video for this project!

<a name="spots"></a>
## Detect parking spots
There are a lot of ways to trace the parking spots. For example, one could create a Region-based Convolutional Neural Networks(R-CNN) that can identify parking spots. However, the white lines of a parking spot are often hardly visible. The techniques we will use is to fix the coordinates of the parking spots by a program called YOLO(You Only Look Once). This program let's you paint the areas of interest on a picture and thereafter give you the coordinates. Here is an example of the program in use.




