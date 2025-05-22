Table of Contents

[Summary of Steps [2](#summary-of-steps)](#summary-of-steps)

[Work Steps [2](#work-steps)](#work-steps)

[Theoretical Part [10](#theoretical-part)](#theoretical-part)

[Conclusion [10](#conclusion)](#conclusion)

# Summary of Steps

This lab focused on modeling a radio link using ArcGIS and Cellular Expert. The main steps were:
1.  Registering in ArcGIS and creating a new project.
2.  Creating a new map and saving project settings.
3.  Activating the Cellular Expert Core Module license.
4.  Creating a new virtual environment for the project.
5.  Familiarizing with map utilities and management in 2D and 3D views.
6.  Creating a Microwave Point-to-Point Link between two chosen locations (Ozas shopping mall and a residential building).
7.  Analyzing the signal path and adjusting antenna heights (5 meters above rooflines) to ensure a clear line of sight and avoid interference.
8.  Understanding and documenting theoretical concepts: Fresnel Zone, Fading Margin, and Link Budget.

# Work Steps

First, registration in the ArcGIS application and project creation were completed. A new map was created, and these settings were saved in the Project folder.

If not done earlier, the license was activated. The Cellular Expert Core Module was selected, and the activation key from the provided Excel file was used.

After license activation, a new virtual environment was created.

Once the virtual environment setup was finished, map utilities were explored in both 2D and 3D views.

After setting up the 2D and 3D maps, a Microwave Point-to-Point Link was created. Ozas shopping mall was chosen as the first point, and a residential building one kilometer away as the second point.

The signal path between these two points was analyzed. Antenna heights were raised 5 meters above the roofline of each building, within urban antenna height limits, to ensure clear transmission without interference.

# Theoretical Part

**Fresnel Zone:**\
The Fresnel zone is an elliptical region around the line-of-sight path between a transmitter and receiver. Radio waves reflecting or diffracting within this zone can cause interference, even with a clear visual path. To maintain signal integrity, at least 60% of the first Fresnel zone should be unobstructed. The zone is widest at its midpoint and narrowest near the antennas. Urban environments, with more obstructions like buildings and trees, typically increase signal loss.

**Fading Margin:**\
Fading margin is extra signal strength incorporated into a wireless link design to compensate for unpredictable signal degradation (fading). Fading can be caused by weather, interference, multipath propagation, or obstacles. This margin ensures the received signal remains above the receiver's minimum threshold. Measured in decibels (dB), it varies by environment; urban areas usually require a higher fading margin due to more frequent interference.

**Link Budget:**\
A link budget is a comprehensive accounting of all gains and losses a signal encounters from the transmitter to the receiver. It includes transmitter power, antenna gains, cable losses, free-space path loss, environmental interference, and the fading margin. The objective is to ensure the received signal strength is sufficient for reliable decoding. In dense urban areas, overcoming signal degradation might require strategies like higher antennas or repeaters. A well-calculated link budget ensures consistent communication performance.

# Conclusion

This lab involved planning a radiocommunication network using Cellular Expert with GIS data. A high-capacity microwave link was established between two locations, requiring analysis of terrain, obstacles, and line-of-sight. A relay point on a TV tower was used to bypass a forested hill, emphasizing Fresnel zone clearance. Students practiced setting endpoints, adjusting antenna heights, analyzing link budgets, and simulating signal strength. The lab demonstrated that reliable links are achievable with careful planning, although meeting fade margin targets can sometimes be a budgetary rather than a purely technical challenge.
