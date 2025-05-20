Faculty of Electronics
Department of Computer Science and Communications Technologies

# Laboratory work 1

## Fundamentals of oscillograph use

Report by: Mark Mikula, IRDfu-22

## Aim of the work

To learn how to tune an oscilloscope, measure signal parameters using manual and automatic methods.

## Task

In parallel with the tasks, prepare a laboratory report. Write to the steps and notes taken. Keep the oscillograms
for illustration.

1.  Open the arduino project "Lab1". Tools->Boards select Arduino Mega. Tools-> Port select comZZ, where
    ZZ is any number but 1. Compile and load the program into arduino board.
2.  Use the calibrator to prepare the oscilloscope for operation.
3.  Connect the ground terminal of the oscilloscope to the GND pin of the EL_lab board. Oscilloscope Connect
    the signal terminal of the oscilloscope to the TP2 test point.
4.  Adjust the oscilloscope so that the generated signal is visible on the display.
    Measure this signal:
    a.  Amplitude: 5.28V
    b.  Period: 16.38ms
    c.  Frequency: 61.0565Hz
    d.  Duty cycle: +Duty[1] 62.89%, -Duty[1] 37.11%
5.  Connect the signal lead of the oscilloscope to the TP13 site. Adjust the oscilloscope settings. The
    oscilloscope shall be adjusted to ensure that the signal is clearly visible. What signal parameters have changed?
    Frequency changed to 1.91Hz, amplitude stayed the same, +Duty[1] and -Duty[1] changed to 50%.
6.  Connect the signal lead of the oscilloscope to the TP6 site. Adjust the oscilloscope so that only one pulse is
    visible on the display. Measure the rise time of this pulse.
    Rise time: 32.40ns.
7.  Use the EL_lab buttons M1 and M2 to activate the signal number assigned to you. This time a more complex
    signal will be generated and will be difficult for the oscilloscope to display. Use the image stop mode. Eight
    bits of ~19 µs duration are repeated in the signal. The spacing between the eight bits is ~220 µs. A 5 V pulse
    represents a logic unit, 0 V signal means logic 0. Decode (write {1,0}) the 8-bit message displayed on the
    screen. – `10100010`
8.  Prepare the report, upload it in pdf format to moodle.
