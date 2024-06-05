import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import TeleportAbsolute, TeleportRelative
import termios, sys, os
from numpy import pi

TERMIOS = termios

def callback(msg):
    rospy.loginfo(msg.x)

def getkey():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
    new[6][TERMIOS.VMIN] = 1
    new[6][TERMIOS.VTIME] = 0
    termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
    c = None
    try:
        c = os.read(fd, 1)
    finally:
        termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
    return c.decode('utf-8')

def move():

    rospy.init_node('robot_cleaner', anonymous = True)
    rate = rospy.Rate(10)

    vel_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size = 10)
    rel_ser = rospy.ServiceProxy('/turtle1/teleport_relative', TeleportRelative)
    abs_ser = rospy.ServiceProxy('/turtle1/teleport_absolute', TeleportAbsolute)

    vel_mes = Twist()

    while not rospy.is_shutdown():

        vel_mes.linear.x = 0
        vel_mes.linear.y = 0
        vel_mes.linear.z = 0
        vel_mes.angular.x = 0
        vel_mes.angular.y = 0
        vel_mes.angular.z = 0

        key = getkey().lower()

        if key == 'w':
            vel_mes.linear.x = 1
        elif key == 's':
            vel_mes.linear.x = -1
        elif key == 'a':
            vel_mes.angular.z = pi*5/180  
        elif key == 'd':
            vel_mes.angular.z = -pi*5/180
        elif key == ' ':
            rel_ser(0, pi)
        elif key == 'r':
            abs_ser(5.54, 5.54, 0)
        else:
            vel_mes.angular.z = 0

        vel_pub.publish(vel_mes)
        rate.sleep()

def main():
    if __name__ == '__main__':
        try:
            move()
        except rospy.ROSInterruptException: pass

main()