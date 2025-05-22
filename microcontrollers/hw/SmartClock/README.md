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
