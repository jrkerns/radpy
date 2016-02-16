# Introduction #

RadPy uses the BDML format to save and load beam data files.  The structure of the BDML format is given below.  The root element is named BDML and consists of a sequence of one or more Beam elements.  Each Beam element has three children: MeasurementDetails, BeamDetails and Data.  Subelements for these are shown below.

This outline also gives the data structure of a beam object in RadPy.  For example, to get the MeasuredDateTime value, you would reference "Beam.MeasurementDetails.MeasuredDateTime".


# Beam #

### MeasurementDetails ###

  * MeasuringDevice
    * Model
    * Type
    * Manufacturer
  * Isocenter
    * x
    * y
    * z
  * CoordinateAxes
    * Inplane
    * Crossplane
    * Depth
  * MeasuredDateTime
  * ModificationHistory
  * StartPosition
    * x
    * y
    * z
  * StopPosition
    * x
    * y
    * z
  * Physicist
    * EmailAddress
    * Telephone
    * Name
    * Institution
  * Medium
  * Servo
    * Model
    * Vendor
  * Electrometer
    * Model
    * Vendor
    * Voltage

### BeamDetails ###

  * Energy
  * Particle
  * SAD
  * SSD
  * CollimatorAngle
  * GantryAngle
  * CrossplaneJawPositions
    * NegativeJaw
    * PositiveJaw
  * InplaneJawPositions
    * NegativeJaw
    * PositiveJaw
  * Wedge
    * Angle
    * Type
  * Applicator
  * Accessory
  * RadiationDevice
    * Vendor
    * Model
    * SerialNumber
    * MachineScale

### Data ###

  * Abscissa
    * Value
    * Value
    * ...
  * Ordinate
    * Value
    * Value
    * ...
  * Quantity