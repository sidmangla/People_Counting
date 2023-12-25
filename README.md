# Security Check and People Counting

First of all, we need to train a custom object detection model to Detect Person, Metal Detectors, Security guards.

**We use the the result of the object detection model to give:**
+ Number of People Entering
+ Number of People Exiting
+ Number of People have gone through security check
+ number of people that were not checked
## Security Config Json file
We have a lot of Parameters to define.

**Model Parameters** - we have used darknet yolov4 model
 * MetaPath - path to the meta or data file of the model
 * WeightPath - path to the model weights
 * ConfigPath - path to model config file
   
Here is the Partition image
![Partition image](https://github.com/sidmangla/People_Counting/blob/main/sec.jpg)
