Faculty of Electronics
Department of Computer and Communication Technologies

# Laboratory work 9

## Examining WD timer and sleep modes

Report by: Mark Mikula, IRDfu-22

## Work objective

Learn how to use the WD timer.

## Task

While completing the tasks, in parallel, prepare the report of the laboratory work. Write down the
steps you take and notes.

1.  Using the AVR libc library, write a function to disable the WD timer. In all the following
    experiments programs, execute WDT disable first.
2.  Configure the WDT timer to call an interrupt every 0.5s. In the interrupt service function,
    change the state of pin 9 to the opposite (on-off-on ...).

### Code

```c++
#include <avr/wdt.h>

boolean kint = false;

void setup()
{
  pinMode(A13,OUTPUT);
  cli(); //##//disable all interrupts
  wdt_reset(); //reset the wdt timer
  /*
  WDTCSR configuration;
  WDIE = 1:Interrupt Enagle
  WDE = 1 :Reset Enable
  WDP3 = 0 :For 2000ms Time-out
  WDP2 = 1 :For 2000ms Time-out
  WDP1 = 1 :For 2000ms Time-out
  WDP0 = 1 :For 2000ms Time-out
  */
  //Enter Watchdog configuration mode:
  WDTCSR |=(1<<WDCE) | (1<<WDE);
  // Set watchdog settings:
  WDTCSR = (1<<WDIE) | (1<<WDE) | (0<WDP3) | (1<<WDP2) | (0<<WDP1) |
  (1<<WDP0);
  sei();
}

void loop()
{
}

ISR(WDT_vect)// Watchdog timer interrupt.
{
  WDTCSR = (1<<WDIE);
  kint = !kint;
  digitalWrite(A13,kint);
}
```

3.  Change pin 9 in the program to the pin to which the LED is connected. Adjust the
    program so that the LED blinks every one second. Make sure that resetting the WDT will
    not allow an interrupt to occur (reset the WDT in the loop function).
    Configure WDT to call an interrupt every 2 seconds. Use and put the microcontroller into
    power_down sleep mode in the `loop()` loop. Prove that after executing the `sleep_cpu()` function,
    the controller actually remains in sleep mode until woken by WDT.

### Code:

```c++
#include <avr/wdt.h>
#include <avr/sleep.h>

boolean kint = false;
long oldtime;

void setup()
{
  pinMode(A12,OUTPUT);
  pinMode(A13,OUTPUT);
  cli(); //##//disable all interrupts
  wdt_reset(); //reset the wdt timer
  Serial.begin(1000000);
  /*
  WDTCSR configuration;
  WDIE = 1:Interrupt Enagle
  WDE = 1 :Reset Enable
  WDP3 = 0 :For 2000ms Time-out
  WDP2 = 1 :For 2000ms Time-out
  WDP1 = 1 :For 2000ms Time-out
  WDP0 = 1 :For 2000ms Time-out
  */
  //Watchdog configuration mode:
  WDTCSR |=(1<<WDCE) | (1<<WDE);
  WDTCSR = (1<<WDIE) | (1<<WDE) | (0<WDP3) | (1<<WDP2) | (1<<WDP1) |
  (1<<WDP0);
  sei();
}

void loop(){
  wdt_disable();
  oldtime = micros();
  wdt_reset(); //reset the wdt timer
  sleep_enable();
  set_sleep_mode(SLEEP_MODE_PWR_DOWN);
  digitalWrite(A13,0);
  sleep_cpu();
  // Serial.println("loop");
  digitalWrite(A13,1);
  Serial.print("t: ");
  Serial.println(micros()-oldtime) ;
  //delay(1000);
}

ISR(WDT_vect)// Watchdog timer interrupt.
{
  WDTCSR = (1<<WDIE);
  kint = !kint;
  digitalWrite(A12,kint);
  sleep_disable();
}

// void WDT_off(void){
//  __disable_interrupt();
//  __watchdog_reset();
//  /* Clear WDRF in MCUSR */
//  MCUSR &= ~(1<<WDRF);
//  /* Write logical one to WDCE and WDE */
//  /* Keep old prescaler setting to prevent unintentional time-out */
//  WDTCSR |= (1<<WDCE) | (1<<WDE);
//  /* Turn off WDT */
//  WDTCSR = 0x00;
//  __enable_interrupt();
// }
```

4.  Write a program that disables WDT. Fulfill it. Make sure WDT is really disabled by loading
    and checking the blink example.
5.  Prepare the report, upload it to moodle in pdf format.

## Help

1.  Time to familiarize yourself with the AVR libc library:
    [https://www.nongnu.org/avrlibc/usermanual/index.html](https://www.nongnu.org/avrlibc/usermanual/index.html). See Library Reference for full
    descriptions.
2.  We will need the `<avr/interrupt.h>` library for interrupt management.
    The WDT interrupt service routine is declared as follows:

```c++
ISR(WDT_vect){
  // I'm doing something, but fast
}
```

## Advice

Don't prohibit interruptions while the experience is modest. Ignore the interrupt prohibitions seen
in the examples - `cli()`.

```c++
#include <avr/wdt.h>

boolean kint = false; 

void setup()
{
  pinMode(13,OUTPUT);
  cli(); //##//disable all interrupts
  wdt_reset(); //reset the wdt timer
  /*
  WDTCSR configuration;
  WDIE = 1:Interrupt Enagle
  WDE = 1 :Reset Enable
  WDP3 = 0 :For 2000ms Time-out
  WDP2 = 1 :For 2000ms Time-out
  WDP1 = 1 :For 2000ms Time-out
  WDP0 = 1 :For 2000ms Time-out
  */
  //Enter Watchdog configuration mode:
  WDTCSR |=(1<<WDCE) | (1<<WDE);
  // Set watchdog settings:
  WDTCSR = (1<<WDIE) | (1<<WDE) | (0<WDP3) | (1<<WDP2) | (0<<WDP1) | (0<<WDP0);
  sei();
}

void loop()
{
}

ISR(WDT_vect)// Watchdog timer interrupt.
{
  WDTCSR = (1<<WDIE);
  kint = !kint;
  digitalWrite(13,kint);
  //include your code here
  //prevent reset
}
```
