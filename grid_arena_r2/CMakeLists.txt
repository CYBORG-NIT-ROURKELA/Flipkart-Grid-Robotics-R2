cmake_minimum_required(VERSION 3.0.2)
project(grid_arena_r2)


find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  actionlib_msgs
  message_generation
)

add_message_files(
  FILES
  rpm.msg
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
  CATKIN_DEPENDS message_runtime
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)
