Table of Contents

[Summary of Steps [2](#summary-of-steps)](#summary-of-steps)

[Work Steps [2](#_Toc196480243)](#_Toc196480243)

[Signal Coverage Optimisation Exercise
[7](#signal-coverage-optimisation-exercise)](#signal-coverage-optimisation-exercise)

[Conclusion [9](#conclusion)](#conclusion)

# Summary of Steps

This lab involved modeling 4G mobile coverage using ArcGIS. Key steps included:
1.  Opening a previous project to utilize an existing working environment.
2.  Setting a Base Station (BS) point on a chosen building (Vilnius University main building).
3.  Configuring antenna azimuths for three cells to cover 360 degrees.
4.  Running a Coverage Prediction simulation.
5.  Analyzing simulation data and removing unnecessary layers to focus on signal strength.
6.  Adjusting display settings to hide signals stronger than -85dBm for clearer analysis of weaker areas. (Assuming dB is dBm for signal strength)
7.  Measuring signal propagation distance and quality.
8.  Optimizing coverage by adding a second BS in an area with poor signal from the first BS.
9.  Repeating the coverage prediction and analysis for the two-BS scenario.

[]{#_Toc196480243 .anchor}Work Steps

Initially, the Lab 7 project was opened to reuse the existing working environment. A Base Station point was set on the main building of Vilnius University.

Next, cell azimuths were configured. The first cell's azimuth was set, then two more cells were created and their azimuths adjusted to ensure 360-degree coverage around the Base Station.

After antenna configuration, a Coverage Prediction was run to assess the chosen antenna location.

The simulation data was then analyzed. Unnecessary layers were removed to visualize only signal strength, highlighting areas with good and poor coverage.

For more precise analysis, color marking for signals stronger than -85dBm was disabled.

Signal propagation distance and quality were also measured.

The initial coverage was considered suboptimal and intermittent, possibly due to the antenna not being raised 2 meters above the building's roof.

# Signal Coverage Optimisation Exercise

To optimize coverage, the existing antenna setup was copied and cloned to a new location in a private residential area near the university, where the first antenna's signal was weak.

The Coverage Prediction process and layer adjustments were repeated for the two-BS scenario.

The addition of the second antenna significantly improved coverage in the residential area, which the first antenna alone could not adequately cover. A comparison was made between the single BS and dual BS coverage.

# Conclusion

This laboratory work enhanced understanding of ArcGIS and provided a clear insight into cell tower installation planning, including how various factors affect coverage. This experience is valuable for a telecommunications specialist.
