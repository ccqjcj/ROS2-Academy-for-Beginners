from setuptools import find_packages, setup

package_name = 'py_tf_broadcaster'

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
    maintainer='ant',
    maintainer_email='ant@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'tf_static_broadcaster = py_tf_broadcaster.tf_static_broadcaster:main',
            'tf_dynamic_broadcaster = py_tf_broadcaster.tf_dynamic_broadcaster:main',
            'tf_point_broadcaster = py_tf_broadcaster.tf_point_broadcaster:main',
        ],
    },
)
