cmake_minimum_required(VERSION 3.0.2)
project(grid_arena_r2)


find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  actionlib_msgs
)

add_action_files(
  DIRECTORY action
  FILES bot.action
)

generate_messages(
  DEPENDENCIES actionlib_msgs std_msgs  # Or other packages containing msgs
)

catkin_package(
  CATKIN_DEPENDS actionlib_msgs
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)
