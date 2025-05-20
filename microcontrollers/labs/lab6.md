Faculty of Electronics
Department of Computer Science and Communications Technologies

# Laboratory work 6

## Digitalization of analog signals

Report by: Mark Mikula, IRDfu-22

## Work objective

Learn how to use an ADC converter.

## Theoretical part

Often, the output signal of the sensors is analog, i.e. its voltage value is proportional to the
measured parameter. For example, a TMP36 temperature sensor output voltage change of 0.01V
corresponds to one degree, and a voltage of 0.75V corresponds to +25°C. With this sensor, we
can measure temperatures from -40°C to 125°C.

The `analogRead()` function returns a result between 0 and 1023. By default, the Arduino
reference voltage takes the supply voltage t. i.e. 5 V. In this case, ADC value 0 means 0 V, and 1023
corresponds to 5 V. Now all that remains is to convert the ADC value to voltage: `float U=ADC/1023*5.0;`. The
variable `U` is of type `float` because the voltage can be any real number. Since `analogRead()`
returns a result of type `int`, the right-hand side requires at least one member of the expression whose
precision is of type `float`. Otherwise, the result `U` will still be of type `int`. Now that we have the
measured voltage, we can convert it to a temperature or other parameter.

A large number of sensors change their resistance in proportion to the measured parameter
(temperature, humidity, lighting and others). Such sensors are connected according to Fig. 2.
the diagram shown. This circuit is called a resistive voltage divider (sometimes a resistance divider).
The output voltage Uout will be proportional to the sensor resistance Rj.

PHOTO and THERMO sensors are enabled according to Fig. 2b. scheme. Thus, the ADC value
obtained with the `analogRead()` function must be converted to the Uout voltage, and the Uout
voltage must be converted to the Rj value, and finally the Rj value must be converted to the
measured parameter. To make life even more interesting, Rj is usually inversely proportional to
the measured quantity and varies logarithmically.

Although the initial sensor signal is analog, a significant number of sensors can output the signal in
digital form. One such sensor is the Dallas DS18B20 temperature sensor. Its measured
temperature range is from -55°C to +125°C. Resolution up to 12 bit i.e. the result is given in 0.0625 °C intervals.
The absolute error is 0.5 °C and does not require calibration. The sensor uses a 1-wire interface for
information exchange.

## Task

Write down the steps you take and notes.

1.  On the EL_lab board, a DS18B20 temperature sensor is connected to the A7 output. This
    sensor uses a DIGITAL 1-wire interface. So, pin A7 will be used in GPIO mode. In the Arduino
    IDE, find the library management tool (Tools -> Manage Libraries) and check if the library
    supporting the DS18B20 sensor is installed (if not, install it).
2.  Using the examples, create a program to read the sensor ID code and temperature.
    Change sensor ASK resolution (9, 10, 11 and 12 bits). Use the `millis()` function. Check how the
    result given by the sensor changes and the time required to obtain this result. Download the
    datasheet of the DS18B20 sensor and compare your results with those declared by the
    manufacturer.

### Code

