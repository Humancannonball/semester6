Faculty of Electronics
Department of Computer Science and Communications Technologies

# Laboratory work 4

## Combination of keyboard and 7-segment indicator

Report by: Mark Mikula, IRDfu-22

## Task

1.  Display the number (symbol) dialed on the keyboard on the 7-segment screen.
2.  Display the two-digit number (symbol) dialed on the keyboard on the 7-segment display.

### Code:

```c++
#define SEG1 46
#define SEG2 47

int ones;
int tens;

int c1 = 34, c2 = 35, c3 = 36, c4 = 37;
int r1 = 30, r2 = 31, r3 = 32, r4 = 33;
int del = 300;

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
  Serial.begin(9600);
  Serial.println("testas");

  pinMode(c1, INPUT_PULLUP);
  pinMode(c2, INPUT_PULLUP);
  pinMode(c3, INPUT_PULLUP);
  pinMode(c4, INPUT_PULLUP);

  pinMode(r1, OUTPUT);
  pinMode(r2, OUTPUT);
  pinMode(r3, OUTPUT);
  pinMode(r4, OUTPUT);

  pinMode(SEG1,OUTPUT);
  pinMode(SEG2,OUTPUT);
  DDRA=255; // pinMode(22 - 29, OUTPUT);
  digitalWrite(SEG1,0); // Assuming SEG1 is active LOW for selection
}

void loop() {
  row1();
  row2();
  row3();
  row4();
}

void display_digit(int digit_to_display, int segment_select_pin) {
    // Assuming segment_select_pin HIGH activates the display
    // and PORTA drives the segments (common cathode assumed by numbers array)
    digitalWrite(SEG1, LOW); // Turn off other segment if multiplexing
    digitalWrite(SEG2, LOW); // Turn off other segment if multiplexing

    PORTA = numbers[digit_to_display % 10]; // Display the unit part of the number
    if (segment_select_pin == SEG1) {
        digitalWrite(SEG1, HIGH);
    } else if (segment_select_pin == SEG2) {
        digitalWrite(SEG2, HIGH);
    }
    delay(5); // Hold time for display
}

void display_char(uint8_t char_pattern, int segment_select_pin) {
    digitalWrite(SEG1, LOW);
    digitalWrite(SEG2, LOW);

    PORTA = char_pattern;
    if (segment_select_pin == SEG1) {
        digitalWrite(SEG1, HIGH);
    } else if (segment_select_pin == SEG2) {
        digitalWrite(SEG2, HIGH);
    }
    delay(5);
}


void row1() {
  digitalWrite(r1, LOW);
  digitalWrite(r2, HIGH);
  digitalWrite(r3, HIGH);
  digitalWrite(r4, HIGH);

  if (digitalRead(c1) == LOW) {
    Serial.println("1"); delay(del);
    // Display 01
    display_digit(0, SEG1); 
    display_digit(1, SEG2);
  }
  else if (digitalRead(c2) == LOW) {
    Serial.println("2"); delay(del);
    // Display 02
    display_digit(0, SEG1);
    display_digit(2, SEG2);
  }
  else if (digitalRead(c3) == LOW) {
    Serial.println("3");delay(del);
    // Display 03
    display_digit(0, SEG1);
    display_digit(3, SEG2);
  }
  else if (digitalRead(c4) == LOW) {
    Serial.println("A");delay(del);
    // Display 0A (A is 0b01110111)
    display_digit(0, SEG1);
    display_char(0b01110111, SEG2);
  }
}

void row2() {
  digitalWrite(r1, HIGH);
  digitalWrite(r2, LOW);
  digitalWrite(r3, HIGH);
  digitalWrite(r4, HIGH);

  if (digitalRead(c1) == LOW) {
    Serial.println("4"); delay(del);
    // Display 04
    display_digit(0, SEG1);
    display_digit(4, SEG2);
  }
  else if (digitalRead(c2) == LOW) {
    Serial.println("5"); delay(del);
    // Display 05
    display_digit(0, SEG1);
    display_digit(5, SEG2);
  }
  else if (digitalRead(c3) == LOW) {
    Serial.println("6"); delay(del);
    // Display 06
    display_digit(0, SEG1);
    display_digit(6, SEG2);
  }
  else if (digitalRead(c4) == LOW) {
    Serial.println("B");delay(del);
    // Display 0B (B is like 8: 0b01111111)
    display_digit(0, SEG1);
    display_char(numbers[8], SEG2); // Using '8' for 'B'
  }
}

void row3() {
  digitalWrite(r1, HIGH);
  digitalWrite(r2, HIGH);
  digitalWrite(r3, LOW);
  digitalWrite(r4, HIGH);

  if (digitalRead(c1) == LOW) {
    Serial.println("7"); delay(del);
    // Display 07
    display_digit(0, SEG1);
    display_digit(7, SEG2);
  }
  else if (digitalRead(c2) == LOW) {
    Serial.println("8");delay(del);
    // Display 08
    display_digit(0, SEG1);
    display_digit(8, SEG2);
  }
  else if (digitalRead(c3) == LOW) {
    Serial.println("9");delay(del);
    // Display 09
    display_digit(0, SEG1);
    display_digit(9, SEG2);
  }
  else if (digitalRead(c4) == LOW) {
    Serial.println("C");delay(del);
    // Display 0C (C is 0b00111001)
    display_digit(0, SEG1);
    display_char(0b00111001, SEG2);
  }
}

void row4() {
  digitalWrite(r1, HIGH);
  digitalWrite(r2, HIGH);
  digitalWrite(r3, HIGH);
  digitalWrite(r4, LOW);

  if (digitalRead(c1) == LOW) {
    Serial.println("*");delay(del);
    // Display something for * if needed, e.g., blank or a specific pattern
  }
  else if (digitalRead(c2) == LOW) {
    Serial.println("0");delay(del);
    // Display 00
    display_digit(0, SEG1);
    display_digit(0, SEG2);
  }
  else if (digitalRead(c3) == LOW) {
    Serial.println("#");delay(del);
    // Display something for # if needed
  }
  else if (digitalRead(c4) == LOW) {
    Serial.println("D");delay(del);
    // Display 0D (D is like 0: 0b00111111, or a specific pattern for D)
    // Using '0' for 'D' as per original code logic for SEG2
    display_digit(0, SEG1); 
    display_char(numbers[0], SEG2); 
  }
}
```
