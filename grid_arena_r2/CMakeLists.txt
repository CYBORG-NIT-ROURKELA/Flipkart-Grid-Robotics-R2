cmake_minimum_required(VERSION 3.0.2)
project(grid_arena_r2)


find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  message_generation
)
add_service_files(
  FILES
  twist.srv
)
catkin_package(
  CATKIN_DEPENDS
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)
