Faculty of Electronics
Department of Computer and Communication Technologies

# Laboratory work 10

## I2C bus and EEPROM 24C04

Report by: Mark Mikula, IRDfu-22

## Work objective

Learn to use I2C bus and write data to EEPROM 24C04.

## Basics

The I2C bus is a widely used communication protocol in the embedded systems and microcontrollers
industry. I2C stands for Inter-Integrated Circuit, which was developed by Philips Semiconductors (now NXP
Semiconductors) in the early 1980s. It is a two-wire bus that uses a clock signal and a data signal to
communicate between devices. In this text, we will explore the basics of the I2C bus, timing diagrams, writing,
and reading data from the bus. The I2C bus is a simple and efficient communication protocol that can be used
to connect multiple devices on the same bus. It consists of two lines: SDA (Serial Data Line) and SCL (Serial
Clock Line). The SDA line is bidirectional, allowing for data transmission in both directions, while the SCL line
is unidirectional, providing a clock signal for synchronizing data transfer. The I2C bus operates in two modes:
master mode and slave mode. In master mode, the device initiates the communication and generates the
clock signal. In slave mode, the device waits for the master device to initiate communication and responds
accordingly. The I2C bus supports multiple masters and multiple slaves on the same bus, allowing for a
flexible and scalable system design. The bus also supports hot-plugging, which allows devices to be added or
removed from the bus while the system is running.

Messages are broken up into two types of frame: an address frame, where the controller indicates
the peripheral to which the message is being sent, and one or more data frames, which are 8-bit data
messages passed from controller to peripheral or vice versa. Data is placed on the SDA line after SCL goes
low, and is sampled after the SCL line goes high. The time between clock edge and data read/write is defined
by the devices on the bus and will vary from chip to chip.

### Start Condition

To initiate the address frame, the controller device leaves SCL high and pulls SDA low. This puts all
peripheral devices on notice that a transmission is about to start. If two controllers wish to take ownership
of the bus at one time, whichever device pulls SDA low first wins the race and gains control of the bus. It is
possible to issue repeated starts, initiating a new communication sequence without relinquishing control of
the bus to other controller(s).

### Address Frame

The address frame is always first in any new communication sequence. For a 7-bit address, the
address is clocked out most significant bit (MSB) first, followed by a R/W bit indicating whether this is a read
(1) or write (0) operation. The 9th bit of the frame is the NACK/ACK bit. This is the case for all frames (data
or address). Once the first 8 bits of the frame are sent, the receiving device is given control over SDA. If the
receiving device does not pull the SDA line low before the 9th clock pulse, it can be inferred that the receiving
device either did not receive the data or did not know how to parse the message. In that case, the exchange
halts, and it's up to the controller of the system to decide how to proceed.

### Data Frames

After the address frame has been sent, data can begin being transmitted. The controller will simply
continue generating clock pulses at a regular interval, and the data will be placed on SDA by either the
controller or the peripheral, depending on whether the R/W bit indicated a read or write operation. The
number of data frames is arbitrary, and most peripheral devices will auto-increment the internal register,
meaning that subsequent reads or writes will come from the next register in line.

### Stop condition

Once all the data frames have been sent, the controller will generate a stop condition. Stop
conditions are defined by a 0->1 (low to high) transition on SDA after a 0->1 transition on SCL, with SCL
remaining high. During normal data writing operation, the value on SDA should not change when SCL is high,
to avoid false stop conditions.

### Writing Data to the I2C Bus

To write data to the I2C bus, the master device must first initiate communication by sending a start condition.
After the start condition, the master device must send the address of the slave device it wants to
communicate with, followed by a write bit. Once the address and write bit have been sent, the master device
can send the data it wants to write to the slave device. The data is transmitted in eight-bit packets, and each
packet is acknowledged by the slave device by pulling the SDA line low during the ninth clock cycle. After all
the data has been transmitted, the master device sends a stop condition to end the communication. The
slave device can then process the data it has received and respond accordingly.

### Reading Data from the I2C Bus

To read data from the I2C bus, the master device must first initiate communication by sending a start
condition. After the start condition, the master device must send the address of the slave device it wants to
communicate with, followed by a read bit. Once the address and read bit have been sent, the slave device
can send the data the master device wants

## EEPROM

EEPROM, or Electrically Erasable Programmable Read-Only Memory, is a non-volatile memory that
can store data even when power is removed. The 24C04 is a popular EEPROM chip from Microchip that has
a capacity of 4 kilobits, or 512 bytes, and uses the I2C bus for communication. The memory is divided into
four blocks, each consisting of 128 bytes. Each block has its own unique address range, which allows for easy
access to specific parts of the memory. The device address is a 7-bit value that is used to identify the chip on
the I2C bus. The device address is composed of a 4-bit fixed value (1010) followed by a 3-bit value that is
determined by the states of the A0, A1, and A2 pins.

In the case of the 24C04 IC, the device address can be set to any value between 0x50 and 0x57,
depending on the states of the A0, A1, and A2 pins. For example, if all three address pins are connected to
GND, the device address will be 0x50. If A0 is connected to VCC and A1 and A2 are connected to GND, the
device address will be 0x52.

It is important to note that the 24C04 EEPROM chip has a limited number of write cycles. The
datasheet specifies that the chip can withstand a minimum of 1 million write cycles per byte. It is therefore
important to carefully manage the usage of the chip to avoid premature wear.

## Tasks

1.  Download arduino program example from moodle. Run the program, and make sure that the data
    is written and read successfully.
2.  Modify the program so that a byte of data is only written to the EEPROM memory once every 1s.
3.  Prepare the oscilloscope for monitoring the I2C bus.
    *   Connect each of the bus signals (SCLK, SDA) to one of the oscilloscope channels. Connect the
        ground potential to one of the probes’ ground clip.
    *   Press BUS key (B)
    *   Press BUS from the bottom menu and choose I2C from side menu.
    *   Press DEFINE inputs from the bottom menu. From the side menu choose the SCLK input CH1
        and SDA input CH2.
    *   Press THRESHOLD. From the side menu select SDA and Threshold set to TTL 1.4 V, select SDA
        and set Threshold to TTL 1.4 V
4.  Connect the oscilloscope to test points TP3 and TP4. Use the SINGLE button to observe the
    transmission timing diagram. Do you notice Start, stop and ACK conditions? Save/take a picture.
5.  Modify the program so that the data byte is only read 1 time per second. Observe the transmission
    timing diagram. Do you notice the difference? Save/take a picture.
6.  Modify the program to fill all memory with the generated data.
7.  Modify the program to read all bytes of memory and output to the serial interface.

## Photos

![Lab 10 Photo 1](photos/lab10.1.png)
![Lab 10 Photo 2](photos/lab10.2.png)
![Lab 10 Photo 3](photos/lab10.3.png)
![Lab 10 Photo 4](photos/lab10.4.png)
