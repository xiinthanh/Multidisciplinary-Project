# Multidisciplinary-Project

## 1. General Info
Group Name: Discrete Group

App: A system to manage the door of a shop during COVID pandemic
  - Open the door when:
    + A Customer wears a mask and has normal temperature.
    + A correct password is entered.
  - Close the door otherwise.

Technology used:
  - AI: whether there is a person at the door, if yes whether that person wears a mask or not.
  - IoT service (Adafruit).
  - Simple hardware (Arduino) is used to get body temperature.
  - Data Analytics (Calculate average body temperature).
  - Extra feature: open the door by password.

## 2. System Deployment
**Step 1:** Clone the source code

**Step 2:** Install the following Python packages
  - For AI:
    + tensorflow
    + keras
    + numpy
    + Pillow
    + opencv-python
  - For IoT Server:
    + adafruit-io
  - For Arduino:
    + pyserial

**Step 3:** Set up the feeds and dashboard on Adafruit as below (can be modified depending on preference). Then change the AIO_USERNAME and AIO_KEY accordingly.

Feeds

<img width="790" alt="Feeds" src="https://github.com/xiinthanh/Multidisciplinary-Project/assets/118944173/2e06be94-92f4-4ca2-b785-45f986748e41">

Dashboard

<img width="790" alt="Dashboard" src="https://github.com/xiinthanh/Multidisciplinary-Project/assets/118944173/16781d74-c346-4d86-b355-e133803786e5">

**Step 4:** Plug-in the Arduino and change the port ("COMx").
<img width="600" alt="Arduino Port" src="https://github.com/xiinthanh/Multidisciplinary-Project/assets/118944173/e4f64fb0-4545-41c6-9007-3ce0002a67a1">

**Step 5:** Run the "mqtt.py" file

**Extra 1:** You can change the camera for AI detecting (the sample code using webcam).
<img width="600" alt="image" src="https://github.com/xiinthanh/Multidisciplinary-Project/assets/118944173/fcec2503-3d7a-4e98-9e99-ce5a714c89ea">

**Extra 2:** Password can be changed here:

<img width="300" alt="image" src="https://github.com/xiinthanh/Multidisciplinary-Project/assets/118944173/7126962a-de46-406a-b071-bcde4098d608">

