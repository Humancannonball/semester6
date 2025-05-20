Faculty of Electronics
Department of Computer Science and Communications Technologies

# Laboratory work 11

## WS2812B Digital LED

Report by: Mark Mikula, IRDfu-22

## Work objective

Learn how to use WS2812B addressable RGB LEDs, understand their signaling protocol, and create color patterns.

## Task

1. Connect the WS2812B LED strip to the Arduino (data pin to pin 7).
2. Install the FastLED library for controlling the LEDs.
3. Write a program to display different colors on the LEDs and observe the signal with an oscilloscope.
4. Analyze the timing and data format of the WS2812B communication protocol.

### Basic Code for Controlling WS2812B LEDs:

```c++
#include <FastLED.h>

#define LED_PIN    7  // Data pin for WS2812B strip
#define NUM_LEDS   1  // Number of LEDs in the strip

CRGB leds[NUM_LEDS];

void setup() {
  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setBrightness(50); // Set global brightness (0-255)
}

void loop() {
  // Cycle through Red, Green, Blue
  // Blue
  leds[0] = CRGB::Blue;
  FastLED.show();
  delay(1000);

  // Red
  leds[0] = CRGB::Red;
  FastLED.show();
  delay(1000);

  // Green
  leds[0] = CRGB::Green;
  FastLED.show();
  delay(1000);
}
```

Once you run this code, you should observe the following with an oscilloscope:
- A signal for color blue consists of 24 bits
- When changing to red color, the signal pattern changes
- Each color has a unique 24-bit pattern

### Extended Code for Multiple LEDs with Different Colors:

```c++
#include <FastLED.h>

#define LED_PIN    7
#define NUM_LEDS   3 // Using 3 LEDs

CRGB leds[NUM_LEDS];

void setup() {
  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setBrightness(50);
}

void loop() {
  // Set different colors to each LED
  
  // Pattern 1: Yellow, Green, White
  leds[0] = CRGB(255, 255, 0); // Yellow
  leds[1] = CRGB(0, 255, 0);   // Green
  leds[2] = CRGB(50, 50, 50);  // Dim white

  FastLED.show();
  delay(1000); // Keep the pattern for 1 second

  // Pattern 2: RGB
  leds[0] = CRGB::Red;
  leds[1] = CRGB::Blue;
  leds[2] = CRGB::Green;
  FastLED.show();
  delay(1000);
  
  // Example: Sequential lighting pattern
  FastLED.clear();
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CRGB::Green;
    FastLED.show();
    delay(200);
  }
  delay(500);
  FastLED.clear();
  FastLED.show();
  delay(500);
}
```

When using 3 LEDs, you should observe:
- A signal with 72 bits (24 bits for each LED)
- The difference between "one" and "zero" bits in the signal
- Different patterns for different color combinations

## WS2812B Protocol Analysis

1. The WS2812B uses a single-wire digital communication protocol.
2. Each LED requires 24 bits of data (8 bits each for red, green, and blue).
3. Observations from oscilloscope measurements:
   - A "0" bit is represented by a short high pulse followed by a longer low pulse
   - A "1" bit is represented by a longer high pulse followed by a shorter low pulse
   - The entire bit period is approximately 1.25μs
   - For a single LED, 24 bits of data are sent (seen on oscilloscope)
   - For multiple LEDs, 24 bits per LED are sent in sequence (e.g., 3 LEDs = 72 bits)

4. Color Intensity:
   - The brightness can be controlled by adjusting the RGB values (0-255 for each component)
   - The global brightness can also be set using FastLED.setBrightness(0-255)

5. Power Considerations:
   - Each LED can draw up to 60mA at full brightness (20mA per color)
   - For longer strips, an external power supply is recommended

## Conclusion

The WS2812B LEDs provide a versatile way to create colorful lighting effects with minimal wiring. The single-wire protocol allows for easy control of multiple LEDs in a chain. By understanding the timing and data format of the protocol, we can better appreciate how these LEDs work and troubleshoot any issues that may arise.
