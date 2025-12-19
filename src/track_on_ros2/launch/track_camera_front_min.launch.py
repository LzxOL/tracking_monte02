import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


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


def generate_launch_description():
    ws_root = get_workspace_root()
    if ws_root:
        checkpoint_default = os.path.join(ws_root, 'src', 'track_on', 'checkpoints', 'track_on_checkpoint.pt')
    else:
        checkpoint_default = ''

    # Launch arguments
    checkpoint_path_arg = DeclareLaunchArgument(
        'checkpoint_path', default_value=checkpoint_default,
        description='TrackOn 模型检查点（ckp）路径')

    camera_topic_arg = DeclareLaunchArgument(
        'camera_topic', default_value='/right/color/video',
        description='前端摄像头颜色图像话题')

    publish_visualization_arg = DeclareLaunchArgument(
        'publish_visualization', default_value='true',
        description='是否发布叠加关键点的可视化图像')

    show_interactive_window_arg = DeclareLaunchArgument(
        'show_interactive_window', default_value='true',
        description='是否显示交互窗口（点击选择关键点、空格开始）')

    # Launch configurations
    checkpoint_path = LaunchConfiguration('checkpoint_path')
    camera_topic = LaunchConfiguration('camera_topic')
    publish_visualization = LaunchConfiguration('publish_visualization')
    show_interactive_window = LaunchConfiguration('show_interactive_window')

    node = Node(
        package='track_on_ros2',
        executable='track_camera_front_min_node',
        name='track_camera_front_min_node',
        output='screen',
        parameters=[{
            'checkpoint_path': checkpoint_path,
            'camera_topic': camera_topic,
            'publish_visualization': publish_visualization,
            'show_interactive_window': show_interactive_window,
        }]
    )

    return LaunchDescription([
        checkpoint_path_arg,
        camera_topic_arg,
        publish_visualization_arg,
        show_interactive_window_arg,
        node
    ])

