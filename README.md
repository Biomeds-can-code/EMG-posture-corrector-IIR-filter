# EMG-posture-corrector-IIR-filter

This project has been designed by 4 Biomedical Engineering students at the University of Glasgow: Sofia Hernandez Gelado, Shamsa Al Harthy, Alistair Bachetti and Lucia Munoz Bohollo.

The purpose of this project was to apply an IIR filter design to solve a real-life issue. When studying, we spend long periods sitting on a chair and tend to use postures which might be harmful or cause back pain. Since the start of the COVID-19 pandemic this problem has only increased. Our team decided to produce a program which would notify the user if they were slouching, allowing them to know they have to correct their posture.


## Features

This program is made up by a series of files, using Python language. 

* 'realtime_iir_main.py': Is the main file of this program, and the one the user must run to check their posture. Obtains the information acquired through the Attys and using pyqtgraph package plots this information in realtime, allowing the user to observe changes in their EMG recording. Imports code from other files to analyse and plot the filtered signal in addition to the raw data.

* 'emg_analysis.py': This file contains the code to analyse the EMG signal and uses a threshold to detect changes in the signal. These changes in the signal correspond to changes in posture, which enables the program to determine when a correct sitting posture has been lost. In turn, this piece of code prints an alert on the Linux terminal or plays a sound to alert the user of correct or slouched posture.

* 'alert.py': Adds a visual notification to the user's screen to notify of whether they are sitting properly or slouching. 3 alert options are given (terminal text, visual pop-up window or auditory alert), it is recommended that the user picks their preferred option and comments out (#) the unwanted ones to prevent distractions. 

* 'iir_filter.py': Creates classes for a 2nd order IIR filter and an IIR filter, which enables multiple filter orders to be achieved through combination of these. A filter of order n=3 is used for this program, therefore it will combine one IIR filter and one 2nd order IIR filter.

* 'rununittest.py': Code to check the 2nd order IIR filter and chain of filters run as expected. This is a testing file and is not required for the program to work.


## Installing the program

This program has been designed to work under Linux.

To get started, you must clone the repository using:
git clone https://github.com/Biomeds-can-code/EMG-posture-corrector-IIR-filter.git 
and compile/install it.

Make sure the following Python packages are installed on your device:
```
pip3 install pyattyscomm
pip3 install pyqt5
pip3 install pyqtgraph
pip3 install scipy
pip3 install numpy
pip3 install matplotlib
```


## Data acquisition

To obtain the required EMG data needed for this program, it is suggested to have the following pieces of equipment:

![alt text](setup.png)

a) Elastic band with bipolar electrode montage. It is wrapped like a belt around the user's waist and hence close contact between the active electrodes and the subject's skin is ensured. Place them at the far right side of the trunk on the user's back.

b) One CE Certified Ag/AgCl electrode with solid gel placed on the subject's wrist bone. This location hence acts as an electric neutral for the whole circuit, due to the wrist bone's low electrical conductivity.

c) A standard lead cable, which connects the external electrode to the Ground (GND) port of the Attys device.

d) Attys DAQ. A portable data acquisition device, which transfers the recorded information to the computer via Bluetooth. This device connects to the elastic band with the help of cables to the positive and negative ports of Channel 1, and to the external electrode via the GND port.

e) ASUS-BT500 Dongle. This device strengthens and optimises Bluetooth connection between the Attys device and the computer.

The flow of information was carried out following the procedure outlined in the figure below:

<p align="center">
  <img src="https://github.com/Biomeds-can-code/EMG-posture-corrector-IIR-filter/blob/main/Flowchart.png" />
</p>


## Realtime demonstration

For a visual explanation of how the program works check the following link:
https://www.youtube.com/watch?v=qLxqRxfgYWU

And for a more thorough explanation of the project and how to place the equipment watch:
https://www.youtube.com/watch?v=cdfoDsuA3O0

