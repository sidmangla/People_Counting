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

**Classes and confidence**
* Trigger - The class that refers to Person detection. Out here we have used the class 'Person' trained with full body annotations of person. _**In a vertical setting**_ we can train with images of a person's head as a lot of occlusion  will be there when people are lined up in a vertical setting or moving along y-axis.
* Trigger Confidence - The confidence of trigger class. This the user has to define after testing the model on certain scenarios and choose the best confidence to avoid false positives.
* Security Trigger - The class that triggers the security check. We have trained for class 'Metal_Detector'. In some cases, this class could be 'Security Guard'. Depends on the view and scenario.
* Security Trigger Confidence - The confidence of the security trigger class.

**Partitions** - we have divided our space into five phases.
  * Orientation - "horizontal" - x-axis or "vertical" - y-axis, Default is *horizontal*
  * First Phase - [270, 540]
  * Second Phase - [540, 810]
  * Third Phase - [810, 1070]
  * Entry Point - 1070
  * Exit Point - 270

We track the person from the first phase to the third phase moving in, when a person crosses the Entry Point the person has entered the facility. similarly, we track the person from the third phase to the first phase moving out, when a person crosses the exit point he has exited the place.

### Security Check
We also have security check functionality. The security check happens in the second phase. when a person has entered the second phase moving in. We check for the vicinity of sec trigger class -'Metal_Detector' near the trigger class- 'Person' in the second phase. We annotate the Security Guard to differentiate between the People in line and people checking. so that the model does not pick the guard checking as the person in the line. if Metal detector is in the vicinity of the Person. 

   
Here is the Partition image
![Partition image](https://github.com/sidmangla/People_Counting/blob/main/sec.jpg)
