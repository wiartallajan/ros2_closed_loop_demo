# Launch file to launch a closed_loop demo file

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import RegisterEventHandler, ExecuteProcess, IncludeLaunchDescription, AppendEnvironmentVariable, SetEnvironmentVariable
from launch.event_handlers import OnProcessExit
from launch.substitutions import  PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    

    ### General Setup ###


    # Set path to bringup package (=current package)
    bringup_pkg = 'ros2_closed_loop_demo_bringup'
    bringup_share = FindPackageShare(package=bringup_pkg).find(bringup_pkg)

    # Set path to description package and model files
    description_pkg = 'ros2_closed_loop_demo_description'
    description_share = FindPackageShare(package=description_pkg).find(description_pkg)
    model_name = 'closed_loop_demo'
    world_name = 'demo_world_rotated'
    world_path = os.path.join(description_share, 'worlds', world_name+'.sdf')
    model_path = os.path.join(description_share, 'models', model_name, 'model.sdf')

    # set ros_gz_sim package
    ros_gz_sim_pkg = 'ros_gz_sim'
    ros_gz_sim_share = get_package_share_directory(ros_gz_sim_pkg)
    gz_launch_path = PathJoinSubstitution([ros_gz_sim_share, 'launch', 'gz_sim.launch.py'])
    gz_sim_path = os.path.join(description_share, 'models')


    ### Set environment variables ###


    # Set gazebo model path
    set_env_vars_resources = AppendEnvironmentVariable('GZ_SIM_RESOURCE_PATH', gz_sim_path)
    set_env_gz_version = SetEnvironmentVariable('GZ_VERSION', 'harmonic')

    env_variables = [
        set_env_vars_resources,
        set_env_gz_version,
    ]
    

    ### Define Launch actions ###


    # Kill all gazebo instances
    kill_gz_harmonic_instances_cmd = ExecuteProcess(
        cmd=['pkill', '-f', '-9', 'ign gazebo'],
        output='screen'
    )

    # Launch gazebo with a given world model (Gazebo Harmonic)
    launch_gz_harmonic_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gz_launch_path),
        launch_arguments={
            'gz_args': ['-r ', world_path,
                # ' --gui-config ', PathJoinSubstitution(
                #     [bringup_share, 'gazebo', 'gz_dec_overview.config']
                #     ),
                ],
            'on_exit_shutdown': 'True'
        }.items()
    )


    ### Declare launch commands ###


    nodes = [
        
        kill_gz_harmonic_instances_cmd,
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=kill_gz_harmonic_instances_cmd,
                on_exit=[launch_gz_harmonic_cmd],
            )
        )

    ]
    

    return LaunchDescription(env_variables + nodes)
