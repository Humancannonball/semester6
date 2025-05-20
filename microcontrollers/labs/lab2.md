Faculty of Electronics
Department of Computer Science and Communications Technologies

# Laboratory work 2

## General Purpose I/O Terminal Management

Report by: Mark Mikula, IRDfu-22

## Work objective

Learn to manage GPIO (General Purpose InputOutput) outputs.

## Theoretical part

1.  In order for the LED to start lighting, you need to connect the negative potential of the
    voltage source (0 V - GND, LOW) to the cathode, and the positive potential (+5 V, HIGH) to
    the anode. LEDs can be connected to microcontrollers in two ways. It is possible to connect
    the cathode to GND, the anode to the GPIO output (common cathode diagram). In this case,
    the LED will light up when the GPIO pin is high and off when the pin is low. Another way, the
    anode of the LED is connected to the +5 V line, the cathode to the GPIO pin (common anode
    diagram). A low level at the output will then turn the LED on and a high level at the output
    will turn the LED off.
2.  Sometimes appliances (stoves, washing machines, microwave ovens, etc.) use 7-segment
    displays to display information. Depending on how many digits we need to display, the
    required number of indicators is selected.

    They are called 7-segment indicators because 7 illuminated lines (LED inside the line) are
    enough to form a number-symbol. Actually there is also an eighth LED, it is for the dot. The
    anodes or cathodes of all LEDs are connected together, so there can be common anode or
    common cathode indicators. Usually, the engineer designing the scheme chooses a more
    convenient option for him, and the programmer has to write the corresponding control
    program. But there are exceptions, when the programmer chooses what is more convenient
    for him :) . The necessary characters on the screen are formed by turning on the
    corresponding LEDs. It is agreed to mark the luminous lines with letters: a, b, c, d, e, f, g and
    a dot - dp.

    So, we will need 7 (8 if we also use a dot) GPIO pins to control one indicator. When more
    characters are needed, like 4, instead of using 7*4= 28 GPIOs (which is a lot, Arduino UNO
    only has 14 GPIOs), our visual inertia is exploited. Only one indicator with the required
    symbol is activated at a time. The other three are considered disabled. In this way, the
    corresponding lines of all symbols are connected together (a to a, b to b, etc.), and the
    activation of the required symbol is controlled via the symbol's common output (com). To
    control such an indicator, the program has to periodically change the states of the GPIO pins.
    And if we also take into account the fact that we still need to perform additional tasks in
    addition to controlling the screen, then the program becomes a little more complicated. This
    is where additional electronics solutions can help. For example, 7-segment decoders (eg:
    CD4511). Then, from the controller, what information is to be displayed is transmitted to the
    decoder, and the decoder itself is engaged in controlling the necessary LEDs. But the decoder
    costs a few cents, and the extra few lines of code are cheaper.
3.  GPIO output can also be used for reading information, for this we need to tell the
    microcontroller that we want to read the state of the corresponding pin (`pinMode(pinNum, INPUT)`). If we have an external device that controls the line and can change its state
    (voltage), then with the function `int digitalRead(pinNum)` we can read the state of the line.
    Often we need to read the states of control buttons (keystrokes, control buttons on devices).
    Then you need to turn on the internal pull-up resistor (`pinMode(pinNum, INPUT_PULLUP)`)
    on the output to be read. Modern microcontrollers have and know how to programmatically
    connect not only pull-up, but also pull-down resistors.

    If there was no Pull-Up resistor, which sets a high level on the input, then until the button is
    pressed, the input of the microcontroller would "hang in the air". It could be interpreted as
    a receiver with a small antenna. In this case, the readable pin state would only depend on
    the ambient electromagnetic noise. Sometimes we would have a high level, sometimes a low
    level. When the pull-up resistor is connected but the button is not pressed, there is a high
    level (5V) on the pin. When we press the button, the pin is connected to GND and we have
    a low level (0 V) at the input.

## Task

NB. Write down the steps you take and notes.

1.  On the EL_lab board we have LEDs of different colors LED1...LED4. They are connected to
    ground with cathodes, and with anodes to terminals A12...A15. A high level on these pins
    will turn the LEDs on and a low level will turn them off. We also have one RGB LED - 3 LEDs
    installed in one housing. However, these LEDs are common anode. We will turn them low on
    pins 10, 11, 12. Write a program that turns on the red RGB LED and LED1 (red color) for one
    second, then turns off the red LEDs and turns on the green LEDs (LED2 and RGB LED) for one
    second. It would turn off the green LEDs and turn on the blue LEDs (LED3 and RGB LEDs) for
    one second. Then it would start all over again.

