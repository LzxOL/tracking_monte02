import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

# 仅启动 TF 查询节点的 launch 文件
# 用法：
#   ros2 launch Monte_api_ros2 head_base_tf.launch.py \
#       robot_ip:=192.168.22.63:50051 \
#       parent_frame:=link_t0_base child_frame:=link_h2_head rate:=2.0

def get_workspace_root():
    """获取工作空间根目录"""
    current_file = os.path.abspath(__file__)
    path = os.path.dirname(current_file)
    for _ in range(10):
        if os.path.basename(path) == 'tracking_with_cameara_ws':
            return path
        parent = os.path.dirname(path)
        if parent == path:
            break
        path = parent
    return None


def generate_launch_description() -> LaunchDescription:
    ws_root = get_workspace_root()
    if ws_root:
        default_lib_path = os.path.join(ws_root, 'src', 'Monte_api_ros2', 'lib')
    else:
        default_lib_path = ''
    
    robot_ip_arg = DeclareLaunchArgument(
        'robot_ip', default_value='192.168.22.63:50051',
        description='Robot gRPC server ip:port'
    )
    robot_lib_path_arg = DeclareLaunchArgument(
        'robot_lib_path',
        default_value=default_lib_path,
        description='Path to RobotLib .so directory'
    )
    parent_frame_arg = DeclareLaunchArgument(
        'parent_frame', default_value='link_t0_base', description='TF parent frame'
    )
    child_frame_arg = DeclareLaunchArgument(
        'child_frame', default_value='link_h2_head', description='TF child frame'
    )
    rate_arg = DeclareLaunchArgument(
        'rate', default_value='2.0', description='Query rate (Hz)'
    )

    robot_ip = LaunchConfiguration('robot_ip')
    robot_lib_path = LaunchConfiguration('robot_lib_path')
    parent_frame = LaunchConfiguration('parent_frame')
    child_frame = LaunchConfiguration('child_frame')
    rate = LaunchConfiguration('rate')

    tf_node = Node(
        package='Monte_api_ros2',
        executable='head_base_tf_node',
        name='head_base_tf_node',
        output='screen',
        parameters=[{
            'robot_ip': robot_ip,
            'robot_lib_path': robot_lib_path,
            'parent_frame': parent_frame,
            'child_frame': child_frame,
            'rate': rate,
        }]
    )

    return LaunchDescription([
        robot_ip_arg, robot_lib_path_arg,
        parent_frame_arg, child_frame_arg, rate_arg,
        tf_node,
    ])

