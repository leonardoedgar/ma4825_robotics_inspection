# ma4825_robotics_inspection
![Actions Status](https://github.com/leonardoedgar/ma4825_robotics_inspection/workflows/Continuous%20Integration%20(CI)/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/leonardoedgar/ma4825_robotics_inspection/badge.svg?branch=master&service=github)](https://coveralls.io/github/leonardoedgar/ma4825_robotics_inspection?branch=master)


NTU MA4825 Robotics Project AY20/21
* Perform object classification to distinguish defected and non-defected objects 

Owner: Leonardo Edgar (leonardo_edgar98@outlook.com)

## Table of Contents

   1. [Getting started](#1-getting-started)
   2. [Prerequisites](#2-prerequisites)
   3. [Installing](#3-installing)
   4. [System characteristics](#4-system-characteristics)


## 1. Getting started

Welcome to **MA4825 Robotics Inspection** project! There are just a few steps to get you started with developing!

## 2. Prerequisites

1. Compute
    * Any computer
2. Camera
    * Universal Video Camera (USBA 2.0 or USBA 3.0 interface)


## 3. Installing

* To build development docker images
```bash
cd dockerfiles
docker-compose -f docker-compose-dev.yaml build
```

## 4. System characteristics

* Object classification
    * With resolution: 1280px by 960px
    	* FOVx (Horizontal Field of View) = 49.81°
    	* FOVy (Vertical Field of View) = 38.22°
