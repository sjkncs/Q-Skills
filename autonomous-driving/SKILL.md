---
name: autonomous-driving
description: Build autonomous driving systems with CARLA, OpenPCDet, mmdetection3d, Open3D. Covers 3D perception (BEV, point cloud), LiDAR processing, SLAM, sensor fusion, motion planning, and end-to-end driving. Use when working with self-driving, ADAS, or autonomous vehicle perception/planning.
version: 1.0.0
---

# Autonomous Driving (自动驾驶)

## Environment Setup (环境搭建)

### CARLA Simulator
```bash
# Download CARLA 0.9.15+ from GitHub releases
# https://github.com/carla-simulator/carla/releases

# Python API (matches server version exactly)
pip install carla==0.9.15

# Verify
python -c "import carla; print('CARLA', carla.__version__)"
```

Key points:
- Server and client versions must match exactly (0.9.15 server needs 0.9.15 client)
- On Windows, use `CarlaUE4.exe` to launch; on Linux, `./CarlaUE4.sh`
- Default port 2000; use `--world-port=2000` for headless
- For RL/agent training, launch with `-fps=20 -quality-level=Low`

### OpenPCDet (3D Detection)
```bash
# Clone and install
git clone https://github.com/open-mmlab/OpenPCDet.git
cd OpenPCDet
pip install spconv-cu118  # match your CUDA version
python setup.py develop

# Verify
python -c "from pcdet.datasets import DatasetTemplate; print('OpenPCDet OK')"
```

Supported models: PointPillars, CenterPoint, VoxelNet, PV-RCNN, SECOND, Part-A2, Voxel-RCNN.
Config files live under `tools/cfgs/`; pretrained weights under `models/`.

### mmdetection3d (BEV / Multi-Modal)
```bash
# Install mmcv first (match PyTorch/CUDA versions)
pip install mmcv==2.1.0 -f https://download.openmmlab.com/mmcv/dist/cu118/torch2.1/index.html

# Install mmdet, mmsegmentation, mmdet3d
pip install mmdet==3.3.0 mmsegmentation==1.2.2
git clone https://github.com/open-mmlab/mmdetection3d.git
cd mmdetection3d
pip install -e .

# Verify
python -c "import mmdet3d; print('mmdet3d', mmdet3d.__version__)"
```

Key models: BEVFormer, BEVFusion, DETR3D, PETR, StreamPETR, SOLOFusion.

### Open3D (Point Cloud Processing)
```bash
pip install open3d

# Verify
python -c "import open3d as o3d; print('Open3D', o3d.__version__)"
```

### nuScenes devkit
```bash
pip install nuscenes-devkit

# Verify
python -c "from nuscenes.nuscenes import NuScenes; print('nuScenes OK')"
```

Download data from https://www.nuscenes.org/download. Set env var:
```bash
export NUSCENES_DATAROOT=/path/to/nuscenes
```

### ROS2 + CARLA-ROS Bridge (Optional)
```bash
# Install ROS2 Humble (Ubuntu 22.04)
sudo apt install ros-humble-desktop

# CARLA-ROS bridge
git clone --recurse-submodules https://github.com/carla-simulator/ros-bridge.git
cd ros-bridge
colcon build --symlink-install
source install/setup.bash

# Launch
ros2 launch carla_ros_bridge carla_ros_bridge.launch.py
```

## Sensor Data & Datasets (传感器数据与数据集)

### nuScenes
- **Sensors**: 6 cameras (360-degree coverage), 1 LiDAR (32-beam Velodyne), 5 radars, GPS/IMU
- **Keyframes**: annotated at 2 Hz (10 classes, 3D boxes + attributes + tracks)
- **Sweeps**: raw sensor data at 20 Hz (LiDAR), 12 Hz (cameras)
- **Scenes**: 1000 scenes, 20 seconds each, ~40k keyframes total
- **Splits**: mini (10 scenes), trainval (850 scenes), test (150 scenes)

```python
from nuscenes.nuscenes import NuScenes
nusc = NuScenes(version='v1.0-trainval', dataroot='/data/nuscenes', verbose=True)
nusc.list_scenes()
sample = nusc.get('sample', nusc.sample[0]['token'])
```

