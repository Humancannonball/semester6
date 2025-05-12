# ESP8266 Smart Clock

## Project Overview

This project implements a smart clock using an ESP8266 microcontroller and an OLED display. It displays the current time, synchronizes with an NTP server via WiFi, and includes an alarm function. User interaction is handled via the built-in Flash button (GPIO0).

## Features

-   Real-time display of current time (hours, minutes, seconds) on OLED.
-   Time synchronization with NTP server over WiFi.
-   Fallback to internal timekeeping if WiFi is unavailable.
-   Manual time setting (hours, minutes).
-   Alarm setting (hour, minute) with visual notification on OLED.
-   Toggle alarm ON/OFF.
-   User interface controlled by a single built-in button (GPIO0) with short and long press detection.

## Hardware Components

-   **Microcontroller**: ESP8266 (e.g., NodeMCU, Wemos D1 Mini)
-   **Display**: OLED Display 128x64 pixels, I2C interface (e.g., SSD1306)
-   **Input**: Built-in Flash button on ESP8266 development board (GPIO0)
-   **Connecting Wires**

## Circuit Diagram and Connections

### 1. ESP8266 to OLED Display (I2C)

| ESP8266 Pin | OLED Display Pin | Function   |
|-------------|------------------|------------|
| D1 (GPIO5)  | SCL / SCK        | I2C Clock  |
| D2 (GPIO4)  | SDA              | I2C Data   |
| 3.3V        | VCC              | Power (3.3V) |
| GND         | GND              | Ground     |

*Note: Ensure your OLED display is 3.3V compatible if powered directly from the ESP8266 3.3V pin. The `SmartClock.ino` code uses I2C address `0x3C` for the OLED.*

### 2. ESP8266 Button

The project uses the **built-in Flash button** typically connected to **GPIO0** on most ESP8266 development boards. No external wiring is needed for this button.

### Assembly Notes
-   Use a breadboard for easy connections or solder components for a more permanent setup.
-   Keep I2C signal wires (SDA, SCL) as short as reasonably possible to minimize noise.
-   Double-check all connections before powering on the ESP8266.

## Software Setup

### 1. Install Arduino IDE
If you haven't already, download and install the Arduino IDE from [arduino.cc](https://www.arduino.cc/en/software).

### 2. Install ESP8266 Board Support
-   In Arduino IDE, go to File > Preferences.
-   Enter `http://arduino.esp8266.com/stable/package_esp8266com_index.json` into the "Additional Board Manager URLs" field. Click OK.
-   Go to Tools > Board > Boards Manager. Search for "esp8266" and install the "esp8266 by ESP8266 Community" package (version 2.7.4 or newer recommended).

### 3. Install Required Libraries
Install the following libraries via the Arduino Library Manager (Tools > Manage Libraries):
-   `NTPClient` by Fabrice Weinberg (version 3.2.0 or newer)
-   `Adafruit SSD1306` by Adafruit (version 2.5.0 or newer)
-   `Adafruit GFX Library` by Adafruit (usually installed as a dependency for SSD1306)
-   `Wire` library is built-in.

### 4. Configure WiFi Credentials
Open the `SmartClock.ino` file in the Arduino IDE. Modify the following lines with your WiFi network details:
```cpp
const char* ssid = "YourNetworkSSID";
const char* password = "YourNetworkPassword";
```

### 5. Configure Timezone
In `SmartClock.ino`, find the `utcOffsetInSeconds` variable and adjust it for your local timezone. The value is in seconds.
```cpp
// Examples: UTC+0: 0, UTC+1: 3600, UTC+2: 7200, UTC-5: -18000
const long utcOffsetInSeconds = 0; // Change this to your UTC offset
```

### 6. Upload the Sketch
-   Connect your ESP8266 to your computer via USB.
-   Select your ESP8266 board type (e.g., "NodeMCU 1.0 (ESP-12E Module)") from Tools > Board.
-   Select the correct COM port from Tools > Port.
-   Click the "Upload" button.

## Operating Instructions

### Basic Operation
Upon startup, the clock attempts to connect to WiFi and sync time via NTP. The display shows:
-   Current time (HH:MM:SS).
-   WiFi connection status.
-   Alarm status (ON/OFF) and set alarm time.

### Button Controls (GPIO0)
| Action                       | Mode             | Function                                      |
|------------------------------|------------------|-----------------------------------------------|
| Short Press                  | Normal Display   | Toggle alarm ON/OFF                           |
| Long Press (approx. 2s)      | Normal Display   | Enter Setting Mode (starts with Set Hour)     |
| Short Press                  | Setting Mode     | Increment current value (Hour, Minute, Alarm H/M) |
| Long Press (approx. 2s)      | Setting Mode     | Cycle to next setting field / Exit settings   |
| Any Press                    | Alarm Sounding   | Silence/Stop the current alarm                |

### Setting Sequence (via Long Press)
1.  **Normal Display** -> Long Press ->
2.  **Set Current Hour** (Short press to increment, Long press to move to next) ->
3.  **Set Current Minute** (Short press to increment, Long press to move to next) ->
4.  **Set Alarm Hour** (Short press to increment, Long press to move to next) ->
5.  **Set Alarm Minute** (Short press to increment, Long press to move to next) ->
6.  **Normal Display**

### Alarm Function
-   When the alarm is enabled ("Alarm: ON" displayed) and the current time matches the alarm time, the OLED display will flash, and "ALARM!" will be shown.
-   Press the button to silence the alarm.
-   The alarm automatically stops after approximately 30 seconds if not silenced.

## Troubleshooting

-   **No Display / Gibberish on OLED:**
    *   Check wiring (SDA, SCL, VCC, GND). Ensure D1->SCL, D2->SDA.
    *   Verify the I2C address in `SmartClock.ino` (`0x3C`) matches your display.
-   **WiFi Connection Issues:**
    *   Verify SSID and password in `SmartClock.ino`.
    *   Ensure your WiFi network is 2.4GHz, as ESP8266 typically doesn't support 5GHz.
-   **Time Not Syncing:**
    *   Check WiFi connection.
    *   Ensure `utcOffsetInSeconds` is correctly set.
    *   NTP servers might be temporarily unreachable.
-   **Button Not Working:**
    *   Ensure you are using the built-in Flash button (GPIO0).
-   **Upload Fails / Port Not Found:**
    *   Ensure correct board and port are selected.
    *   Install CH340 or CP210x drivers if your board uses one of these USB-to-Serial chips.
    *   Try a different USB cable.
    *   Hold the Flash/Boot button (GPIO0) while uploading if issues persist.

## Technical Notes
-   The clock attempts NTP synchronization upon startup and then approximately every hour.
-   If WiFi or NTP sync fails, the clock relies on its internal `millis()` for timekeeping. Manual time setting might be required in this case.
-   Button input uses debouncing to prevent multiple triggers from a single press.