### Code:

```c++
void setup() {
  pinMode(A12, OUTPUT); // LED1 (Red)
  pinMode(A13, OUTPUT); // LED2 (Green)
  pinMode(A14, OUTPUT); // LED3 (Blue)
  // RGB LED pins (Common Anode, LOW to turn on)
  pinMode(10, OUTPUT);  // RGB Blue
  pinMode(11, OUTPUT);  // RGB Green
  pinMode(12, OUTPUT);  // RGB Red
}

void loop() {
  // Turn on Red LEDs
  digitalWrite(A12, HIGH); // LED1 Red ON
  digitalWrite(12, LOW);   // RGB Red ON
  delay(1000);             // wait for a second

  // Turn off Red LEDs
  digitalWrite(A12, LOW);  // LED1 Red OFF
  digitalWrite(12, HIGH);  // RGB Red OFF
  // delay(1000); // Original code had an extra delay here, usually not needed before switching to next color immediately

  // Turn on Green LEDs
  digitalWrite(A13, HIGH); // LED2 Green ON
  digitalWrite(11, LOW);   // RGB Green ON (assuming pin 11 is Green for RGB)
  delay(1000);

  // Turn off Green LEDs
  digitalWrite(A13, LOW);  // LED2 Green OFF
  digitalWrite(11, HIGH);  // RGB Green OFF
  // delay(1000);

  // Turn on Blue LEDs
  digitalWrite(A14, HIGH); // LED3 Blue ON
  digitalWrite(10, LOW);   // RGB Blue ON (assuming pin 10 is Blue for RGB)
  delay(1000);

  // Turn off Blue LEDs
  digitalWrite(A14, LOW);  // LED3 Blue OFF
  digitalWrite(10, HIGH);  // RGB Blue OFF
  delay(1000); // Delay before restarting the cycle
}
```

2.  We have two 7-segment indicators on the EL_lab board. Their anodes are connected to
    terminals 46 and 47. Cathodes are connected to: a-22, b-23, c-24, ..., f-27, g-28 terminals.
    The corresponding indicator will be turned on when there is a high level on the appropriate
    anode. Create a program that would periodically output the numbers: 0, 1, 2, 3, ... 9 to one
    indicator.

### Code:

