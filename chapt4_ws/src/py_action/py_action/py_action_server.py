import time
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node

from interfaces_demo.action import Progress

class ProgressActionServer(Node):

    def __init__(self):
        super().__init__('progress_action_server')
        self._action_server = ActionServer(
            self,
            Progress,
            'get_sum',
            self.execute_callback)
        self.get_logger().info('动作服务已启动')

    def execute_callback(self, goal_handle):
        self.get_logger().info('开始执行任务')


        feedback_msg = Progress.Feedback()

        sum = 0
        for i in range(1, goal_handle.request.num + 1):
            sum += i
            feedback_msg.progress = i / goal_handle.request.num
            self.get_logger().info('连续反馈: %.2f' % feedback_msg.progress)
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1)

        goal_handle.succeed()
        result = Progress.Result()
        result.sum = sum
        self.get_logger().info('任务完成')

        return result


def main(args=None):

    rclpy.init(args=args)

    Progress_action_server = ProgressActionServer()
    rclpy.spin(Progress_action_server)

    rclpy.shutdown()

if __name__ == '__main__':
    main()