**README**

Welcome to the Touchless Interaction Suite: a multi-module collection of Python/Arduino projects that transform everyday webcams and a single gesture-sensor into powerful-computer-interaction (HCI) tools.  
This README acts as a single, authoritative reference for:

*   Complete installation instructions.
*   Hardware & software prerequisites.
*   Detailed explanations of each module’s purpose, architecture, and usage.
*   Troubleshooting tips and extensibility guidance.

**Overview**

The suite ships six independent Python applications (plus one Arduino sketch):

1.  Presentation Controller – slide navigation & on-screen annotation.
2.  Virtual Mouse – cursor control & click emulation.
3.  Volume/Scroll/Cursor Controller – tri-mode desktop control.
4.  Dino Game Controller – jump automation for the Chrome offline game.
5.  Hill Climb Racing Controller – accelerator/brake automation.
6.  3D Racing Game Controller – steering, throttle, & reverse.
7.  Arduino Gesture Sensor Driver – APDS-9960 gesture feed (optional).

Each program relies on real-time hand-landmark extraction by **MediaPipe Hands** and/or raw gesture decoding from the **APDS-9960** sensor. Output actions are injected via **pyautogui**, **autopy**, or Windows Core Audio (pycaw) where appropriate.

**Quick-Start Installation**

**1\. Python Environment**

| Item | Min Version | Tested On | Notes |
| --- | --- | --- | --- |
| Python | 3.8 | 3.8.18, 3.9.19 | autopy only ships wheels ≤3.8. For 3.9+, compile from source or use an alternative library[1][2]. |
| Pip | 23.0 | 24.0 | Upgrade: python -m pip install --upgrade pip |

