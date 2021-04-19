#!/usr/bin/env python
import rospy
from geometry_msgs.msg  import Twist,PoseStamped
from math import pow,atan2,sqrt
from nav_msgs.msg import Odometry
import tf

class turtlebot():

    def __init__(self):
        #Creating our node,publisher and subscriber
        rospy.init_node('turtlebot_controller', anonymous=True)
        self.velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.pose_subscriber = rospy.Subscriber('/odom_h', Odometry, self.pose_callback)
        self.goal_sub = rospy.Subscriber("/2dgoal",PoseStamped,self.goal_callback)
        self.goal = PoseStamped()
        self.goal_last = PoseStamped()
        self.odom = Odometry()
        rospy.spin()

    #Callback function implementing the pose value received
    def pose_callback(self, data):
        self.odom = data

    def goal_callback(self,data):
        self.goal_last = self.goal
        self.goal_last.header = data.header
        self.goal = data
        self.move2goal()

    def get_distance(self, goal_x, goal_y):
        distance = sqrt(pow((goal_x - self.odom.pose.pose.position.x), 2) + pow((goal_y - self.odom.pose.pose.position.y), 2))
        return distance

    def move2goal(self):
        goal_pose_x = self.goal.pose.position.x
        goal_pose_y = self.goal.pose.position.y
        quaternion = (self.odom.pose.pose.orientation.x,self.odom.pose.pose.orientation.y,self.odom.pose.pose.orientation.z,self.odom.pose.pose.orientation.w)
        euler = tf.transformations.euler_from_quaternion(quaternion)        
        pose_theta = euler[2]
        distance_tolerance = 0.3
        angle_tolerance = 0.3
        vel_msg = Twist()
        #Porportional Controller
        #linear velocity in the x-axis:
        distance_error = sqrt(pow((goal_pose_x - self.odom.pose.pose.position.x), 2) + pow((goal_pose_y - self.odom.pose.pose.position.y), 2))
        vel_msg.linear.x = 0.5 * distance_error
        vel_msg.linear.y = 0
        vel_msg.linear.z = 0

        angle_error = atan2(goal_pose_y - self.odom.pose.pose.position.y, goal_pose_x - self.odom.pose.pose.position.x) - pose_theta
        #angular velocity in the z-axis:
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z = 0.5 * angle_error

        print("distance ",distance_error)
        print("angleError ",angle_error)



        #Stopping our robot after the movement is over
        if distance_error < distance_tolerance:
           vel_msg.linear.x = 0
           if self.goal_last.pose.position != self.goal.pose.position:
              vel_msg.angular.z = 0

        self.velocity_publisher.publish(vel_msg)

        

if __name__ == '__main__':
    try:
        #Testing our function
        x = turtlebot()

    except rospy.ROSInterruptException: pass