### KITTI
- **Sensors**: stereo grayscale + stereo color cameras, Velodyne HDL-64E LiDAR, GPS/IMU
- **Tasks**: object detection, tracking, odometry, road/lane, depth completion, semantic segmentation
- **Coordinate frame**: camera-centric (x=right, y=down, z=forward)

```python
# KITTI detection label format
# type truncated occluded alpha bbox_2d dimensions location rotation_y
# Car 0.00 0 1.58 587.01 173.33 614.12 200.12 1.65 1.67 3.64 -0.45 1.66 46.70 -1.59
```

### Waymo Open Dataset
- **Sensors**: 5 LiDARs (1 main + 4 short-range), 5 cameras (front + sides + rear), GPS/IMU, audio
- **Scale**: 230k frames across 1150 scenes (20s each)
- **Labels**: 3D boxes for vehicles, pedestrians, cyclists + 2D camera labels
- **Access**: `pip install waymo-open-dataset`; data via TensorFlow Records

```python
import tensorflow as tf
from waymo_open_dataset import dataset_pb2
dataset = tf.data.TFRecordDataset('/path/to/tfrecords/*.tfrecord')
for raw_record in dataset:
    frame = dataset_pb2.Frame()
    frame.ParseFromString(bytearray(raw_record.numpy()))
```

### Argoverse 2
- **HD maps**: lane-level topology, crosswalks, stop lines, driveable area
- **Sensor data**: 7 ring cameras, 2 32-beam LiDARs, stereo cameras
- **Scenarios**: 1000 logs with 15-min segments
- **Forecasting**: 250k scenarios with 6s history + 6s future trajectories
- **API**: `pip install av2`

### CARLA Synthetic Data Generation
```python
import carla
client = carla.Client('localhost', 2000)
world = client.get_world()

# Spawn vehicle
vehicle_bp = world.get_blueprint_library().filter('vehicle.tesla.model3')[0]
spawn_point = world.get_map().get_spawn_points()[0]
vehicle = world.spawn_actor(vehicle_bp, spawn_point)

# Attach RGB camera
camera_bp = world.get_blueprint_library().find('sensor.camera.rgb')
camera_bp.set_attribute('image_size_x', '1920')
camera_bp.set_attribute('image_size_y', '1080')
camera_bp.set_attribute('fov', '90')
camera = world.spawn_actor(camera_bp, carla.Transform(
    carla.Location(x=1.5, z=2.0)), attach_to=vehicle)

# Attach LiDAR
lidar_bp = world.get_blueprint_library().find('sensor.lidar.ray_cast')
lidar_bp.set_attribute('channels', '64')
lidar_bp.set_attribute('range', '100')
lidar_bp.set_attribute('points_per_second', '1300000')
lidar = world.spawn_actor(lidar_bp, carla.Transform(
    carla.Location(x=0, z=2.0)), attach_to=vehicle)

# Depth camera for GT depth
depth_bp = world.get_blueprint_library().find('sensor.camera.depth')
depth_camera = world.spawn_actor(depth_bp, carla.Transform(
    carla.Location(x=1.5, z=2.0)), attach_to=vehicle)

# Semantic segmentation camera
seg_bp = world.get_blueprint_library().find('sensor.camera.semantic_segmentation')
seg_camera = world.spawn_actor(seg_bp, carla.Transform(
    carla.Location(x=1.5, z=2.0)), attach_to=vehicle)
```

## 3D Perception (三维感知)

### Point Cloud Methods

**Voxel-based (体素化)**
```
# VoxelNet: raw points -> voxels -> 3D CNN -> BEV -> detection
# SECOND: sparse 3D convolutions for efficiency
# Config: voxel_size=[0.16, 0.16, 4.0], point_cloud_range=[-51.2,-51.2,-5.0,51.2,51.2,3.0]
```

**Pillar-based (柱状化)**
```
# PointPillars: points -> pillars (vertical voxels) -> 2D CNN (Pseudo-image)
# Faster than voxel methods; trades z-resolution for speed
# pillar_size: [0.16, 0.16, 4.0], max_points_per_pillar: 100
```

