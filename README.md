# ros2_closed_loop_demo

Demo repository to test the limits of modelling closed kinematic loops in ROS2 and the new Gazebo

## Install

This repo works with all the standard ROS2 / Gazebo packages, no special installs required.

The functionality was only tested for `ROS2 Humble` with `Gazebo Harmonic`.

Simply clone the repository, link to your ros2 workspace and build.

```bash
colcon build
```

In a new terminal source the workspace (if you have not added this to your bashrc-file, make sure to source ROS as well).

```bash
. install/setup.bash
```

## Usage

To launch the provided models, simply use the provided launch files.

### 1. Five Bar Linkage

This model contains a standard five bar linkage. The axes of the closed loop are aligned with the world coordinate axis.

```bash
ros2 launch ros2_closed_loop_demo_bringup launch_closed_loop_demo.launch.py
```

>> This model behaves as expected: The DetachableJoint plugin keeps the kinematic loop closed and the links dangle freely.

### 2. Five Bar Linkage - rotated

This model contains a standard five bar linkage. But the five bar linkage is rotated around the z-axis, so that the axes of the closed loop are not aligned with the world coordinate axes anymore.

```bash
ros2 launch ros2_closed_loop_demo_bringup launch_closed_loop_rotated.launch.py
```

>> This model does not behave as expected: the kinematic chain bugs around.

### 3. Five Bar Linkage with additional vertical joint

This model contains a standard five bar linkage. But the five bar linkage is suspended with an additional joint aligned with the world z-axis.

```bash
ros2 launch ros2_closed_loop_demo_bringup launch_closed_loop_addJoint.launch.py
```

>> This model does not behave as expected: Gazebo crashes as soon as the vertical joint D0 is moved via the JointPositionController-Plugin in Gazebo. As long as the joint is not moved after launch, the model behaves as expected.
