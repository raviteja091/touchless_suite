#include <Arduino_APDS9960.h>
void setup() {
  Serial.begin(9600);
  if (!APDS.begin()) Serial.println("Sensor error!");
}
void loop() {
  if (APDS.gestureAvailable()) {
    int g = APDS.readGesture();
    if (g==GESTURE_UP) Serial.println("UP");
    if (g==GESTURE_DOWN) Serial.println("DOWN");
    if (g==GESTURE_LEFT) Serial.println("LEFT");
    if (g==GESTURE_RIGHT) Serial.println("RIGHT");
  }
}
