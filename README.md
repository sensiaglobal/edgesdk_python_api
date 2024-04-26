# SDK for HCC2 in python

This packages provides the required interface between an application and HCC2 data using HCC2 modbus server as the data source.

This package must be installed alon with the application:

### Build

To build a new version of this package:
```
./build.sh
```
The output of this build is the dist/ folder.

### Notes

1. We recommend not to change this code. 
2. Should you need to build a new version, you must then copy it into the applications that needs it.
3. Package installation into the application:
```
pip install dist/hcc2sdk-X.X.X-py3-none-any.whl --force-reinstall  
```
(X.X.X is the package version number)
