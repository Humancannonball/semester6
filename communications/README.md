# Communication Labs

This folder contains networking and communication systems laboratory work completed during Semester 6.

## Lab Work Overview

### Lab Work #3: Cisco router and basic LAN configuration
- Screenshots from real hardware: [./lab3/](./lab3/)
- Screenshots from Cisco Packet Tracer: [./lab3_sim/](./lab3_sim/)

### Lab Work #4: Cisco switch configuration and MAC-IP addressing
- Screenshots from real hardware: [./lab4/](./lab4/)
- Screenshots from Cisco Packet Tracer: [./lab4_sim/](./lab4_sim/)

### Lab Work #5: VLAN networking
- Screenshots from real hardware: [./lab5/](./lab5/)
- Screenshots from Cisco Packet Tracer: [./lab5_sim/](./lab5_sim/)

### Lab Work #6: Internet and NAT operation
- Screenshots from real hardware: [./lab6/](./lab6/)
- Screenshots from Cisco Packet Tracer: [./lab6_sim/](./lab6_sim/)

### Lab Work #7: Radio link modelling in ArcGIS
- Screenshots and documentation: [./lab7/](./lab7/)

### Lab Work #8: Modelling 4G Mobile Coverage with ArcGIS
- Screenshots and documentation: [./lab8/](./lab8/)

## Folder Structure

- **export/**: Contains DOCX and PDF files
- **labX/**: Contains screenshots from real hardware implementations
- **labX_sim/**: Contains screenshots from Cisco Packet Tracer simulations (not needed in reports)
- **main.py**: Python script that creates PDF files from screenshot folders

## Setup

Create a virtual environment and install required packages:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install Pillow reportlab
```

## Usage

Run `main.py` to automatically generate PDF files from the lab screenshot folders:

```bash
python main.py
```

This will process lab3, lab4, lab5, and lab6 folders and create corresponding PDF files with screenshots from real hardware.
