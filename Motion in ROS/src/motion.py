#!/usr/bin/python3

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time

def pose_call_back(pose_message):
    global x
    global y,yaw
    x = pose_message.x
    y = pose_message.y
    yaw = pose_message.theta


def move(velocity_publisher, speed, distance, is_forward):
    velocity_message = Twist()

    global x,y
    x0 = x
    y0 = y

    if (is_forward):
        velocity_message.linear.x = abs(speed)
    else:
        velocity_message.linear.y = -abs(speed)

    distance_moved = 0.0
    loop_rate = rospy.Rate(10)

    while True:
        rospy.loginfo("Turtlesim moves forwards")
        velocity_publisher.publish(velocity_message)
        loop_rate.sleep()
        distance_moved = abs(math.sqrt(((x-x0)**2)+((y-y0)**2)))
        print(distance_moved)
        if (distance_moved>distance):
            rospy.loginfo("reached")
            break

    velocity_message.linear.x = 0
    velocity_publisher.publish(velocity_message)

if __name__=='__main__':
    try:
        rospy.init_node('tutlesim_motion_pose', anonymous=True)

        cmd_vel_topic = '/turtle1/cmd_vel'
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

        position_topic = 'turtle1/pose'
        pose_subscriber = rospy.Subscriber(position_topic, Pose, pose_call_back)
        time.sleep(2)

        move(velocity_publisher, -1.0, 2.0, False)
    
    except rospy.ROSInterruptException:
        pass
