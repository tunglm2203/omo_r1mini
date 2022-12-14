################################################################################
# Set minimum required version of cmake, project name and compile options
################################################################################
cmake_minimum_required(VERSION 2.8.3)
project(omo_r1mini_bringup)

## Compile as C++11, supported in ROS Kinetic and newer
add_compile_options(-std=c++11)

################################################################################
# Find catkin packages and libraries for catkin and system dependencies
################################################################################
find_package(catkin REQUIRED COMPONENTS
  rospy
  sensor_msgs
  nav_msgs
  geometry_msgs
  tf
  message_generation
  #usb_cam
  #omo_r1mini_description
)

add_service_files(
  DIRECTORY srv
  FILES
  Battery.srv
  Color.srv
  SaveColor.srv
  ResetOdom.srv
  Calg.srv
  Onoff.srv
)


################################################################################
# Setup for python modules and scripts
################################################################################
catkin_python_setup()

generate_messages(
  DEPENDENCIES
  std_msgs
)

################################################################################
# Declare ROS messages, services and actions
################################################################################

################################################################################
# Declare ROS dynamic reconfigure parameters
################################################################################

################################################################################
# Declare catkin specific configuration to be passed to dependent projects
################################################################################
catkin_package(
  CATKIN_DEPENDS
  rospy
  sensor_msgs
  nav_msgs
  geometry_msgs
  tf
  usb_cam
  #omo_r1mini_description
  message_runtime
  std_msgs
)

################################################################################
# Build
################################################################################

################################################################################
# Install
################################################################################
catkin_install_python(PROGRAMS
  nodes/omo_packet_handler.py
  nodes/omo_r1mini_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

################################################################################
# Test
################################################################################
