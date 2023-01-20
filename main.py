import rospy
import dynamic_reconfigure.client
import os
import json
import requests


rospy.init_node('flight')


def get_data():
    """Get json data for aruco_pose."""
    host = 'http://10.1.4.207:80'
    s = requests.Session()
    s.auth = ('Participant-1', 'pass')
    data = {
        "message": "Success"
    }
    r = s.post(host + "/storage/report/map", json=data, verify=False)

    if r.status_code != 200:  # if error
        raise Exception(r.text)  # raise exception if error
    return r.text


x = get_data()
y = json.loads(x)  # parse json from string
name = 'out_map.txt'
s = f"rosrun aruco_pose genmap.py {y.get('length')} {y.get('x')} {y.get('y')} {y.get('dist_x')} {y.get('dist_y')} {y.get('first')} {'--bottom-left' if y.get('bottom_left') is True else '--top-left'} -o {name}"

os.system(s)  # run the command in terminal

map_client = dynamic_reconfigure.client.Client('aruco_map')
map_client.update_configuration({'map': f'/home/clover/catkin_ws/src/clover/aruco_pose/map/{name}'})  # update the map
