# 使用方法

```xml
roslaunch trajectory_player trajectory_player.launch
```

在 launch 文件中可以改变轨迹数据的路径、时间间隔，两点之间的插值数量以及是否循环播放。

多车场景**或许**可以这样设置 roslaunch（我也没试过，GPT 说的）

```xml
<!-- Define common parameters -->
<arg name="data_interval" default="0.1"/>
<arg name="discrete_num" default="10"/>
<arg name="loop_flag" default="False"/>

<!-- Group nodes under common parameters -->
<group ns="vehicles">
    <param name="data_interval" value="$(arg data_interval)"/>
    <param name="discrete_num" value="$(arg discrete_num)"/>
    <param name="loop_flag" value="$(arg loop_flag)"/>

    <!-- Node definitions -->
    <node name="model_1" pkg="trajectory_player" type="trajectory_player.py" output="screen">
        <param name="data_path" value="path-to-model1-trajectory.csv"/>
        <param name="model_name" value="model1"/>
    </node>

    <!-- Node definitions -->
    <node name="model_2" pkg="trajectory_player" type="trajectory_player.py" output="screen">
        <param name="data_path" value="path-to-model2-trajectory.csv"/>
        <param name="model_name" value="model2"/>
    </node>
</group>
```