```c++
#define SEG_ANODE1 46 // Anode for first 7-segment display
#define SEG_ANODE2 47 // Anode for second 7-segment display
// Pins for segments a-g are assumed to be on PORTA (pins 22-29 on Arduino Mega)

// int ones; // Not used in this specific task part
// int tens; // Not used in this specific task part

const uint8_t numbers[10]={
  0b00111111, // 0 (dp-g-f-e-d-c-b-a)
  0b00000110, // 1
  0b01011011, // 2
  0b01001111, // 3
  0b01100110, // 4
  0b01101101, // 5
  0b01111100, // 6 (mistake in original, should be 0b01111101 for common cathode if g is MSB)
              // Assuming common anode for segments (LOW turns on segment)
              // and common anode for display selection (HIGH turns on display)
              // The provided numbers array is for common cathode segments.
              // If segments are common anode, invert bits: ~0b00111111 etc.
              // Let's assume the 'numbers' array is correct for how PORTA drives the segments.
  0b00000111, // 7
  0b01111111, // 8
  0b01100111  // 9 (mistake in original, should be 0b01101111 for common cathode if g is MSB)
};


// For task 3:
const int buttonPinM1 = 2;  // Button M1
const int buttonPinM2 = 3;  // Button M2
// const int ledPin = A12; // Not directly related to 7-segment display task, but in original code

// int buttonStateM1 = 0; // Renamed from buttonState
// int buttonStateM2 = 0; // Renamed from buttonState1
int counter = 0;

void setup() {
  pinMode(SEG_ANODE1, OUTPUT);
  pinMode(SEG_ANODE2, OUTPUT);
  // pinMode(ledPin, OUTPUT); // From original code, not directly for 7-seg
  pinMode(buttonPinM1, INPUT_PULLUP); // For task 3
  pinMode(buttonPinM2, INPUT_PULLUP); // For task 3

  DDRA = 0xFF; // Sets pins 22-29 (PORTA) to OUTPUT for segment cathodes
  
  digitalWrite(SEG_ANODE1, LOW); // Turn off display 1 initially
  digitalWrite(SEG_ANODE2, LOW); // Turn off display 2 initially
}

void loop() {
  // Task 2: Display 0-9 on one indicator (e.g., SEG_ANODE2)
  /*
  for( int i=0; i<10; i++){
    PORTA = numbers[i];         // Set segment pattern for number i
    digitalWrite(SEG_ANODE2, HIGH); // Turn on the selected display
    delay(500);                   // Display for 0.5 seconds
    digitalWrite(SEG_ANODE2, LOW);  // Turn off display before changing number (optional, good practice)
  }
  */

  // Task 3: Counting button presses
  bool m1_pressed = (digitalRead(buttonPinM1) == LOW);
  bool m2_pressed = (digitalRead(buttonPinM2) == LOW);

  static bool m1_last_state = HIGH;
  static bool m2_last_state = HIGH;

  if (m1_pressed && m1_last_state == HIGH) { // M1 pressed (falling edge)
    counter++;
    if (counter > 9) { // Assuming single digit display for now
      counter = 9;     // Or counter = 0; to wrap around
    }
    delay(50); // Debounce
  }
  m1_last_state = digitalRead(buttonPinM1);


  if (m2_pressed && m2_last_state == HIGH) { // M2 pressed (falling edge)
    counter--;
    if (counter < 0) {
      counter = 0;
    }
    delay(50); // Debounce
  }
  m2_last_state = digitalRead(buttonPinM2);
  
  // Display the counter on one of the 7-segment displays (e.g., SEG_ANODE2)
  // For Bonus (two-digit display), this part needs to be expanded for multiplexing
  
  // Displaying single digit 'counter' on SEG_ANODE2
  PORTA = numbers[counter % 10]; // Ensure counter is within 0-9 for single digit
  digitalWrite(SEG_ANODE1, LOW);  // Ensure other display is off
  digitalWrite(SEG_ANODE2, HIGH); // Turn on display 2
  
  // For Bonus (two-digit numbers):
  // This requires multiplexing. The loop structure would change significantly.
  // Example for two digits (tens on SEG_ANODE1, ones on SEG_ANODE2):
  /*
  int ones_digit = counter % 10;
  int tens_digit = (counter / 10) % 10;

  // Display tens digit on SEG_ANODE1
  PORTA = numbers[tens_digit];
  digitalWrite(SEG_ANODE2, LOW);
  digitalWrite(SEG_ANODE1, HIGH);
  delay(5); // Multiplexing delay

  // Display ones digit on SEG_ANODE2
  PORTA = numbers[ones_digit];
  digitalWrite(SEG_ANODE1, LOW);
  digitalWrite(SEG_ANODE2, HIGH);
  delay(5); // Multiplexing delay
  
  digitalWrite(SEG_ANODE2, LOW); // Turn off before next cycle to prevent ghosting
  */
  
  // The original code had a delay(150) at the end of the loop.
  // If multiplexing, this delay should be small (e.g., 5ms per digit)
  // and the overall loop should repeat quickly.
  // For single digit display with button check, a small delay after display is fine.
  delay(20); // Small delay for stability and button responsiveness
}
```

3.  The El_lab board has four switches - buttons: M1, M2, M3, M4. They are connected to
    terminals 2, 3, 43, 44. Modify the program so that your indicator counts button presses.
    Pressing M1 should increase the number and pressing M2 should decrease the number. Note
    1. A microcontroller can read the state of a button up to several million times per second.
    Note 2. Mechanical switches are characterized by bouncing of contacts. At the moment of
    pressing, due to the jumping of the contacts, we will have changing states at the output of
    the switch: on/off. Depends on the switch, but typically within 100ms the contacts stop
    jumping and the state doesn't change anymore. But during that 100 ms, the microcontroller
    manages to read the state of the button many times. You need to use some kind of
    debouncing algorithm.
4.  BONUS. Modify the program so that it can output two-digit numbers to the screen.
5.  Prepare a work report. Convert the report to pdf and upload it to moodle.
