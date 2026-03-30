# LightHead3000Smart+ Domain Model

Hotel &emsp; <1 --- ..\*> &emsp; Hotel room  
Hotel &emsp; <1 --- ..\*> &emsp; Public areas  
Hotel &emsp; <1 --- ..\*> &emsp; Guest  
Hotel &emsp; <1 --- ..\*> &emsp; Employee  
Hotel &emsp; <1 ---- 1> &emsp; Hotel Manager  

Hotel room &emsp; <1 ---- 1> &emsp; Operating device/touch screen  
Hotel room &emsp; <1 ---- 1> &emsp; Charging deck  
Hotel room &emsp; <1 --- ..\*> &emsp; Guest  
Hotel room &emsp; <1 --- ..\*> &emsp; Light  

Charging deck &emsp; <1 --- 1> &emsp; Hotel room  
Charging deck &emsp; < ----- > &emsp; Operating device/touch screen


Public areas &emsp; <..\* ----- ..\*> &emsp; Lights  
Public areas &emsp; <1..\* --- 1..\*> &emsp;Lightning system operating system  

Guest &emsp; <1 ---- 1> &emsp; Phone  
Guest &emsp; <..\* --- 1> &emsp; Hotel room  

Phone &emsp; <1 --- 1> &emsp; Application/Guest app  

Application/guest app &emsp; <..\* --- 1> &emsp; Operating device/touch screen  

Employee/Staff/Personnel &emsp; <1 --- 1> &emsp; SystemControl / MonitoringApp  
Hotel Manager &emsp; <1 --------------- 1> &emsp; SystemControl / MonitoringApp  

Operating device/touch screen &emsp; <1 ---- 1> &emsp; Hotel room  
Operating device/touch screen &emsp; <1 --- ..\*> &emsp; Guest  
Operating device/touch screen &emsp; <1 --- ..\*> &emsp; Light  
Operating device/touch screen &emsp; <1 --- ..\*> &emsp; Guest app  
Operating device/touch screen &emsp; <1 ---- 1> &emsp; Operating system  
Operating device/touch screen &emsp; <1 ---- 1> &emsp; Charging deck  

Operating system &emsp; <1 ----- 1> &emsp; Operating device  
Operating system &emsp; <1 --- 1..\*> &emsp; Operating system language  

Light &emsp; <1..\* --- 1> &emsp; Operating device/touch screen  
Light &emsp; <1 ---- ..\*> &emsp; Light status