**OpenPCDet training example**:
```bash
# Train PointPillars on KITTI
cd OpenPCDet/tools
python train.py --cfg_file cfgs/kitti_models/pointpillar.yaml \
    --batch_size 4 --epochs 80 --workers 4

# Train CenterPoint on nuScenes
python train.py --cfg_file cfgs/nuscenes_models/cbgs_dyn_pp_centerpoint.yaml \
    --batch_size 4 --epochs 20 --sync_bn
```

### BEV Perception (鸟瞰图感知)

**BEVFormer** (Transformer-based):
- Camera images -> image features (ResNet/VoV)
- BEV queries on grid -> deformable attention on image features
- Temporal aggregation across frames
- 3D detection heads (CenterPoint-style)
- nuScenes NDS: 56.9 (base), 59.5 (large)

```bash
# Train BEVFormer on nuScenes
cd projects/configs/bevformer
python tools/train.py projects/configs/bevformer/bevformer_base.py \
    --work-dir work_dirs/bevformer_base
```

**BEVFusion** (Camera + LiDAR):
- Camera branch: image features -> BEV via LSS (Lift-Splat-Shoot) or inverse depth
- LiDAR branch: point cloud -> VoxelNet backbone -> BEV features
- Feature-level fusion in BEV space
- NDS: 69.3 (nuScenes val), real-time capable

**BEVDet / BEVDet4D**:
- Explicit depth estimation for camera-to-BEV projection
- 4D variant adds temporal BEV feature alignment across frames

### Camera-Only 3D Detection

| Model | Approach | nuScenes NDS | Key Idea |
|-------|----------|--------------|----------|
| PETR | 3D position encoding | 41.3 | Implicit 3D coords from camera intrinsics |
| StreamPETR | Temporal streaming | 49.8 | Recurrent BEV feature update |
| SOLOFusion | Long-range temporal | 52.5 | Frame-wise features without explicit depth |
| PETRv2 | Temporal + guided attn | 47.4 | Temporal PETR with guided attention |

### End-to-End Driving (端到端自动驾驶)

**UniAD**: perception -> prediction -> planning in unified Transformer
- Single model: tracking + motion forecasting + occupancy prediction + planning
- Camera input -> planning output (waypoints)
- CARLA leaderboard: top scores with planning safety score

**SparseDrive**: sparse queries for perception + planning
- Sparse instance queries across perception and planning
- End-to-end optimization of detection + motion planning
- Lower compute than dense BEV methods

**VAD (Vectorized Auto-Driving)**:
- Vectorized scene representation (agent queries, map queries, planner query)
- Direct waypoint regression for planning
- Efficient: no dense BEV grid needed

## LiDAR Processing with Open3D (点云处理)

### Loading Point Clouds
```python
import open3d as o3d
import numpy as np

# Load PCD file
pcd = o3d.io.read_point_cloud("scan.pcd")
print(f"Points: {len(pcd.points)}")

# Load KITTI .bin (raw float32: x, y, z, intensity)
points = np.fromfile("000000.bin", dtype=np.float32).reshape(-1, 4)
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points[:, :3])

# Load PLY
pcd = o3d.io.read_point_cloud("scan.ply")

# Visualize
o3d.visualization.draw_geometries([pcd])
```

### Ground Plane Removal
```python
# RANSAC plane segmentation
plane_model, inliers = pcd.segment_plane(
    distance_threshold=0.2,   # max distance to plane
    ransac_n=3,               # points per iteration
    num_iterations=1000
)
ground = pcd.select_by_index(inliers)
non_ground = pcd.select_by_index(inliers, invert=True)

# Cloth Simulation Filter (better for uneven terrain)
# Requires Open3D >= 0.16
# import open3d.t.geometry as tgeom  # tensor geometry API
```

### Downsampling & Filtering
```python
# Voxel downsampling (uniform density)
downsampled = pcd.voxel_down_sample(voxel_size=0.1)

# Statistical outlier removal (remove noise)
cl, ind = downsampled.remove_statistical_outlier(
    nb_neighbors=20,      # neighbors to analyze
    std_ratio=2.0         # standard deviation threshold
)
clean = downsampled.select_by_index(ind)

# Radius outlier removal
cl, ind = clean.remove_radius_outlier(
    nb_points=16, radius=0.5
)
clean = clean.select_by_index(ind)
```

