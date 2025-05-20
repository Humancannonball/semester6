Faculty of Electronics
Department of Computer Science and Communications Technologies

# Laboratory work 10

## Controller chip SSD1306

Report by: Mark Mikula, IRDfu-22

## Work objective

Learn how to use the SSD1306 OLED display controller and implement various graphical elements.

## Task

While completing the tasks, prepare the laboratory report. Write down the steps you take and notes.

1. Download and install the required libraries for the SSD1306 display: Adafruit_GFX and Adafruit_SSD1306.
2. Open the example code and change the I2C address to `0x3C` which is the correct address for most SSD1306 displays.
3. Run the example code and observe the various graphical demonstrations.
4. Create your own program to display text, lines, and shapes on the display.

### Basic "Hello World" Display:

```c++
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1); // OLED_RESET = -1

void setup() {
  Serial.begin(9600); // Initialize serial for debugging
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3C for 128x64
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }
  delay(100); // Pause briefly after init
  displayMessage(); // Call function to display message
}

void loop() {
  // Nothing to do here for a static message
}

void displayMessage() {
  display.clearDisplay();
  display.setTextSize(2);             // Draw 2X-scale text
  display.setTextColor(SSD1306_WHITE); // Draw white text
  display.setCursor(10, 20);          // Start at a centered position
  display.println(F("Hello, world!"));
  display.display();
}
```

### Drawing Lines:

```c++
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

void setup() {
  Serial.begin(9600);
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  }
  delay(100);
  display.clearDisplay(); // Clear display once at setup
  display.display();
}

void loop() {
  display.clearDisplay(); // Clear before drawing new line
  display.drawLine(0, 0, 50, 50, SSD1306_WHITE);
  display.display();
  delay(1000);

  display.clearDisplay();
  display.drawLine(0, 0, display.width()-1, display.height()-1, SSD1306_WHITE); 
  display.display();
  delay(1000);
}
```

### Drawing Animated Circles:

```c++
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

void setup() {
  Serial.begin(9600);
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  }
  delay(100);
  display.clearDisplay();
  display.display();
}

void loop() {
  // Animate a growing circle
  for (int r = 5; r < display.height()/2; r += 5) {
    drawCircleAtCenter(r);
    delay(200);
    display.clearDisplay();
  }
  // Then animate a shrinking circle
  for (int r = display.height()/2 - 5; r >= 5; r -= 5) {
    drawCircleAtCenter(r);
    delay(200);
    display.clearDisplay();
  }
}

void drawCircleAtCenter(int radius) {
  int centerX = display.width() / 2;
  int centerY = display.height() / 2;
  display.drawCircle(centerX, centerY, radius, SSD1306_WHITE);
  display.display();
}
```

5. Observe and document how different shapes and animations are rendered on the SSD1306 display.
6. Prepare the report, upload it to moodle in pdf format.

## Notes

1. The SSD1306 is a single-chip CMOS OLED/PLED driver with controller for organic/polymer light emitting diode dot-matrix graphic display system.
2. Communication with the controller can be done via I2C bus, with a typical address being 0x3C.
3. The Adafruit libraries make it easy to draw various graphical elements, including:
   - Single pixels
   - Lines
   - Rectangles (outline and filled)
   - Circles (outline and filled)
   - Triangles (outline and filled)
   - Text (with different sizes)
   - Bitmap images
4. I2C pins on Arduino Mega are SDA on pin 20 and SCL on pin 21.
5. The display supports animation by quickly clearing and redrawing the screen.

## Conclusion

Working with the SSD1306 OLED display allows for creating interactive visual feedback in Arduino projects. The display is small but versatile, able to show text, shapes, and even simple animations. Through this lab, we've learned how to initialize the display, configure its settings, and draw various elements on it.