⚠️ If you already run Python 3.9+ and wish to avoid Rust toolchain compilation, install a parallel 3.8 interpreter exclusively for this suite; point your IDE or virtualenv to that interpreter before proceeding[\[1\]](#fn1).

**2\. System Packages**

Windows users must install the **Visual C++ Build Tools** to satisfy pycaw prerequisites:

choco install visualcpp-build-tools # Windows 10/11 Chocolatey\[^14\]  

Linux (for pyautogui) additionally requires:

sudo apt-get install scrot python3-tk python3-dev # display capture & Tk bindings\[^20\]  

macOS users may need the **command-line developer tools** (xcode-select --install).

**3\. Python Dependencies**

Create and activate a new virtual environment, then install the libraries:

pip install opencv-python mediapipe cvzone # computer-vision core\[^11\]\[^2\]  
pip install pyautogui pygetwindow pyscreeze # GUI automation stack\[^20\]  
pip install pycaw comtypes psutil # audio control\[^14\]  
pip install autopy # low-level mouse control (≤3.8 wheels)\[^8\]  
pip install pyserial # serial communication (for Arduino)  

If pip install autopy fails, install Rust nightly 2019-10-05 and build from source[\[2\]](#fn2):

rustup default nightly-2019-10-05  
pip install setuptools-rust  
pip install autopy  

**4\. Hardware**

| Module | Mandatory Hardware | Optional |
| --- | --- | --- |
| All Python scripts | 720p USB/Webcam | — |
| Scroll/Volume Controller | Speakers/headphones (for feedback) | — |
| Arduino driver | Arduino Nano/Uno + APDS-9960 breakout | On-board LED for testing |

**Repository Structure**

.  
├─ Presentation/  
│ ├─ 01.png … # Slide images  
│ └─ presentation.py # Main script (#1)  
├─ virtual\_mouse.py # Module #2  
├─ handtrackingmodule.py  
├─ volume\_scroll.py # Module #3  
├─ dino\_game.py # Module #4  
├─ hill\_climb.py # Module #5  
├─ racing\_3d.py # Module #6  
├─ arduino\_apds.ino # Module #7  
└─ README.md # ← current file  

**1\. Presentation Controller**

**Purpose**

Navigate PowerPoint/Keynote/Google Slides and draw annotations in real time using finger gestures tracked by a webcam.

**Key Features**

| Gesture | Fingers Up Pattern | Action |
| --- | --- | --- |
| Slide ← | 1 (forefinger) | Previous slide |
| Slide → | 5th finger only | Next slide |
| Laser Pointer | Forefinger + middle | Show red dot |
| Draw Start | Forefinger only | Begin annotation stroke |
| Undo Stroke | Forefinger + middle + ring | Remove last stroke |

**Launch**

python presentation/presentation.py  

Press **Q** to exit.

**Configuration**

Edit the constants at the top of presentation.py:

*   folderPath: image directory.
*   gestureThreshold: vertical pixel threshold above which slide-nav gestures register.
*   delay: debounce frames between commands.

**2\. Virtual Mouse**

**Purpose**

Control the system cursor and perform clicks purely through hand pose.

**Gestures & Mapping**

| FingersUp State | Mode | Action Details |
| --- | --- | --- |
| Index=1, Middle=0 | Move | Map fingertip within reduced frameR (100 px margin) to screen; smoothing factor 7. |
| Index=1, Middle=1 | Click | Distance between tip-IDs 8 and 12 < 40 px triggers left-click. |

**Launch**

python virtual\_mouse.py  

Tune variables:  
frameR (dead-zone size), smoothening (cursor easing), camera index (cap = cv2.VideoCapture(x)).

**3\. Volume / Scroll / Cursor Controller**

**Purpose**

Cycle between three desktop-control modes via dynamic fingers-up patterns:

**Mode Selection**

| Pattern | Result |
| --- | --- |
| `` | Neutral (awaiting) |
| [^3] OR [^3][^3] | Scroll mode |
| [^3][^3] | Volume mode |
| [^3][^3][^3][^3][^3] | Cursor mode |

**Mode-Specific Mappings**

1.  **Scroll**
    *   Index up → scroll +300 units.
    *   Index+Middle up → scroll -300 units.
2.  **Volume**
    *   Thumb & index distance map 50 – 200 px to -63 dB … 0 dB range[\[3\]](#fn3).
    *   Thumb closed → click to unselect.
3.  **Cursor**
    *   Hand inside ROI (110×620 / 20×350) controls autopy mouse move.
    *   Thumb touch → left-click.

**Launch**

python volume\_scroll.py  

**Note**

Requires **pycaw** (Windows only). On Linux/macOS, comment out the AudioUtilities section to compile without sound control.

**4\. Dino Game Controller**

**Purpose**

Automate jumps in Chrome’s offline T-Rex game using gesture detection.

| Pattern Detected | Action | Screen Overlay |
| --- | --- | --- |
| `` | Simulate SPACE key via directkeys | Jumping label |
| [0,1,*,*,*] | No action | Not Jumping |

directkeys.py must expose PressKey/ReleaseKey and scancode for SPACE.

**Launch**

python dino\_game.py  

**5\. Hill Climb Racing Controller**

**Purpose**

Provide brake and accelerator activation based on total-fingers count.

| Total Fingers | Action |
| --- | --- |
| 0 | Brake (hold LEFT arrow) |
| 5 | Accelerate (hold RIGHT arrow) |

**Launch**

python hill\_climb.py  

Ensure directkeys values left\_pressed/right\_pressed match the game’s keybindings.

**6\. 3D Racing Game Controller**

**Purpose**

Full steering wheel emulation using the **wrist landmarks** of both hands.

| Condition | Keys Pressed | Comment |
| --- | --- | --- |
| Hands diverge left | A | Hard-left |
| Hands diverge right | D | Hard-right |
| Hands centered | W | Straight |
| Single-hand detected | S | Reverse/backing |

Vector math determines mid-point (xm, ym), radius 150 px virtual steering circle, and slope to classify direction.

**Launch**

python racing\_3d.py  

Requires keyinput utility (Windows) mapping press\_key/release\_key.

**7\. Arduino APDS-9960 Gesture Driver**

**Purpose**

Stream **UP/DOWN/LEFT/RIGHT** swipes over serial (9600 baud) to any host program.

#include <Arduino\_APDS9960.h>  
  
void setup(){  
Serial.begin(9600);  
if(!APDS.begin()){  
Serial.println("Error initializing sensor!");  
}  
}  
  
void loop(){  
if(APDS.gestureAvailable()){  
switch(APDS.readGesture()){  
case GESTURE\_UP: Serial.println("UP"); break;  
case GESTURE\_DOWN: Serial.println("DOWN"); break;  
case GESTURE\_LEFT: Serial.println("LEFT"); break;  
case GESTURE\_RIGHT: Serial.println("RIGHT"); break;  
}  
}  
}  

Upload via the Arduino IDE, open Serial Monitor to verify events.

**Calibration & Tuning Guide**

**Webcam Framing**

1.  Position camera at chest-to-face height.
2.  Ensure uniform lighting to reduce MediaPipe mis-detections (ideal illumination: 300–500 lx).
3.  Verify that **green threshold line** (Presentation module) bisects your forehead in the preview.

**Latency Optimizations**

*   Use cv2.CAP\_DSHOW flag on Windows for lower capture latency.
*   Reduce resolution to 640×480 for slower CPUs.
*   Adjust MediaPipe min\_detection\_confidence & min\_tracking\_confidence (default 0.5) to trade accuracy for FPS[\[4\]](#fn4)[\[5\]](#fn5).

**Autopy Cursor Jitter**

Increase smoothening > 7 to minimise tremors; values > 15 impair responsiveness.

**Troubleshooting**

| Symptom | Likely Cause | Resolution |
| --- | --- | --- |
| ModuleNotFoundError: mediapipe.python._framework_bindings | Incomplete wheel on ARM/RPi[6] | Install via pip install mediapipe-lite-raspbian-*.whl or compile from source. |
| error: no override and no default toolchain set while installing autopy | Rust not present[7] | Install Rust nightly 2019-10-05 (rustup default nightly-2019-10-05). |
| pycaw install fails on Python 3.12 | Wheels unavailable | Pin Python ≤3.11 or build from source with VS Build Tools[8][3]. |
| Cursor jumps to corners | Incorrect screen size retrieval | Confirm wScr,hScr = autopy.screen.size() returns correct dimensions. |
| Slides not advancing | Hand center below gestureThreshold | Lower threshold constant or raise hand higher. |

**Extending the Suite**

1.  **Custom Gestures** – modify fingersUp patterns or integrate **MediaPipe Gesture Recognizer** model for ML-based classification[\[9\]](#fn9).
2.  **Voice Feedback** – overlay pyttsx3 TTS for confirmation cues.
3.  **Cross-Platform Audio** – swap pycaw for alsaaudio (Linux) or pyobjc-core (macOS) to unify volume control.
4.  **Modular Framework** – refactor repetitive hand-tracking code into a shared gesture\_engine.py.

**Contribution Guidelines**

*   Fork the repo ➜ create feature branch ➜ submit pull request.
*   Adhere to **PEP 8** style; run flake8 before committing.
*   Document new gestures thoroughly in this README and code comments.
*   Hardware-specific changes must include fallback stubs for other OSes.

**License**

All original source files are released under the MIT License.  
Third-party libraries maintain their own licenses (Apache-2.0 for MediaPipe, MIT for cvzone, GPL-compatible for pyautogui, etc.).

**Acknowledgements**

*   **Murtaza Hassan’s CVZone** for simplified MediaPipe wrappers and concise tutorials[\[10\]](#fn10)[\[11\]](#fn11).
*   Google Research for the _MediaPipe Hands_ landmark network[\[12\]](#fn12).
*   Community contributors on StackOverflow, PyPI, and Reddit for installation insights[\[8\]](#fn8)[\[13\]](#fn13)[\[14\]](#fn14)[\[7\]](#fn7).

**End-to-End Test Checklist**

1.  Run python presentation/presentation.py → navigate slides left/right.
2.  Run python virtual\_mouse.py → move cursor, perform click gesture.
3.  Run python volume\_scroll.py → adjust system volume from 10% to 90%.
4.  Launch Chrome offline with chrome://dino → verify space trigger.
5.  Start Hill Climb Racing (BlueStacks/Steam) → brake & accelerate.
6.  Launch a Unity 3D driving game → steer smoothly via both hands.
7.  Open Arduino Serial Plotter → swipe gestures display.

Complete all seven tests to certify a functional installation.

Happy hacking, and enjoy a hands-free computing future!

⁂

1.  [https://www.youtube.com/watch?v=XqepBUU3iL0](https://www.youtube.com/watch?v=XqepBUU3iL0)

1.  [https://pypi.org/project/autopy/](https://pypi.org/project/autopy/)

1.  [https://pypi.org/project/pycaw/](https://pypi.org/project/pycaw/)

1.  [https://mediapipe.readthedocs.io/en/latest/solutions/hands.html](https://mediapipe.readthedocs.io/en/latest/solutions/hands.html)

1.  [https://ai.google.dev/edge/mediapipe/solutions/vision/hand\_landmarker](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker)

1.  [https://github.com/cvzone/cvzone/issues/36](https://github.com/cvzone/cvzone/issues/36)

1.  [https://www.reddit.com/r/pythonhelp/comments/pbpf4z/need\_help\_installing\_autopy/](https://www.reddit.com/r/pythonhelp/comments/pbpf4z/need_help_installing_autopy/)

1.  [https://stackoverflow.com/questions/69807796/how-to-install-pycaw](https://stackoverflow.com/questions/69807796/how-to-install-pycaw)

1.  [https://ai.google.dev/edge/mediapipe/solutions/vision/gesture\_recognizer](https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer)

1.  [https://github.com/cvzone/cvzone](https://github.com/cvzone/cvzone)

1.  [https://www.youtube.com/watch?v=Xt-9WWpPO0Y](https://www.youtube.com/watch?v=Xt-9WWpPO0Y)

1.  [https://arxiv.org/abs/2006.10214](https://arxiv.org/abs/2006.10214)

1.  [https://stackoverflow.com/questions/75748411/cannot-import-cvzone-in-vscode-though-correctly-installed](https://stackoverflow.com/questions/75748411/cannot-import-cvzone-in-vscode-though-correctly-installed)

1.  [https://stackoverflow.com/questions/43692426/how-to-install-pyautogui-on-python3-64-bit-on-windows-10](https://stackoverflow.com/questions/43692426/how-to-install-pyautogui-on-python3-64-bit-on-windows-10)