### Registration (配准)
```python
# ICP (Iterative Closest Point) - fine alignment
source = o3d.io.read_point_cloud("source.pcd")
target = o3d.io.read_point_cloud("target.pcd")

# Initial guess from odometry or coarse alignment
init_transform = np.eye(4)

# Point-to-plane ICP (faster convergence)
source.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(
    radius=0.1, max_nn=30))
target.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(
    radius=0.1, max_nn=30))

result = o3d.pipelines.registration.registration_icp(
    source, target,
    max_correspondence_distance=0.05,
    init=init_transform,
    estimation_method=o3d.pipelines.registration.TransformationEstimationPointToPlane()
)
print(f"Fitness: {result.fitness:.4f}, RMSE: {result.inlier_rmse:.4f}")

# Fast Global Registration (FGR) - coarse alignment
source_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
    source, o3d.geometry.KDTreeSearchParamHybrid(radius=0.5, max_nn=100))
target_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
    target, o3d.geometry.KDTreeSearchParamHybrid(radius=0.5, max_nn=100))

result_fgr = o3d.pipelines.registration.registration_fgr_based_on_feature_matching(
    source, target, source_fpfh, target_fpfh,
    o3d.pipelines.registration.FastGlobalRegistrationOption(
        maximum_correspondence_distance=0.075
    )
)
```

### Feature Extraction (FPFH)
```python
# Estimate normals
pcd.estimate_normals(
    search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30)
)

# Compute FPFH features (33-dim descriptor per point)
fpfh = o3d.pipelines.registration.compute_fpfh_feature(
    pcd,
    search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.25, max_nn=100)
)
# Shape: (33, num_points)
features = np.asarray(fpfh.data)
```

## Sensor Fusion (多传感器融合)

### Early Fusion (前融合)
- Concatenate camera features with LiDAR point features before detection head
- Requires precise extrinsic calibration (camera-to-LiDAR transform)
- Example: PointPainting (paint LiDAR points with semantic scores from camera)

```python
# Pseudo-code: PointPainting
for point in lidar_points:
    pixel = project_to_camera(point, lidar_to_camera_extrinsic, camera_intrinsic)
    seg_score = segmentation_model(image)[pixel]
    point.features = concat(point.features, seg_score)
# Then run detection on enriched point cloud
```

### Late Fusion (后融合)
- Run detection independently per modality
- Fuse results with NMS (Non-Maximum Suppression) across modalities
- Simpler, more robust to single-sensor failure
- Common in production: camera detections + radar detections + LiDAR detections

```python
# Pseudo-code: late fusion NMS
dets_camera = detect_3d_camera(images)
dets_lidar = detect_3d_lidar(point_cloud)
all_dets = dets_camera + dets_lidar
# NMS: suppress overlapping boxes, keep higher confidence
final_dets = nms_3d(all_dets, iou_threshold=0.25)
```

### BEVFusion (特征级融合)
- Camera branch: image backbone -> FPN -> LSS depth estimation -> BEV features
- LiDAR branch: VoxelNet backbone -> BEV features
- Fusion: element-wise addition in BEV space + conv refinement
- State-of-the-art on nuScenes: NDS 69.3

```python
# mmdetection3d BEVFusion config
# projects/configs/bevfusion/bevfusion_lidar_voxel0075_second_secfpn_8xb4.py
```

### Temporal Fusion (时序融合)
- Aggregate BEV features across multiple frames
- Align using ego-motion (pose delta between frames)
- BEVFormer: spatial-temporal attention over past N frames
- StreamPETR: recurrent feature bank with pose-guided warping
- Critical for occlusion handling and velocity estimation

```python
# Pseudo-code: temporal BEV aggregation
bev_features = []
for t in range(num_frames):
    feat = extract_bev(frame[t])
    aligned_feat = warp_bev(feat, ego_pose_delta[t])
    bev_features.append(aligned_feat)
# Attend over temporal features
temporal_bev = temporal_attention(bev_features)
```

