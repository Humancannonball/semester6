Faculty of Electronics
Department of Computer and Communication Technologies

# Laboratory work 8

## Ethernet Internet Module

Report by: Mark Mikula, IRDfu-22

## Work objective

Learn to transfer information from IoT objects using the Internet network.

## Task

While completing the tasks, in parallel, prepare the report of the laboratory work. Write
down the steps you take and notes.

1.  Connect the Arduino Ethernet module to the Internet network, the Arduino board to the
    computer. Open `File->Examples->Ethernet->WebClient` example. In the program, change the
    last number of the MAC address from `0xED` to your workstation number. For example: `0x01`. In the
    Arduino Ethernet module, the MAC address is assigned programmatically, and for our IoT
    network to work, we need things to have unique MAC addresses. Change the serial interface speed from
    9600 to 1000000 (line 53). Compile and upload the program to the Arduino. Open the Serial
    Monitor window:
    a.  What IP address did the Arduino get from the DHCP server? `10.21.46.28`
    b.  What is the IP address of www.google.com? `142.250.185.228`
    c.  Wait for the Arduino to disconnect from the server. What was the data transfer rate
        between the Arduino and the server? Received 123701 bytes in 3.0037s, rate is 41.18
        kbytes/second.

2.  Open `File->Examples->Ethernet->WebServer` example. Change the MAC address
    according to point 1. Change IP address to static IP: `10.21.46.100 + workplace_number`. Upload the
    program to the Arduino. Open the Serial Monitor window. Check the IP address received by the Arduino
    WEB server.
    a)  Open a WEB browser on your computer. Connect to your server. Follow what the
        Arduino is seeing in the Serial Monitor window.
    b)  Modify the Arduino program and HTML code to display the states of the three
        buttons on the WEB page. The buttons are connected to terminals A1, A2 and A3.
    c)  Spend 10 minutes designing a WEB page so that it stands out from the work of your
        colleagues.

### Enhanced WebServer Code:

```c++
#include <SPI.h>
#include <Ethernet.h>

// Enter MAC and IP address for your controller
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0x10 };
IPAddress ip(10, 21, 43, 210);

// Initialize the Ethernet server library
EthernetServer server(80);

void setup() {
  // Configure analog pins A1, A2, A3 as inputs
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);

  // Start Serial and Ethernet connection
  Serial.begin(9600);
  Ethernet.begin(mac, ip);

  if (Ethernet.hardwareStatus() == EthernetNoHardware) {
    Serial.println("Ethernet shield not found. Cannot continue.");
    while (true) delay(1);
  }

  // Start the server
  server.begin();
  Serial.print("Server is at ");
  Serial.println(Ethernet.localIP());
}

void loop() {
  EthernetClient client = server.available();
  if (client) {
    bool currentLineIsBlank = true;
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        Serial.write(c);

        if (c == '\n' && currentLineIsBlank) {
          // Send HTTP response header
          client.println("HTTP/1.1 200 OK");
          client.println("Content-Type: text/html");
          client.println("Connection: close");
          client.println("Refresh: 5"); // Auto-refresh every 5 seconds
          client.println();
          
          // HTML content
          client.println("<!DOCTYPE HTML>");
          client.println("<html>");
          client.println("<head>");
          client.println("<title>Button States</title>");
          client.println("<style>");
          client.println("body { font-family: Arial, sans-serif; text-align: center; background-color: #282c34; color: white; }");
          client.println("h1 { color: #61dafb; }");
          client.println(".status-box { display: inline-block; width: 200px; padding: 20px; margin: 10px; border-radius: 10px; font-size: 24px; font-weight: bold; }");
          client.println(".on { background-color: #4CAF50; color: white; }");
          client.println(".off { background-color: #f44336; color: white; }");
          client.println("</style>");
          client.println("</head>");
          client.println("<body>");
          client.println("<h1>Arduino Button States</h1>");
          
          // Display button states
          for (int i = A1; i <= A3; i++) {
            client.print("<div class='status-box ");
            client.print(digitalRead(i) ? "on" : "off");
            client.print("'>Button A");
            client.print(i - A0);
            client.print(": ");
            client.print(digitalRead(i) ? "ON" : "OFF");
            client.println("</div>");
          }

          client.println("</body>");
          client.println("</html>");
          break;
        }

        if (c == '\n') currentLineIsBlank = true;
        else if (c != '\r') currentLineIsBlank = false;
      }
    }
    delay(1);
    client.stop();
  }
}
```

