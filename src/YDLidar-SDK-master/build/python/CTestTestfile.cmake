# CMake generated Testfile for 
# Source directory: /home/yahboom/YDLidar-SDK-master/python
# Build directory: /home/yahboom/YDLidar-SDK-master/build/python
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(ydlidar_py_test "/usr/bin/python" "/home/yahboom/YDLidar-SDK-master/python/test/pytest.py")
set_tests_properties(ydlidar_py_test PROPERTIES  ENVIRONMENT "PYTHONPATH=/opt/ros/melodic/lib/python2.7/dist-packages:/home/yahboom/YDLidar-SDK-master/build/python")
subdirs("examples")