## SLAM & Localization (定位与建图)

### Visual SLAM
- **ORB-SLAM3**: monocular/stereo/RGB-D, multi-map, IMU fusion, loop closure
  - Good for camera-only setups; requires good feature texture
  - `git clone https://github.com/UZ-SLAMLab/ORB_SLAM3.git`
- **RTAB-Map**: real-time, graph optimization, RGB-D/stereo, built-in OctoMap
  - ROS integration: `sudo apt install ros-humble-rtabmap-ros`

### LiDAR SLAM
- **LOAM / A-LOAM**: feature-based (edge + planar), real-time on Velodyne
- **LeGO-LOAM**: lightweight, ground segmentation + clustering for features
- **LIO-SAM**: factor graph + IMU preintegration, state-of-the-art accuracy
  ```bash
  git clone https://github.com/TixiaoShan/LIO-SAM.git
  roslaunch lio_sam run.launch
  ```
- **hdl-graph-slam**: graph-based, NDT scan matching + IMU + GPS (optional)

### Multi-Sensor Fusion SLAM
- LiDAR + IMU + GPS + camera for robustness
- Factor graph: pose nodes connected by LiDAR odometry, IMU preintegration, GPS priors, loop closure
- For autonomous driving: high-precision GNSS/INS + LiDAR SLAM for centimeter-level localization
- HD map matching: localize against pre-built map using LiDAR-to-map registration

## Motion Planning (运动规划)

### Frenet Frame Planning (Frenet坐标系规划)
- Decouple into lateral (s-direction along reference path) and longitudinal (d-direction lateral offset)
- Sample lateral offsets and longitudinal profiles
- Evaluate trajectories: collision, smoothness, comfort, lane keeping
- Convert back to Cartesian for execution

```python
# Pseudo-code: Frenet planner
for lateral_offset in np.arange(-3.5, 3.5, 0.5):
    for target_speed in np.arange(0, max_speed, 2.0):
        for time_horizon in [2.0, 3.0, 4.0, 5.0]:
            trajectory = generate_frenet_trajectory(
                lateral_offset, target_speed, time_horizon, reference_path
            )
            cost = evaluate_trajectory(trajectory, obstacles, road_constraints)
            candidates.append((trajectory, cost))

best_trajectory = min(candidates, key=lambda x: x[1])
```

### Lattice Planner
- State lattice: discretize state space (x, y, heading, curvature, speed)
- Pre-compute motion primitives connecting states
- Search graph for optimal path
- Good for structured environments (parking lots, intersections)

### EM Planner (Expectation-Maximization Planner, Apollo)
- **E-step (path)**: given current speed profile, optimize lateral path
- **M-step (speed)**: given current path, optimize longitudinal speed profile
- Iterate until convergence (typically 3-5 iterations)
- DP (dynamic programming) for warm start + QP (quadratic programming) for refinement

### Behavioral Planning (行为规划)
```python
# Finite state machine for driving decisions
class DrivingFSM:
    states = ['LANE_FOLLOW', 'LANE_CHANGE_LEFT', 'LANE_CHANGE_RIGHT',
              'STOP', 'YIELD', 'EMERGENCY_STOP']

    def transition(self, current_state, observations):
        if observations['obstacle_ahead_distance'] < emergency_threshold:
            return 'EMERGENCY_STOP'
        if current_state == 'LANE_FOLLOW':
            if observations['slow_vehicle_ahead'] and observations['left_lane_clear']:
                return 'LANE_CHANGE_LEFT'
            if observations['red_light'] or observations['stop_sign']:
                return 'STOP'
        if current_state == 'LANE_CHANGE_LEFT':
            if observations['lane_change_complete']:
                return 'LANE_FOLLOW'
        return current_state
```

### MPC Trajectory Tracking (模型预测控制)
```python
# Bicycle model for vehicle dynamics
# State: [x, y, psi, v]
# Control: [delta (steering), a (acceleration)]
# dx/dt = v * cos(psi)
# dy/dt = v * sin(psi)
# dpsi/dt = v / L * tan(delta)   # L = wheelbase
# dv/dt = a

# MPC formulation
# min sum_{k=0}^{N} || state[k] - reference[k] ||_Q + || control[k] ||_R
# subject to: bicycle model dynamics, steering limits, acceleration limits
# Use CasADi or OSQP for real-time solving

import casadi as ca
# Define optimization variables, constraints, cost
# Solve at 10-20 Hz for real-time tracking
```