3.  Open `File->Examples->Ethernet->ChatServer` example. Change the MAC address
    according to point 1. Change IP address to static IP: `10.21.46.100 + workstation_number`.
    Upload the program to the Arduino. Open the Serial Monitor window.
    a)  On your computer, launch a Command window. Connect to your (colleague's) Chat
        server via Telnet. Monitor the messages displayed in the Serial Monitor window. What is
        the maximum number of clients that can connect to the server?
    b)  BONUS improve the ChatServer app.

4.  Download the `web_control.ino` program from moodle. Explore how it works. Modify it so
    that 3 LEDs can be controlled from the WEB page.

### Enhanced LED Control Web Page:

```c++
#define LED1 13
#define LED2 12
#define LED3 11

#include <SPI.h>
#include <Ethernet.h>

byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0x10};
byte ip[] = {10, 21, 43, 210};
byte subnet[] = {255, 255, 255, 0};

EthernetServer server(80);
String readString;

void setup() {
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);
  digitalWrite(LED1, HIGH); // Assuming HIGH is OFF for LEDs
  digitalWrite(LED2, HIGH);
  digitalWrite(LED3, HIGH);

  Ethernet.begin(mac, ip, subnet);
  server.begin();
  Serial.begin(9600);
}

void loop() {
  EthernetClient client = server.available();
  if (client) {
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        readString += c;
        if (c == '\n') {
          Serial.print(readString);
          if (readString.indexOf('?') >= 0) { // Request contains parameters
            client.println(F("HTTP/1.1 204 No Content"));
            client.println();
          } else { // Initial request for the page
            client.println(F("HTTP/1.1 200 OK"));
            client.println(F("Content-Type: text/html"));
            client.println();
            client.println(F("<html><head><title>LED Control</title>"));
            client.println(F("<style>body { font-family: Arial; text-align: center; } .btn { padding: 10px; margin: 5px; display: inline-block; border: 1px solid #000; text-decoration: none; color: #333; background-color: #f0f0f0; border-radius: 5px;} .btn:hover { background-color: #e0e0e0; }</style></head>"));
            client.println(F("<body><h1>Control LEDs</h1>"));
            client.println(F("<a class='btn' href='/?on1'>LED1 ON</a> <a class='btn' href='/?off1'>LED1 OFF</a><br>"));
            client.println(F("<a class='btn' href='/?on2'>LED2 ON</a> <a class='btn' href='/?off2'>LED2 OFF</a><br>"));
            client.println(F("<a class='btn' href='/?on3'>LED3 ON</a> <a class='btn' href='/?off3'>LED3 OFF</a><br>"));
            client.println(F("<a class='btn' href='/?all_on'>ALL ON</a> <a class='btn' href='/?all_off'>ALL OFF</a>"));
            client.println(F("</body></html>"));
          }
          delay(1); // Give the web browser time to receive the data
          client.stop();

          // Control LEDs based on the request
          if (readString.indexOf("on1") > 0) digitalWrite(LED1, LOW); // Assuming LOW is ON
          if (readString.indexOf("off1") > 0) digitalWrite(LED1, HIGH);
          if (readString.indexOf("on2") > 0) digitalWrite(LED2, LOW);
          if (readString.indexOf("off2") > 0) digitalWrite(LED2, HIGH);
          if (readString.indexOf("on3") > 0) digitalWrite(LED3, LOW);
          if (readString.indexOf("off3") > 0) digitalWrite(LED3, HIGH);
          if (readString.indexOf("all_on") > 0) {
            digitalWrite(LED1, LOW);
            digitalWrite(LED2, LOW);
            digitalWrite(LED3, LOW);
          }
          if (readString.indexOf("all_off") > 0) {
            digitalWrite(LED1, HIGH);
            digitalWrite(LED2, HIGH);
            digitalWrite(LED3, HIGH);
          }
          readString = ""; // Clear the string for the next request
        }
      }
    }
  }
}
```

5.  Using the examples on the Internet, create a program that transmits the status of 6
    analog channels (A1-A5) to the ThingSpeak server.
6.  Prepare the report, upload it to moodle in pdf format.