```c++
#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS A7
#define TEMPERATURE_PRECISION 9

// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(ONE_WIRE_BUS);
// Pass our oneWire reference to Dallas Temperature.
DallasTemperature sensors(&oneWire);

int numberOfDevices;
DeviceAddress tempDeviceAddress; // We'll use this variable to store a found device address

void setup(void){
  Serial.begin(9600);
  Serial.println("Dallas Temperature IC Control Library Demo");
  sensors.begin();
  numberOfDevices = sensors.getDeviceCount();
  // locate devices on the bus
  Serial.print("Locating devices...");
  Serial.print("Found ");
  Serial.print(numberOfDevices, DEC);
  Serial.println(" devices.");
  Serial.print("Parasite power is: ");
  if (sensors.isParasitePowerMode()) Serial.println("ON");
  else Serial.println("OFF");

  for (int i = 0; i < numberOfDevices; i++)
  {
    if (sensors.getAddress(tempDeviceAddress, i))
    {
      Serial.print("Found device ");
      Serial.print(i, DEC);
      Serial.print(" with address: ");
      printAddress(tempDeviceAddress);
      Serial.println();
      Serial.print("Setting resolution to ");
      Serial.println(TEMPERATURE_PRECISION, DEC);
      sensors.setResolution(tempDeviceAddress, TEMPERATURE_PRECISION);
      Serial.print("Resolution actually set to: ");
      Serial.print(sensors.getResolution(tempDeviceAddress), DEC);
      Serial.println();
    } else {
      Serial.print("Found ghost device at ");
      Serial.print(i, DEC);
      Serial.print(" but could not detect address. Check power and cabling");
    }
  }
}

void printTemperature(DeviceAddress deviceAddress)
{
  // method 1 – is slower
  //Serial.print("Temp C: ");
  //Serial.print(sensors.getTempC(deviceAddress));
  //Serial.print(" Temp F: ");
  //Serial.print(sensors.getTempF(deviceAddress)); // Makes a second call to getTempC and then converts to Fahrenheit

  // method 2 – is faster
  float tempC = sensors.getTempC(deviceAddress);
  if (tempC == DEVICE_DISCONNECTED_C)
  {
    Serial.println("Error: Could not read temperature data");
    return;
  }
  Serial.print("Temp C: ");
  Serial.print(tempC);
  Serial.print(" Temp F: ");
  Serial.println(DallasTemperature::toFahrenheit(tempC)); // Converts tempC to Fahrenheit
}

void loop(void)
{
  Serial.print("Requesting temperatures...");
  sensors.requestTemperatures(); // Send the command to get temperatures
  Serial.println("DONE");
  // Loop through each device, print out temperature data
  for (int i = 0; i < numberOfDevices; i++)
  {
    if (sensors.getAddress(tempDeviceAddress, i))
    {
      // Output the device ID
      Serial.print("Temperature for device: ");
      Serial.println(i, DEC);
      printTemperature(tempDeviceAddress); // Use a simple function to print out the data
    }
  }
}

// function to print a device address
void printAddress(DeviceAddress deviceAddress)
{
  for (uint8_t i = 0; i < 8; i++)
  {
    if (deviceAddress[i] < 16) Serial.print("0");
    Serial.print(deviceAddress[i], HEX);
  }
}
```

3.  Two analog sensors are soldered on the EL_lab board. The light intensity sensor
    (photoresistor) is connected to the A0 terminal. A temperature sensor (thermistor) is
    connected to the A1 terminal. Create a program that reads the sensor signals and outputs
    their values to the Arduino terminal once per second.

### Code

```c++
const int LIGHT_SENSOR_PIN = A0;
const int TEMP_SENSOR_PIN = A1;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
}

void loop() {
  // Read analog values from sensors
  int lightValue = analogRead(LIGHT_SENSOR_PIN);
  int tempValue = analogRead(TEMP_SENSOR_PIN);

  float lightIntensity = map(lightValue, 0, 1023, 0, 100);
  float temperature = map(tempValue, 0, 1023, 0, 100);

  Serial.print("Light Intensity: ");
  Serial.print(lightIntensity);
  Serial.println("%");
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println("°C");
  delay(1000);
}
```

4.  Speed up the output of sensor signal values up to 5 times per second. Enable the Serial
    plotter window (Tools->Serial Plotter). Cover the light sensor (PHOTO) with your hand.
    Monitor signal changes. Record the amplitude values (in ADC units and volts) corresponding
    to the lighted and darkened sensor.

### Code

```c++
const int LIGHT_SENSOR_PIN = A0;
const int TEMP_SENSOR_PIN = A1;
const int LED_PIN = 9; // Define the LED pin

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT); // Set LED pin as output
}

void loop() {
  // Read analog values from sensors
  int lightValue = analogRead(LIGHT_SENSOR_PIN);
  int tempValue = analogRead(TEMP_SENSOR_PIN);

  // Convert analog values to actual sensor readings
  float lightIntensity = map(lightValue, 0, 1023, 0, 100);
  float temperature = map(tempValue, 0, 1023, 0, 100);

  // Control LED brightness based on light level
  analogWrite(LED_PIN, map(lightValue, 0, 1023, 0, 255));

  // Output to serial monitor
  Serial.print("Light Intensity: ");
  Serial.print(lightIntensity);
  Serial.print("% (ADC: ");
  Serial.print(lightValue);
  Serial.print(", Volts: ");
  Serial.print(lightValue * (5.0 / 1023.0));
  Serial.println("V)");
  
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println("°C");

  // For serial plotter
  Serial.print(lightIntensity);
  Serial.print(",");
  Serial.println(temperature);

  // Delay to allow Serial communication
  delay(200); // 200 milliseconds = 5 times per second
}
```
