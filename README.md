# pyzemax
Python wrapper to make macros and read data


### Usage
NSC is a simple object to hold, write, execute zpl macros

Objects (NSCObject, NSCDetector, NSCSource) are stored in an internal list

Easiest way to initialize objects are by adding to the list

obj = NSCObject(objtype, position, parameters=[], properties=[])

where position is the position (x,y,z,angle0,angle1,angle2), 
parameters and properties are tuples of key,value pairs. A list of parameter/property codes can be found
[here](https://osphotonics.wordpress.com/2015/05/07/zemax-programming-language-3-10-non-sequential-components/).

Check available types via macro.types().

After adding objects in the system initialization can be done by 
macro.clear() #clear the macro
macro.initialize_objects() #export all objects to macro
macro.update() #macro line UPDATE ALL updates all added objects

### Measurement
if a detector is added, a measurment can be done by:

macro.clear_detectors()
macro.nstr()
macro.savedetector(index, "export.ddr")

index can also be automatically determined via macro.object_index(NSCDetector)[0] (index of first detector)






