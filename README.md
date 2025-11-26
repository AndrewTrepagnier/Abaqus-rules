# Nozzle Moment Checker

Simple visualization of reaction forces and moments.

## Python Version

### Install
```bash
pip install matplotlib numpy
```

### Run
```bash
python abaqus_moment.py
```

## TCL/Tk Version

### Install
TCL/Tk usually comes pre-installed on most systems.

### Run
```bash
./abaqus_moment.tcl
# or
tclsh abaqus_moment.tcl
# or
wish abaqus_moment.tcl
```

## Usage

Enter:
- Nozzle direction (+z, -x, etc.)
- RF values (RFx, RFy, RFz) 
- RM values (RMx, RMy, RMz)

## Check

Does the moment wrap the way you expect?

Right-hand rule: Thumb = moment axis, Fingers = rotation
