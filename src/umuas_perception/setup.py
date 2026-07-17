from setuptools import find_packages, setup

package_name = 'umuas_perception'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='triangle',
    maintainer_email='triangle@todo.todo',
    description='TODO: UMUAS perception solutions, such as target detection and tracking',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'my_node = umuas_perception.my_node:main'
        ],
    },
)