## Evaluation Metrics (评价指标)

### 3D Object Detection
- **AP (Average Precision)**: at IoU threshold (0.7 for car, 0.5 for pedestrian on KITTI)
- **AP@BEV**: IoU computed in bird's eye view only
- **AP@3D**: IoU computed on 3D bounding boxes
- **KITTI difficulty**: Easy / Moderate / Hard (by occlusion, truncation, bounding box height)

### nuScenes Detection Score (NDS)
```
NDS = 1 - (1/6) * sum of normalized errors
Errors:
  - mAP: mean AP across 10 classes at distance thresholds [0.5, 1.0, 2.0, 4.0]
  - mATE: mean Average Translation Error (center distance, meters)
  - mASE: mean Average Scale Error (IoU of box sizes)
  - mAOE: mean Average Orientation Error (yaw difference, radians)
  - mAVE: mean Average Velocity Error (velocity magnitude + direction)
  - mAAE: mean Average Attribute Error (attribute classification accuracy)
```

### Tracking Metrics
- **AMOTA**: Average Multi-Object Tracking Accuracy (across recall thresholds)
- **AMOTP**: Average Multi-Object Tracking Precision (average position error)
- **IDS**: Identity Switches (number of times track IDs swap)
- **HOTA**: Higher-Order Tracking Accuracy (detection + association quality)

### Planning Metrics
- **L2 Error**: average L2 distance between planned and GT expert trajectory
- **Collision Rate**: fraction of planned trajectories that intersect obstacles
- **Comfort**: lateral/longitudinal acceleration and jerk limits
- **Progress**: distance covered along route per unit time
- **Off-road Rate**: fraction of trajectory outside drivable area

### Benchmarking Commands
```bash
# OpenPCDet evaluation on KITTI
python test.py --cfg_file cfgs/kitti_models/pointpillar.yaml \
    --ckpt output/pointpillar/default/ckpt/checkpoint_epoch_80.pth

# mmdetection3d evaluation on nuScenes
python tools/test.py projects/configs/bevformer/bevformer_base.py \
    work_dirs/bevformer_base/latest.pth --eval bbox
```

## Visualization (可视化)

### Open3D Point Cloud + Bounding Boxes
```python
import open3d as o3d
import numpy as np

# Load and color point cloud
pcd = o3d.io.read_point_cloud("scan.pcd")
pcd.paint_uniform_color([0.7, 0.7, 0.7])  # gray

# Create 3D bounding box
bbox = o3d.geometry.OrientedBoundingBox(
    center=[10.0, 2.0, 1.0],
    R=o3d.geometry.TriangleMesh.create_coordinate_frame().get_rotation_matrix_from_xyz([0, 0, 0.3]),
    extent=[4.5, 1.8, 1.6]  # l, w, h
)
bbox.color = [1, 0, 0]  # red

o3d.visualization.draw_geometries([pcd, bbox])
```

### BEV Visualization
```python
import matplotlib.pyplot as plt
import numpy as np

# BEV from point cloud
def pointcloud_to_bev(points, voxel_size=0.1, x_range=(-51.2, 51.2), y_range=(-51.2, 51.2)):
    x_idx = ((points[:, 0] - x_range[0]) / voxel_size).astype(int)
    y_idx = ((points[:, 1] - y_range[0]) / voxel_size).astype(int)
    x_size = int((x_range[1] - x_range[0]) / voxel_size)
    y_size = int((y_range[1] - y_range[0]) / voxel_size)
    bev = np.zeros((x_size, y_size), dtype=np.uint8)
    valid = (x_idx >= 0) & (x_idx < x_size) & (y_idx >= 0) & (y_idx < y_size)
    bev[x_idx[valid], y_idx[valid]] = 255
    return bev

bev_image = pointcloud_to_bev(points)
plt.imshow(bev_image, cmap='gray')
plt.title("Bird's Eye View")
plt.show()
```

