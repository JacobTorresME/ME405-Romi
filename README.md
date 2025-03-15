# Mechatronics II Romi Project
A MycroPython-based Romi robot porject use and STM32 board (via the 'pyb' module)

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Bill of Materials (BOM)](#bill-of-materials-bom)
- [Dependencies & Installation](#dependencies--installation)
- [State-Space Model](#state-space-model)
- [Code Descriptions](#code-descriptions)
  - [Core Files](#core-files)
  - [Task Files](#task-files)
- [Demonstration](#demonstration)
- [Contributing](#contributing)
- [License](#license)
- [Contact / Acknowledgments](#contact--acknowledgments)

---

## Overview 

In this project, a Pololu Romi chassis is outfitted with:
- An STM32-based microcontroller running MicroPython.
- A BNO055 IMU for orientation and heading data.
- Infrared sensors for line detection and surface detection.
- Bump sensors for collision detection.
- Two DC motors with encoders, driven by DRV8838 drivers.

Romi, the robot, can:
1. Follow black lines using IR sensors and a PID controller.  
2. Navigate a grid or tunnel utilizing IMU headings and encoder distance data.  
3. Detect collisions via bump sensors and respond accordingly.
