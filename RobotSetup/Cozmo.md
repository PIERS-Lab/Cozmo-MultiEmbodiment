#  Cozmo
- I higly recommend using linux for this, Ideally WSL if you are using windows, This guide will be going through the linux
 process, There are links to the SDK's documentation included if you want to try setting this up on a different system.
- Some useful links for the Cozmo SDK:
- [Documentation](https://web.archive.org/web/20220715081845/http://cozmosdk.anki.com/docs/)
- [Github](https://github.com/anki/cozmo-python-sdk)

## Enviornment
- Have a virtual enviornment setup with python 3.5.6, later versions have a deprecated async function
that the Cozmos use, so they won't work on newer python versions.

## SDK installation

You can find these instructions on the SDK's website on the internet archive, but considering that could 
go down any minute, I am compiling the linux steps here

### Linux

Install python 3.5 if you don't have it

```
sudo add-apt-repository ppa:deadsnakes
sudo apt-get update
sudo apt-get install python3.5 python3.5-tk 
```

Setup virtualenv (you can also use anaconda for this, but virtual env is easiest)
```
sudo apt-get install python-pip
pip install virtualenv
virtualenv -p python3.5 ~/cozmo-env
```
#### Imoprtant!
You will need to activate your enviornment every time you want to set up anything with the cozmos or run any programs

if you are using anaconda you can do 
```
conda activate [envName]
```

if you are using venev, you need to source the setup file
```
source ~/cozmo-env/bin/activate
```

finally install the SDK itself
```
pip install 'cozmo[camera]'
```

## Robot Setup
-  An unfortunate property that the cozmos have is that they need to be connected to another device to properly run
-  You can emulate a phone, but this can be slow and emulator quality varies (I recommend android studio if you intend to do this)
-  - For each device you need to download the cozmo app, luckily as of the time of writing this, it is avaliable on both
- IOS and android.
- once this is done, you can follow the in-app instructions to get a cozmo moving, and put it into SDK mode via the in-app settings to run programs
- Now, depending on the OS of the device that you'll be using with the Cozmo,
- you will need either [ADB](https://developer.android.com/tools/adb)(Android) or [usbmuxd](https://web.archive.org/web/20230324060005/https://github.com/libimobiledevice/usbmuxd)
### Android Debug Bridge
- Add The Platform Tools directory to your path (put his in your .bashrc file so it is automatically run)
```
export PATH=${PATH}:[Path to your insatllation]
```
- The install path will likely be wherever you downloaded the zip to/android-sdk-linux/platform-tools)
- you can verify that everything is good using this
```
which adb
```
### usbmuxd 
- The instructions for usbmuxd cover the setup needed there
## Running Programs 
- Once evertyhing is all squared off, run through the following to run programs
- connect to the cozmo with your secondary device and put it into SDK mode
- plug the secondary devices into the computer you'll use to run the programs vis USB
- Verify that the device connection is working if needed (if using adb, just run ``` adb devices ```).
- Then just run the program on the primary device and the robot will properly react. 