### CARLA Visualization
```python
import carla

# Set spectator (third-person camera)
world = client.get_world()
spectator = world.get_spectator()
spectator.set_transform(carla.Transform(
    carla.Location(x=-10, z=15),
    carla.Rotation(pitch=-30)
))

# Weather/lighting presets
weather_presets = [
    carla.WeatherParameters.ClearNoon,
    carla.WeatherParameters.CloudySunset,
    carla.WeatherParameters.HardRainNoon,
    carla.WeatherParameters.ClearSunset,
]
world.set_weather(carla.WeatherParameters.HardRainNoon)
```

### nuScenes Visualization
```python
from nuscenes.nuscenes import NuScenes
nusc = NuScenes(version='v1.0-trainval', dataroot='/data/nuscenes')

# Render scene (plays back sensor data)
nusc.render_scene(nusc.scene[0]['token'])

# Render specific sensor data (camera, LiDAR, radar)
sample = nusc.sample[0]
for sensor_channel in ['CAM_FRONT', 'LIDAR_TOP', 'RADAR_FRONT']:
    sample_data = nusc.get('sample_data',
        nusc.get_sample_data_path(sample['data'][sensor_channel]))
    nusc.render_sample_data(sample_data['token'], out_path=f'viz_{sensor_channel}.png')

# Render ego pose on map
nusc.render_egoposes_on_fancy_map(nusc.scene[0]['token'])

# Render annotation (3D boxes on camera image)
nusc.render_sample(sample['token'])
```

## Pitfalls (常见陷阱)

- **nuScenes sweeps vs keyframes**: sweeps = raw 20 Hz data (no annotations); keyframes = annotated 2 Hz data. Always check which you are using. `nusc.get_sample_data` returns keyframe by default; use `nusc.get('sample_data', token)` with sweep token for raw sweeps.

- **LiDAR coordinate frames**: nuScenes LiDAR frame is sensor-local (x=forward, y=left, z=up). KITTI LiDAR is different (x=forward, y=left, z=up but origin offset). Always apply the correct sensor-to-ego and ego-to-global transforms.

- **Camera intrinsic calibration**: BEVFormer and LSS-based methods require precise camera intrinsics. Even small errors in focal length or principal point cause severe depth estimation errors. Always use dataset-provided intrinsics, not assumed pinhole models.

- **CARLA weather/lighting**: synthetic data quality depends heavily on lighting conditions. Models trained only on ClearNoon fail at night/rain. Always randomize weather, time-of-day, and sun position during data collection.

- **End-to-end model compute**: UniAD, VAD, SparseDrive require 4-8 A100 GPUs and days of training. Start with modular pipelines (detection + tracking + planning) before attempting end-to-end.

- **nuScenes evaluation server**: test set has no public GT labels. Submit to the evaluation server at https://eval.ai for official scores. Local validation uses the val split (150 scenes).

- **OpenPCDet spconv versions**: spconv API changed between v1.x and v2.x. Use `spconv-cu118` (v2.x) with recent OpenPCDet. Mismatched spconv versions cause silent import errors.

- **Point cloud range**: different models expect different point cloud ranges. nuScenes default is [-51.2, -51.2, -5.0, 51.2, 51.2, 3.0]; KITTI is [0, -40, -3, 70.4, 40, 1]. Check model configs carefully.

- **CARLA tick vs wait**: `world.tick()` advances simulation by one step and returns. `world.wait_for_tick()` blocks until next tick. Use `tick()` for synchronous mode (recommended for data collection).

- **GPS/IMU drift**: pure GPS localization drifts 1-5 meters. Always fuse with LiDAR SLAM or visual odometry for autonomous driving applications.

## Verification (验证)

Run these commands to confirm your environment:
```bash
python -c "import carla; print('CARLA', carla.__version__)"
python -c "import open3d as o3d; print('Open3D', o3d.__version__)"
python -c "from pcdet.datasets import DatasetTemplate; print('OpenPCDet OK')"
python -c "import mmdet3d; print('mmdet3d', mmdet3d.__version__)"
python -c "from nuscenes.nuscenes import NuScenes; print('nuScenes OK')"
```
