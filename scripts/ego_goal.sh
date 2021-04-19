##vins-mono
gnome-terminal --window -e 'bash -c "roslaunch simulation ego_stick.launch; exec bash"' \
--tab -e 'bash -c "sleep 1; roslaunch simulation ego_model.launch; exec bash"' \
--tab -e 'bash -c "sleep 1;source ~/EGO_ws/devel/setup.bash; rosrun pubcmd pub_campose.py; exec bash"' \
--tab -e 'bash -c "sleep 1;source ~/EGO_ws/devel/setup.bash; rosrun pubcmd repubodom.py; exec bash"' \
--tab -e 'bash -c "sleep 2;source ~/EGO_ws/devel/setup.bash; roslaunch ego_planner rviz.launch; exec bash"' \
--tab -e 'bash -c "sleep 2;source ~/EGO_ws/devel/setup.bash; roslaunch ego_planner burger_demo.launch; exec bash"' \
--tab -e 'bash -c "sleep 3;source ~/EGO_ws/devel/setup.bash; rosrun pubcmd pubcmd.py; exec bash"' \
--tab -e 'bash -c "sleep 3;source ~/EGO_ws/devel/setup.bash; rosrun pubcmd pubtwist.py; exec bash"' \
--tab -e 'bash -c "sleep 5; roslaunch simulation ego_model_car.launch; exec bash"' \
--tab -e 'bash -c "sleep 5; roslaunch turtlebot3_teleop turtlebot3_teleop_key_car.launch; exec bash"' \
--tab -e 'bash -c "sleep 5;source ~/EGO_ws/devel/setup.bash; rosrun pubcmd pub_goal.py; exec bash"' \

