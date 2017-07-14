# GardenPY
This repo is being built for our Garden Automation Project. This project will take place in 2 major phases. Phase 1 will 
implement a moisture detection system that will send the data mined from the soil to an AWS SQS queue. Data will be picked
by a Lambda and fed into AuroraDB. It will also trigger an SNS topic based on Warning and Critical thresholds. Phase 2 
will actually trigger a watering system in the garden.

### Structure
Since we currently have 3 different technologies they will be stored in sperate directories. In theory this project could
extend to Intel Edision's or other devices. Some people may choose to only use 1 device as well.
- Lambda
- Raspberry Pi
- Ardunio

### Data Flow
Soil Moisture Sensor -> Arduino -> Raspberry Pi -> SQS Queue -> AuroraDB + SNS Topic

### Hardware
- Soil Moisture Sensor: https://www.sparkfun.com/products/13322
- Arduino Pro Micro: https://www.sparkfun.com/products/12640
- Raspberry Pi 3: https://www.sparkfun.com/products/13825

### Contributing
If you would like to contibute, feel free to fork this project. If you would like to implement this on different hardware
or add additional functionality that you believe will benefit others, submit a push request. This project will be standardized
on Python outside of the Arduino code. Feel free to contact me at horan116@gmail.com.
