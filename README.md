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

when we train the model we define the input model resolution. The resolution at which the image is input to the model during training. By Default, Darknet Yolov4 uses 416 x 416 resolution. The coordinates we get from the _**Result**_ are according to the model resolution which is 512 x 512. Therefore we have to recalculate the coordinates according to the test image resolution.

**Partitions** - we have divided our space into five phases.
  * Orientation - "horizontal" - x-axis or "vertical" - y-axis, Default is *horizontal*
  * First Phase - [270, 540]
  * Second Phase - [540, 810]
  * Third Phase - [810, 1070]
  * Entry Point - 1070
  * Exit Point - 270
We track the person from the first phase to the third phase moving in, when a person crosses the Entry Point the person has entered the facility. similarly, we track the person from the third phase to the first phase moving out, when a person crosses the exit point he has exited the place.

We also have security check functionality. The security check happens in the second phase. when aperson has enteredthe second phase from first p

   
Here is the Partition image
![Partition image](https://github.com/sidmangla/People_Counting/blob/main/sec.jpg)
