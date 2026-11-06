import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'umuas_simulation'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        # Launch files
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')),

        # Gazebo worlds
        (os.path.join('share', package_name, 'worlds'),
            glob('worlds/**/*', recursive=True)),

        # Gazebo models
        (os.path.join('share', package_name, 'models'),
            glob('models/**/*', recursive=True)),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='triangle',
    maintainer_email='umiller101@gmail.com',
    description='TODO: Package description',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
