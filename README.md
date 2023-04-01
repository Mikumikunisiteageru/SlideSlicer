# SlideSlicer

In this era of online lectures, the audience take screenshots to capture presented slides (Beamer, Microsoft PowerPoint, etc.) as notes. However, the frequent need for action may repeatedly distract the listeners from the continuous stream of contents.

This software named SlideSlicer is designed to save every slide page shown on the screen without manual supervision. It keeps monitoring the screen, recognizes the moments of paging down, and saves the screenshot for each page. 

Turn on SlideSlicer beforehand and enjoy the lectures with all your attention.

## Installation

For 64-bit Windows operating system, the software has been compiled and released as [an executable file](https://github.com/Mikumikunisiteageru/SlideSlicer/releases). The executable file is assumed to run instantly without installation.

For other environments, it is possible to obtain a single executable file by
```
pyinstaller -F -w SlideSlicer.py
```
with [Python 3](https://www.python.org/downloads/), [NumPy](https://pypi.org/project/numpy/), and [PyQt 5](https://pypi.org/project/PyQt5/) having been installed.

## Graphical user interface

The simple software has three buttons: Record (`=` or `@`), Help (`?`), and Exit (`x`).
- The Record Button starts or stops recording, where `@` means recording and `=` means waiting (not recording). 
- The Help Button opens the configuration file in the default plain text editor. 
- The Exit Button stops recording and closes the software.

When the recording mode is on, the software periodically observes the full screen. Not all observed screenshots are saved --- it does only if the current image is *significantly different* from the last saved one, which usually implies a new slide. Every time a picture is taken, the background color of its window becomes ![#39C5BB](https://via.placeholder.com/15/39C5BB/000000?text=+) pure blue-green, and then gradually turns transparent. 

## Technical details

The period of taking screenshots is controlled by `SCREENSHOT/everyxmillisecond` in the configuration file, with a default value of `2000` (unit: millisecond).

Two images are considered *significantly different* if the ratio of corresponding bits (say `b1` and `b2`, both in UInt8) with the following properties exceeds the value of `PAGEDETECTION/threshold` (default: `0.001`):
- The value of `PAGEDETECTION/threshold` (default: `128`) lies between `b1` and `b2`; 
- The difference between `b1` and `b2` exceeds the value of `PAGEDETECTION/rangesize` (default: `154`).

All the variables mentioned in this subsection can be modified in the configuration file (SlideSlicer_config.ini, automatically generated if absent). Besides, it is also possible to modify the directory for screenshot images at `OUTPUT/path`.

## Disclaimer

The software is released under the MIT License (see [LICENSE.md](https://github.com/Mikumikunisiteageru/SlideSlicer/blob/main/LICENSE.md) for more details). Any user may utilize the software free of charge. 

The author does not provide any warranty of any form and will not be liable for any possible consequence, including:
- Some slides may be not detected and therefore not saved;
- Same slides may be regarded different and therefore saved multiple times;
- Legally protected (e.g., copyright reserved) or irrelevant contents may be saved.

USE AT OWN RISK!
