#!/usr/bin/env python

import rospy
from gazebo_msgs.msg import LinkStates
from geometry_msgs.msg import PoseStamped

class GazeboLinkPose:
  link_name = ''
  link_pose = PoseStamped()
  def __init__(self, link_name):
    self.link_name = link_name
    self.link_name_rectified = link_name.replace("::", "_")

    if not self.link_name:
      raise ValueError("'link_name' is an empty string")

    self.states_sub = rospy.Subscriber("/gazebo/link_states", LinkStates, self.callback)
    self.pose_pub = rospy.Publisher("/gazebo/" + self.link_name_rectified, PoseStamped, queue_size = 10)

  def callback(self, data):
    try:
      ind = data.name.index(self.link_name)
      self.link_pose.pose = data.pose[ind]
      self.link_pose.header.frame_id = "world"
    except ValueError:
      pass

if __name__ == '__main__':
  try:
    rospy.init_node('gazebo_link_pose', anonymous=True)
    gp = GazeboLinkPose(rospy.get_param('~link_name'))
    publish_rate = rospy.get_param('~publish_rate', 10)

    rate = rospy.Rate(publish_rate)
    while not rospy.is_shutdown():
      gp.pose_pub.publish(gp.link_pose)
      rate.sleep()

  except rospy.ROSInterruptException:
    pass