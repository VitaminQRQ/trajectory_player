cmake_minimum_required(VERSION 3.0.2)
project(trajectory_player)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  geometry_msgs
  gazebo_ros
)

catkin_package(
  CATKIN_DEPENDS rospy std_msgs geometry_msgs gazebo_ros
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

catkin_install_python(PROGRAMS
  scripts/trajectory_player.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)