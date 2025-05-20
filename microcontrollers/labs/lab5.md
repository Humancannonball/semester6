Faculty of Electronics
Department of Computer Science and Communications Technologies

# Laboratory work 5

## Ultrasonic distance sensors

Report by: Mark Mikula, IRDfu-22

## Work objective

Learn to form control signals, measure the duration of signals.

## Theoretical part

Ultrasonic distance sensors emit high-frequency sound pulses. Our ears can't hear these
signals (I'm not sure about domestic animals). And waits for these signals to bounce back after
being reflected off the obstacle. All we have to do is measure how long the signal's journey took.
We know that the speed of sound in air is 331.5 m/s at 0 °C. To estimate the influence of
temperature, we use the following formula: `v[m/s]=331.5+0.6∙T[℃]`. Just don't forget that the
signal travels twice the distance, i.e. to the obstacle and back. The distance measured by such
sensors is from a few cm to 3-5 meters.

Parking distance meters in cars work on exactly the same principle when we park. Only
there are more sensors (typically four at the front and four at the back). They are installed in
smaller enclosures and sealed as required. The control unit of these sensors is located in the
cabin, and the distance is indicated by sound signals and/or numbers on the screen.

The measurement procedure is simple. The microcontroller (MC) must generate a pulse
(5 microseconds long) on GPIO pin 48 (TRIG) that activates the measurement. Then the sensor HCSR04 at the other output 8 (ECHO) forms a pulse whose duration is proportional to the travel
time of the ultrasonic signal.

Measurement procedure for 4-pin sensor:

1.  Set the GPIO pin 48, to which the TRIG pin of the sensor is connected, to the output
    (OUTPUT) mode. Set high level to pin 48, wait 5 microseconds.
2.  Set a low level to pin 48.
    //pulse duration measurement
3.  Set pin 8 to input mode (INPUT)
4.  Wait for pin 8 level to change from low to high level.
5.  Record the time t1 (use the function `micros()`).
6.  Wait until the state of pin 8 changes to a low level.
7.  Record the time t2.
8.  The duration of the pulse (the travel time of the ultrasonic signal) will be `t=t2-t1`.
9.  Estimate the temperature, speed of sound, time and calculate the distance.

The program should evaluate cases where the obstacle is outside the measurement range.

## Task

Write down the steps you take and notes.

1.  Connect the ultrasonic distance sensor to the EL Lab board. Connect the GND and
    POWER sensor pins to Arduino GND and 5V pins, and the sensor TRIG pin to Arduino
    GPIO pin 8. Connect an oscilloscope to the TRIG signal (TP14) and observe the TRIG
    signal. (take a photo of the signal). Connect an oscilloscope (Test Point TP13) to the
    ECHO line and set the time axis to 2 ms/cell. Observe how the duration of the pulse
    changes depending on the distance to the obstacle. (Take a photo of the signal)

    **Notes from observation:**
    * TP13 echo - The longer distance, the longer the signal. The pulse time is 
      proportional to propagation time.
    * TP14 - The trigger impulse. This pulse starts the measurement.

2.  Create a program that measures the distance every second and outputs the result in
    centimeters to the Serial Monitor window. The ambient temperature is 25 °C.
3.  Calibrate your meter so that the measured results match the position of the obstacle.
4.  BONUS. Output the measured distance in centimeters to the 7-segment display.

### Code:

```c++
#define TRIG_PIN 48
#define ECHO_PIN 8
#define SEG1 46
#define SEG2 47

int ones;
int tens;

const uint8_t numbers[10]={
  0b00111111, // 0
  0b00000110, // 1
  0b01011011, // 2
  0b01001111, // 3
  0b01100110, // 4
  0b01101101, // 5
  0b01111100, // 6
  0b00000111, // 7
  0b01111111, // 8
  0b01100111  // 9
};

void setup() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(SEG1,OUTPUT);
  pinMode(SEG2,OUTPUT);
  DDRA=255; // pinMode(22 - 29, OUTPUT); 
  digitalWrite(SEG1,0); // Assuming SEG1 is active LOW for selection
  Serial.begin(9600);
}

void loop() {
  long duration, distance;

  // Clears the TRIG_PIN condition
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  // Sets the TRIG_PIN HIGH (ACTIVE) for 5 microseconds
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(5);
  digitalWrite(TRIG_PIN, LOW);

  // Reads the ECHO_PIN, returns the sound wave travel time in microseconds
  duration = pulseIn(ECHO_PIN, HIGH);
  
  // Calculating the distance
  // The speed of sound at 25°C is approximately 346.13 m/s
  // To convert to cm/µs: 346.13 m/s * 100 cm/m * 1e-6 s/µs = 0.034613 cm/µs
  distance = duration * 0.034613 / 2; // More precise calculation for 25°C

  ones = distance % 10; // i divided by 10, remainder taken
  tens = distance / 10; // i divided by 10, whole taken

  Serial.println(ones);
  Serial.println(tens);

  if (distance >= 99 || distance <= 2) {
    for (int j = 0; j < 100; j++){
      PORTA = numbers[9];
      digitalWrite(SEG1, HIGH); // Activate segment display 1
      digitalWrite(SEG2, LOW);  // Deactivate segment display 2
      delay(5);
      PORTA = numbers[9];
      digitalWrite(SEG1, LOW);  // Deactivate segment display 1
      digitalWrite(SEG2, HIGH); // Activate segment display 2
      delay(5);
      // Optional: Turn both off briefly to prevent ghosting
      // digitalWrite(SEG1, LOW); 
      // digitalWrite(SEG2, LOW);
    }
  } else {
    for (int j = 0; j < 100; j++){
      PORTA = numbers[tens];
      digitalWrite(SEG1, HIGH); // Activate segment display 1
      digitalWrite(SEG2, LOW);  // Deactivate segment display 2
      delay(5);
      PORTA = numbers[ones];
      digitalWrite(SEG1, LOW);  // Deactivate segment display 1
      digitalWrite(SEG2, HIGH); // Activate segment display 2
      delay(5);
      // Optional: Turn both off briefly to prevent ghosting
      // digitalWrite(SEG1, LOW);
      // digitalWrite(SEG2, LOW);
    }
  }

  Serial.print("Distance: ");
  if (distance >= 99 || distance <= 2) {
    Serial.println("Out of range");
  } else {
    Serial.print(distance);
    Serial.println(" cm");
  }
  // Wait for 1 second (total loop time should be considered)
  delay(10); // This delay is very short, consider if 1 second is needed between measurements
}
```
