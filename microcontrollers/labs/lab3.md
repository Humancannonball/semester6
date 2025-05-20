Faculty of Electronics
Department of Computer Science and Communications Technologies

# Laboratory work 3

## Use of GPIO in various situations

Report by: Mark Mikula, IRDfu-22

## Work objective

Learn how to use GPIO pins to control various peripherals

## Theoretical part

RGB LED - LED with three color LEDs in one crystal. Has 4 pins. One anode which connects to
VCC and 3 terminals: Red (R), Green (G) and Blue (B). By enabling combinations of primary colors,
we can create other colors. We can have 7 colors in total. A single pixel in smartphone screens is a
micro RGB LED. Advertising screens in cities are constructed using similar RGB LEDs. By changing the
currents flowing through the LEDs of the corresponding colors, we can obtain all the color intensities
visible to the human eye. We won't be able to do this with GPIO alone, but later we will study the
PWM signals that make this possible.

Tilt sensors can be the most diverse. From very precise, when you can estimate the direction
and angle of an object (building, car, phone, etc.) to the simplest, when tilting the sensor +/- 15
degrees, its internal switch is activated. Previously, mercury (a metal that is poisonous to us) was
used, a drop of which moved the sensor when it was tilted and connected the contacts. MEMS
(Micro Electronic Mechanical Systems) are now used because it is safer.

Reading the status of such a sensor is exactly the same as reading the status of a simple
switch. We activate the pull-up resistor. We connect one end of the sensor to the reading output,
the other to GND. Keyboards can be different, but they are very similar in structure. The type of
keyboard shown below is mostly used in Arduino (and not only) projects. Each button is the simplest
switch.

In order to save pins, the buttons are arranged as a matrix. Clicking the button connects the
corresponding row to the corresponding column. There are different ways to read button presses.
The simplest is to connect all lines to MV GPIO lines. Then configure the row pins for reading with
the pull-up resistors on, and the column pins for writing. The reverse is also possible, since the rows
and columns are completely equivalent to the conclusion. In the initial state, all column lines must
be at a high level. Then we select the first column C1, writing a low level in its line. Due to the pull-
up resistors, when reading the R1 line we will have a high level when no button on the R1 line is
pressed. And we will have a low level when the "1" button is pressed, because this button will
connect the low level C1 line to the R1 line. Buttons "4", "7", "*" respectively will activate the low
level on the lines of the next lines being read. This reads the buttons in column C1. The C1 column
is then brought back high and the next column is selected (low level). We repeat the line scan again.
This polls all buttons. Computer keyboard buttons can be polled about 50 times per second. Simpler
keyboards may be polled less frequently. It all depends on the purpose of the system.

When developing and testing program code, it is convenient to display variable states or
other diagnostic information. This can be done by programming Arduino as well. Arduino can
exchange information with the computer through a virtual com port. For this we need to activate
the Arduino UART interface: `Serial.begin(9600);` where 9600 is the communication rate in
bits/second. Further in the program you can use: `Serial.print("text")`, `Serial.print(variable)`. The same
applies to `Serial.println()`, only in this case a newline command will be added. `cout/cin`, `printf`
functions are not supported. You can monitor Arduino messages in the SerialMonitor window (in
the Aruino IDE).

## Task

Write down the steps you take and notes.

1.  Connect the tilt sensor to the SERVO connector. The inclination sensor will have one contact
    connected to GND, the other to pin 9. The sensor behaves like a simple switch. Create a program
    that would turn on a new (7 in total) RGBLED color (10, 11, 12 output pins, set LOW to enable).
2.  Connect the keyboard (Keypad 4x4 ) to the KEYBOARD connector. Create a program would
    output the number or symbol of the pressed button to computer terminal (Serial monitor).

### Code:

```c++
int c1 = 34, c2 = 35, c3 = 36, c4 = 37; // Column pins
int r1 = 30, r2 = 31, r3 = 32, r4 = 33; // Row pins

void setup() {
  Serial.begin(9600);

  // Set column pins as OUTPUT initially for scanning
  // This will be changed in each doColumnX function
  // pinMode(c1, OUTPUT);
  // pinMode(c2, OUTPUT);
  // pinMode(c3, OUTPUT);
  // pinMode(c4, OUTPUT);

  // Set row pins as INPUT_PULLUP
  pinMode(r1, INPUT_PULLUP);
  pinMode(r2, INPUT_PULLUP);
  pinMode(r3, INPUT_PULLUP);
  pinMode(r4, INPUT_PULLUP);
}

void loop() {
  doColumn1();
  doColumn2();
  doColumn3();
  doColumn4();
}

void doColumn1() {
  // Configure pins for scanning column 1
  pinMode(c1, OUTPUT);
  pinMode(c2, INPUT); // Set other columns to INPUT to avoid shorts if multiple buttons in different columns are pressed
  pinMode(c3, INPUT);
  pinMode(c4, INPUT);

  digitalWrite(c1, LOW);  // Activate column 1
  digitalWrite(c2, HIGH); // Deactivate other columns (not strictly necessary if they are INPUT)
  digitalWrite(c3, HIGH);
  digitalWrite(c4, HIGH);

  if (digitalRead(r1) == LOW) {
    Serial.println("1");
    delay(150); // Debounce delay
  } else if (digitalRead(r2) == LOW) {
    Serial.println("4");
    delay(150);
  } else if (digitalRead(r3) == LOW) {
    Serial.println("7");
    delay(150);
  } else if (digitalRead(r4) == LOW) {
    Serial.println("*");
    delay(150);
  }
}

void doColumn2() {
  // Configure pins for scanning column 2
  pinMode(c1, INPUT);
  pinMode(c2, OUTPUT);
  pinMode(c3, INPUT);
  pinMode(c4, INPUT);

  digitalWrite(c1, HIGH);
  digitalWrite(c2, LOW);  // Activate column 2
  digitalWrite(c3, HIGH);
  digitalWrite(c4, HIGH);

  if (digitalRead(r1) == LOW) {
    Serial.println("2");
    delay(150);
  } else if (digitalRead(r2) == LOW) {
    Serial.println("5");
    delay(150);
  } else if (digitalRead(r3) == LOW) {
    Serial.println("8");
    delay(150);
  } else if (digitalRead(r4) == LOW) {
    Serial.println("0");
    delay(150);
  }
}

void doColumn3() {
  // Configure pins for scanning column 3
  pinMode(c1, INPUT);
  pinMode(c2, INPUT);
  pinMode(c3, OUTPUT);
  pinMode(c4, INPUT);

  digitalWrite(c1, HIGH);
  digitalWrite(c2, HIGH);
  digitalWrite(c3, LOW);  // Activate column 3
  digitalWrite(c4, HIGH);

  if (digitalRead(r1) == LOW) {
    Serial.println("3");
    delay(150);
  } else if (digitalRead(r2) == LOW) {
    Serial.println("6");
    delay(150);
  } else if (digitalRead(r3) == LOW) {
    Serial.println("9");
    delay(150);
  } else if (digitalRead(r4) == LOW) {
    Serial.println("#");
    delay(150);
  }
}

void doColumn4() {
  // Configure pins for scanning column 4
  pinMode(c1, INPUT);
  pinMode(c2, INPUT);
  pinMode(c3, INPUT);
  pinMode(c4, OUTPUT);

  digitalWrite(c1, HIGH);
  digitalWrite(c2, HIGH);
  digitalWrite(c3, HIGH);
  digitalWrite(c4, LOW);  // Activate column 4

  if (digitalRead(r1) == LOW) {
    Serial.println("A");
    delay(150);
  } else if (digitalRead(r2) == LOW) {
    Serial.println("B");
    delay(150);
  } else if (digitalRead(r3) == LOW) {
    Serial.println("C");
    delay(150);
  } else if (digitalRead(r4) == LOW) {
    Serial.println("D");
    delay(150);
  }
}
```

3.  Prepare the report: task charts and corresponding programs. Convert to pdf and upload to
    moodle.

## Connection diagram

```
Posvyrio jutiklis
GND
9
SERVO

30 31 32 33 34
35 36
37
Rows {30-33}, Columns {34-37}
Arduino EL lab 2021
```
*1 fig. Connection diagram of tilt sensor and keyboard*
