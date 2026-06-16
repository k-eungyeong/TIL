[ airsim_nav2/setup.py 수정 예시 ] 

import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'airsim_nav2'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # ── 내가 만든 하위 폴더들을 빌드 대상에 추가 ──────────────────
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'maps'), glob('maps/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dmin',
    maintainer_email='dmin@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'cmd_vel_bridge = airsim_nav2.cmd_vel_bridge:main',
        ],
    },
)
