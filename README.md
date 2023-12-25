# Security Check and People Counting

First of all, we need to train a custom object detection model to Detect Person, Metal Detectors, Security guards.

**We use the result of the object detection model to give:**
+ Number of People Entering
+ Number of People Exiting
+ Number of People have gone through security check
+ number of people that were not checked
## Security Config JSON file
We have a lot of Parameters to define.

**Model Parameters** - we have used darknet yolov4 model
 * MetaPath - path to the meta or data file of the model
 * WeightPath - path to the model weights
 * ConfigPath - path to model config file
 * Model_height - 512
 * Model_weight - 512   
when we train the model we define the input model resolution. The resolution at which the image is input to the model. By Default, darknet yolov4 uses 416 x 416 resolution.

**Partitions** - we have divided our space into five phases.
  * Orientation - "horizontal" - x-axis or "vertical" - y-axis
  * First Phase - []
  * Second Phase - []
  * Third Phase - []
  * Entry Point - 
  * Exit Point -

   
Here is the Partition image
![Partition image](https://github.com/sidmangla/People_Counting/blob/main/sec.jpg)
