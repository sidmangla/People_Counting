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
* Trigger - The class that refers to Person detection. Out here we have used the class _**'Person'**_ trained with full body annotations of person. _**In a vertical setting**_ we can train with images of a person's head as a lot of occlusion  will be there when people are lined up in a vertical setting or moving along y-axis.
* Trigger Confidence - The confidence of trigger class. This the user has to define after testing the model on certain scenarios and choose the best confidence to avoid false positives.
* Security Trigger - The class that triggers the security check. We have trained for class _**'Metal_Detector'**_. In some cases, this class could be _**'Security Guard'**_. Depends on the view and scenario.
* Security Trigger Confidence - The confidence of the security trigger class.

**Partitions** - we have divided our space into five phases.
  * Orientation - _"horizontal"_ - x-axis or _"vertical"_ - y-axis, Default is *__horizontal__*
  * First Phase - [270, 540]
  * Second Phase - [540, 810]
  * Third Phase - [810, 1070]
  * Entry Point - 1070
  * Exit Point - 270

Here is the Partition image

![Partition image](https://github.com/sidmangla/People_Counting/blob/main/partition.jpg)

We track the person from the first phase to the third phase moving in, when a person crosses the Entry Point the person has entered the facility. similarly, we track the person from the third phase to the first phase moving out, when a person crosses the exit point he has exited the place.

### Security Check
We also have security check functionality. The security check happens in the second phase. when a person has entered the second phase moving in. We check for the vicinity of the security trigger class -_**'Metal_Detector'**_ near the trigger class- _**'Person'**_ in the second phase. We annotate the *__'Security_Guard'__* to differentiate between the People in line and people checking. so that the model does not pick the guard checking as the person in the line. if the Metal detector is in the vicinity of the Person. This vicinity can be user-defined.

+ **Diff_pixel** - One of the most important parameter as it differentiates between the same or different person. so when we detect a person on the scene we get its coordinate on the image. when we process the next frame. we find the absolute difference between the coordinates of the persons detected in the previous frame and the coordinates of the persons detected in the current frame. If this difference is above/ more the _**Diff_pixel**_ then it is a different person. otherwise, the same person has moved a bit in the next frame.
+ **sec_trig_xlimit** - The x-axis limit of the vicinity area.
+ **sec_trig_ylimit** - The y-axis limit of the vicinity area.

From the Object detection model, we get the bounding box (its coordinates actually). We calculate the center point of the bounding box as a reference for that object. In the image below in _**Red**_ we show the center of the Person bounding box and in _**Blue**_ we have the midpoint of the Metal Detector bounding box. The _**Green**_ boxes are the vicinity area if have vicinity x-limit and y-limit value of 50. In that case, the metal detector will not be in the vicinity of the Person. As shown in the image the inner green rectangle does not include the Person midpoint. Therefore we need to keep in mind these things before setting the parameters for security check.
  
![Security check image](https://github.com/sidmangla/People_Counting/blob/main/sec.jpg)

**Other Important parameters**

* security_check - we have this parameter to opt out of the security functionality. Therefore this can be just used to count people entering and exiting a facility.
* draw - Write the Stats on the image and  return it.
* print_coord - For testing purposes when we need to define the parameters we can use this for testing multiple use cases and debugging

