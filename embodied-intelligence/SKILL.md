---
name: embodied-intelligence
description: Build embodied AI systems with MuJoCo, NVIDIA Isaac Sim/Lab, LeRobot, OpenVLA, Genesis. Covers sim-to-real transfer, robotic manipulation, navigation, VLA models, and reinforcement learning for robotics. Use when working with robot simulation, policy training, or deployment.
version: 1.0.0
---

# Embodied Intelligence / 具身智能

Comprehensive skill for building embodied AI systems — from simulation and policy training to real-world deployment. Covers the full stack: physics simulators, imitation learning, reinforcement learning, vision-language-action models, and sim-to-real transfer.

---

## 1. Environment Setup / 环境搭建

### 1.1 MuJoCo (Core Simulator)

MuJoCo is the default physics simulator for robotics research. Version 3.0+ includes GPU-accelerated MJX (MuJoCo XLA) via JAX.

```bash
# Core MuJoCo (C library + Python bindings)
pip install "mujoco>=3.0"

# MJX for GPU-parallel simulation (requires JAX with CUDA)
pip install "mujoco[mjx]"
# Or install MJX explicitly:
pip install mujoco-mjx

# Verify installation
python -c "import mujoco; m=mujoco.MjModel.from_xml_string('<mujoco/>'); print(f'MuJoCo {mujoco.__version__} OK')"

# Test MJX (GPU)
python -c "import mujoco.mjx; print('MJX available')"
```

**Key dependencies:**
- `dm_control` — DeepMind's control suite built on MuJoCo, provides standard benchmark tasks
- `gymnasium[mujoco]` — Gymnasium wrappers for MuJoCo environments

```bash
pip install dm_control "gymnasium[mujoco]"
```

### 1.2 NVIDIA Isaac Sim / Isaac Lab

Isaac Sim provides photorealistic simulation with RTX rendering. Isaac Lab (formerly Isaac Orbit) is the RL/robot-learning framework built on top.

```bash
# Option A: Install Isaac Lab via pip (recommended for Isaac Sim 4.2+)
# Requires Isaac Sim installed first via Omniverse Launcher
pip install isaaclab isaaclab_assets isaaclab_tasks isaaclab_mimic

# Option B: Install from source (latest features)
git clone https://github.com/isaac-sim/IsaacLab.git
cd IsaacLab
./isaaclab.sh --install  # Linux
isaaclab.bat --install   # Windows

# Option C: Container (headless training on remote GPU servers)
docker pull nvcr.io/nvidia/isaac-sim:4.2.0
# Run with GPU passthrough:
docker run --gpus all -e "ACCEPT_EULA=Y" --rm -it \
  -v $HOME/.Xauthority:/root/.Xauthority \
  --network host \
  nvcr.io/nvidia/isaac-sim:4.2.0

# Verify Isaac Lab
python -c "from isaaclab.envs import ManagerBasedRLEnv; print('Isaac Lab OK')"
```

**Hardware requirement:** NVIDIA GPU with RTX support (Turing/Ampere/Hopper), 8GB+ VRAM minimum, 24GB+ recommended for parallel environments.

### 1.3 LeRobot (Hugging Face Robotics)

LeRobot is the "Hugging Face of robotics" — a unified framework for data collection, policy training, and deployment. Supports ALOHA, Koch, SO-100 robots out of the box.

```bash
# Install LeRobot (v0.4+)
pip install lerobot

# Install with optional robot hardware support
pip install "lerobot[aloha]"    # ALOHA bimanual robot
pip install "lerobot[koch]"     # Koch v1.1 arm
pip install "lerobot[so100]"    # SO-100 low-cost arm

# Install from source for latest
git clone https://github.com/huggingface/lerobot.git
cd lerobot
pip install -e ".[dev]"

# Verify
python -c "from lerobot.common.datasets.lerobot_dataset import LeRobotDataset; print('LeRobot OK')"

# Download a dataset from the Hub
python -c "
from lerobot.common.datasets.lerobot_dataset import LeRobotDataset
ds = LeRobotDataset('lerobot/aloha_sim_transfer_cube_human')
print(f'Episodes: {ds.num_episodes}, Frames: {len(ds)}')
"
```

### 1.4 Genesis (Ultra-Fast Parallel Simulation)

Genesis provides 10-80x faster simulation than MuJoCo for massively parallel training. Written in Taichi for GPU-native physics.

```bash
pip install genesis-world

# Verify
python -c "import genesis as gs; gs.init(); print(f'Genesis {gs.__version__} OK')"
```

**When to use Genesis vs MuJoCo:**
- Genesis:大规模并行训练 (1000s of parallel envs), soft-body, fluid, cloth
- MuJoCo: precise contact dynamics, standard benchmarks, MJCF ecosystem
- Isaac Sim: photorealistic rendering, domain randomization for sim2real

### 1.5 VLA Models (Vision-Language-Action)

```bash
# OpenVLA (7B parameter VLA, based on Llama 2 + SigLIP + DROID)
pip install openvla transformers torch
# Requires 24GB+ VRAM for inference, 48GB+ for fine-tuning

# Octo (generalist policy, supports fine-tuning to new robots)
pip install octo
# GitHub: https://github.com/octo-models/octo

# OpenPI / Pi0 (flow-matching VLA from Physical Intelligence)
# Access via: https://github.com/Physical-Intelligence/openpi
git clone https://github.com/Physical-Intelligence/openpi.git
cd openpi
pip install -e .
# Pi0 uses flow matching for continuous action generation —
# more sample-efficient than diffusion for dexterous manipulation
```

---

## 2. Simulation Pipeline / 仿真管线

### 2.1 MuJoCo Scene Definition

```xml
<!-- robot_task.xml — minimal manipulation scene -->
<mujoco model="robot_task">
  <compiler angle="radian" meshdir="meshes/" autolimits="true"/>

  <option timestep="0.002" integrator="implicitfast" gravity="0 0 -9.81"/>

  <asset>
    <!-- Robot mesh (URDF-converted or native MJCF) -->
    <mesh name="base_link" file="base_link.stl"/>
    <mesh name="link1" file="link1.stl"/>
    <texture type="skybox" builtin="gradient" rgb1="0.3 0.3 0.3" rgb2="0.0 0.0 0.0"/>
    <texture name="floor_tex" type="2d" builtin="checker" rgb1=".2 .3 .4" rgb2=".1 .15 .2" width="512" height="512"/>
    <material name="floor_mat" texture="floor_tex" texrepeat="5 5"/>
  </asset>

  <worldbody>
    <light pos="0 0 3" dir="0 0 -1" diffuse="0.8 0.8 0.8"/>
    <geom name="floor" type="plane" size="2 2 0.1" material="floor_mat"/>

    <!-- Robot arm -->
    <body name="base" pos="0 0 0.05">
      <geom type="mesh" mesh="base_link"/>
      <body name="link1" pos="0 0 0.1">
        <joint name="joint1" type="hinge" axis="0 0 1" range="-3.14 3.14"/>
        <geom type="mesh" mesh="link1"/>
        <!-- Add more links... -->
      </body>
    </body>

    <!-- Target object -->
    <body name="target_cube" pos="0.3 0 0.05">
      <freejoint name="cube_joint"/>
      <geom type="box" size="0.02 0.02 0.02" rgba="1 0 0 1" mass="0.1"/>
    </body>

    <!-- Camera for visual observations -->
    <camera name="wrist_cam" pos="0.2 0 0.3" xyaxes="0 1 0 -1 0 1" fovy="90"/>
    <camera name="overhead_cam" pos="0 0 1" xyaxes="1 0 0 0 1 0" fovy="60"/>
  </worldbody>

  <actuator>
    <motor joint="joint1" ctrlrange="-1 1" ctrllimited="true" gear="100"/>
    <!-- Add actuators for each joint -->
  </actuator>

  <sensor>
    <jointpos joint="joint1" name="joint1_pos"/>
    <jointvel joint="joint1" name="joint1_vel"/>
    <framepos objtype="body" objname="target_cube" name="cube_pos"/>
    <touch site="fingertip" name="fingertip_touch"/>
  </sensor>
</mujoco>
```

```python
# Loading and stepping the simulation
import mujoco
import numpy as np

model = mujoco.MjModel.from_xml_path("robot_task.xml")
data = mujoco.MjData(model)

# Step the simulation
for _ in range(1000):
    data.ctrl[:] = np.random.uniform(-1, 1, model.nu)
    mujoco.mj_step(model, data)

# Render camera image
renderer = mujoco.Renderer(model, height=480, width=640)
mujoco.mj_forward(model, data)
renderer.update_scene(data, camera="overhead_cam")
image = renderer.render()  # numpy array (H, W, 3)
```

### 2.2 Isaac Lab Parallel Environments

```python
"""Isaac Lab: parallel environment setup for manipulation task."""
import isaaclab.sim as sim_cfg
from isaaclab.envs import ManagerBasedRLEnv, ManagerBasedRLEnvCfg
from isaaclab.scene import InteractiveSceneCfg
from isaaclab.assets import ArticulationCfg, AssetBaseCfg
from isaaclab.managers import ObservationTerm as ObsTerm
from isaaclab.managers import RewardTerm as RewTerm
from isaaclab.utils import configclass
import torch

@configclass
class MyManipulationEnvCfg(ManagerBasedRLEnvCfg):
    """Configuration for a parallel manipulation environment."""

    # Simulation: 512 parallel envs on a single GPU
    sim: sim_cfg.SimulationCfg = sim_cfg.SimulationCfg(
        dt=1/120,
        device="cuda:0",
    )
    scene: InteractiveSceneCfg = InteractiveSceneCfg(
        num_envs=512,        # parallel environments
        env_spacing=2.0,     # meters between env origins
        replicate_physics=True,
    )

    # Observations, actions, rewards, terminations...
    # (configure via manager term configs)

# Create and use the environment
env = ManagerBasedRLEnv(cfg=MyManipulationEnvCfg())
obs, _ = env.reset()

for step in range(200):
    actions = torch.randn(env.num_envs, env.action_space.shape[-1], device="cuda:0")
    obs, rewards, terminated, truncated, info = env.step(actions)
```

### 2.3 Genesis Parallel Simulation

```python
"""Genesis: massively parallel rigid-body simulation."""
import genesis as gs
import torch

gs.init(backend=gs.cuda)  # GPU backend

scene = gs.Scene(
    sim_options=gs.options.SimOptions(
        dt=0.01,
        substeps=10,
    ),
    viewer_options=gs.options.ViewerOptions(
        camera_pos=(3, -1, 1.5),
        camera_lookat=(0.0, 0.0, 0.5),
        camera_fov=40,
    ),
    show_viewer=False,  # headless for training
)

# Load robot (URDF) and object
plane = scene.add_entity(gs.morphs.Plane())
robot = scene.add_entity(
    gs.morphs.URDF(file="urdf/franka_panda.urdf", fixed=True),
)
cube = scene.add_entity(
    gs.morphs.Box(size=(0.04, 0.04, 0.04), pos=(0.5, 0, 0.02)),
)

scene.build(n_envs=4096)  # 4096 parallel environments

# Run simulation loop
for i in range(100):
    actions = torch.randn(4096, robot.n_dofs, device="cuda")
    robot.control_dofs_force(actions)
    scene.step()

    # Access state in batched form
    positions = robot.get_dofs_position()  # shape: (4096, n_dofs)
```

### 2.4 Domain Randomization (Sim-to-Real Bridge)

Domain randomization is the most effective technique for bridging the sim-to-real gap. Randomize visual and physical parameters so the policy generalizes to the real world.

```python
# MuJoCo domain randomization example
import mujoco
import numpy as np

def randomize_domain(model, data):
    """Randomize physical and visual parameters each episode."""
    # --- Physical randomization ---
    # Friction (geom_friction: [sliding, torsional, rolling])
    for geom_id in range(model.ngeom):
        model.geom_friction[geom_id] = np.random.uniform(0.3, 1.5, 3)

    # Joint damping
    for jnt_id in range(model.njnt):
        model.dof_damping[jnt_id] = np.random.uniform(0.01, 0.5)

    # Object mass
    model.body_mass[cube_body_id] = np.random.uniform(0.05, 0.3)

    # --- Visual randomization ---
    # Light intensity
    model.light_diffuse[:, :] = np.random.uniform(0.4, 1.0, (model.nlight, 3))

    # Camera position jitter (±2cm)
    model.cam_pos[:] += np.random.uniform(-0.02, 0.02, model.cam_pos.shape)

    # Background color
    model.geom_rgba[floor_geom_id] = np.random.uniform(0.1, 0.9, 4)

    mujoco.mj_forward(model, data)
```

```python
# Isaac Lab domain randomization (built-in, config-driven)
from isaaclab.managers import EventTerm as EventTerm
import isaaclab.utils.math as math_utils

@configclass
class MyRandomizationCfg:
    """Randomize at episode reset."""
    # Randomize joint positions and velocities
    reset_joint_pos = EventTerm(
        func=math_utils.sample_uniform,
        params={"lower": -0.1, "upper": 0.1},
    )
    # Randomize object pose
    reset_object_pose = EventTerm(
        func=math_utils.sample_uniform,
        params={
            "lower": [-0.1, -0.1, 0.0],
            "upper": [0.1, 0.1, 0.1],
        },
    )
```

---

## 3. Policy Training / 策略训练

### 3.1 Imitation Learning: Diffusion Policy

Diffusion Policy learns a conditional denoising process to generate action sequences. State-of-the-art for manipulation from visual + proprioceptive inputs.

```python
"""Diffusion Policy training with LeRobot."""
from lerobot.common.policies.diffusion.configuration_diffusion import DiffusionConfig
from lerobot.common.policies.diffusion.modeling_diffusion import DiffusionPolicy
from lerobot.common.datasets.lerobot_dataset import LeRobotDataset

# Load dataset
dataset = LeRobotDataset("lerobot/aloha_sim_transfer_cube_human")

# Configure and create policy
config = DiffusionConfig(
    input_shapes={
        "observation.images.top": (3, 480, 640),
        "observation.state": (14,),  # joint positions + velocities
    },
    output_shapes={"action": (14,)},
    n_obs_steps=2,            # observation history length
    n_action_steps=8,         # action chunk size
    horizon=16,               # diffusion prediction horizon
    n_diffusion_steps=100,    # DDPM steps (100 for training, 50 for inference)
    noise_scheduler_type="DDPM",
)

policy = DiffusionPolicy(config, dataset_stats=dataset.stats)

# Training loop
import torch
optimizer = torch.optim.Adam(policy.parameters(), lr=1e-4)

policy.train()
for epoch in range(100):
    for batch in dataset.dataloader:
        loss = policy.compute_loss(batch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if epoch % 10 == 0:
        print(f"Epoch {epoch}, Loss: {loss.item():.4f}")

# Save
policy.save_pretrained("outputs/diffusion_policy_checkpoint")
```

### 3.2 Imitation Learning: ACT (Action Chunking with Transformers)

ACT uses a CVAE (Conditional Variational AutoEncoder) + Transformer to predict action chunks. Excellent for bimanual manipulation.

```python
"""ACT policy with LeRobot."""
from lerobot.common.policies.act.configuration_act import ACTConfig
from lerobot.common.policies.act.modeling_act import ACTPolicy

config = ACTConfig(
    input_shapes={
        "observation.images.top": (3, 480, 640),
        "observation.images.wrist": (3, 480, 640),
        "observation.state": (14,),
    },
    output_shapes={"action": (14,)},
    n_obs_steps=1,
    n_action_steps=100,    # predict 100 actions ahead
    chunk_size=100,
    n_encoder_layers=4,
    dim_feedforward=3200,
    temporal_ensemble_coeff=0.01,  # exponential moving average for smooth actions
    kl_weight=10.0,
)

policy = ACTPolicy(config, dataset_stats=dataset.stats)
# ... training loop same as Diffusion Policy
```

**Diffusion Policy vs ACT — when to use which:**
| Aspect | Diffusion Policy | ACT |
|--------|-----------------|-----|
| Multi-modal actions | Better (inherent to diffusion) | Needs CVAE latent |
| Training speed | Slower (100 diffusion steps) | Faster (single forward pass) |
| Inference speed | ~100ms (can reduce steps) | ~10ms |
| Best for | Complex contact-rich tasks | Smooth trajectory tasks |

### 3.3 Reinforcement Learning with Stable-Baselines3

```python
"""PPO training for robotic manipulation in MuJoCo via Gymnasium."""
import gymnasium as gym
from stable_baselines3 import PPO, SAC
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import EvalCallback

# Create vectorized MuJoCo environment
env = make_vec_env(
    "gymnasium.envs.mujoco.HalfCheetah-v5",
    n_envs=4,
)

# PPO with tuned hyperparameters for robotics
model = PPO(
    "MlpPolicy",
    env,
    learning_rate=3e-4,
    n_steps=2048,
    batch_size=64,
    n_epochs=10,
    gamma=0.99,
    gae_lambda=0.95,
    clip_range=0.2,
    ent_coef=0.0,
    vf_coef=0.5,
    max_grad_norm=0.5,
    tensorboard_log="./logs/ppo_manipulation",
    verbose=1,
)

# Evaluation callback
eval_env = gym.make("gymnasium.envs.mujoco.HalfCheetah-v5")
eval_callback = EvalCallback(
    eval_env,
    best_model_save_path="./logs/best_model",
    log_path="./logs/eval",
    eval_freq=10000,
    n_eval_episodes=10,
)

# Train
model.learn(total_timesteps=1_000_000, callback=eval_callback)
model.save("ppo_manipulation_final")

# SAC for continuous control (often better for manipulation)
model_sac = SAC(
    "MlpPolicy",
    env,
    learning_rate=3e-4,
    buffer_size=1_000_000,
    batch_size=256,
    tau=0.005,
    ent_coef="auto",
    tensorboard_log="./logs/sac_manipulation",
)
model_sac.learn(total_timesteps=1_000_000)
```

### 3.4 VLA Fine-Tuning: OpenVLA

```python
"""Fine-tune OpenVLA for a custom robot task."""
import torch
from transformers import AutoModelForVision2Seq, AutoProcessor
from peft import LoraConfig, get_peft_model

# Load pretrained OpenVLA (7B parameters)
model_id = "openvla/openvla-7b"
processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)
model = AutoModelForVision2Seq.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    device_map="auto",  # auto-split across GPUs
)

# LoRA fine-tuning (memory-efficient)
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()  # ~0.1% of total

# Prepare dataset in OpenVLA format
# Each sample: {image: PIL.Image, instruction: str, action: np.ndarray}
# Actions are discretized into 256 bins per dimension

# Training with Hugging Face Trainer
from transformers import TrainingArguments, Trainer

training_args = TrainingArguments(
    output_dir="./openvla_finetuned",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    learning_rate=2e-5,
    bf16=True,
    num_train_epochs=10,
    logging_steps=50,
    save_strategy="epoch",
    gradient_checkpointing=True,
)

# Inference
prompt = "In: Pick up the red cube and place it on the shelf.\nOut:"
inputs = processor(prompt, image).to("cuda", dtype=torch.bfloat16)
action = model.predict_action(**inputs, unnorm_key="custom_robot")
```

### 3.5 Pi0 / OpenPI (Flow-Matching VLA)

```python
"""Pi0 inference with OpenPI — flow-matching VLA for dexterous manipulation."""
from openpi.client import Client

# Connect to Pi0 inference server (or run locally)
client = Client()

# Provide image observation + language instruction
observation = {
    "image": current_camera_frame,          # numpy array (H, W, 3)
    "wrist_image": current_wrist_frame,     # optional second view
    "state": robot_joint_positions,         # numpy array (n_dofs,)
}

instruction = "Pick up the mug by the handle and place it in the sink"

# Get action chunk via flow matching
action_chunk = client.infer(
    observation=observation,
    instruction=instruction,
    model="pi0_base",  # or "pi0_fast"
)

# action_chunk: numpy array (chunk_size, action_dim)
# Execute on robot with temporal ensembling
for action in action_chunk:
    robot.send_command(action)
```

### 3.6 Sim-to-Real Transfer Strategy

Sim-to-real is the critical bottleneck in deploying learned policies. Use a layered approach:

**Layer 1: Domain Randomization (essential)**
```python
randomization_ranges = {
    # Physical parameters
    "joint_damping": (0.01, 0.5),
    "joint_friction": (0.01, 0.2),
    "object_mass": (0.05, 0.5),
    "object_friction": (0.3, 1.5),
    "gripper_force": (0.5, 2.0),

    # Visual parameters
    "light_intensity": (0.3, 1.5),
    "light_position": ((-2, -2, 1), (2, 2, 4)),
    "camera_position_noise": (0.0, 0.02),    # meters
    "camera_rotation_noise": (0.0, 2.0),     # degrees
    "background_color": ((0.0, 0.0, 0.0), (1.0, 1.0, 1.0)),
    "object_color_range": "full_hsv",        # randomize object appearance
}
```

**Layer 2: System Identification (recommended)**
```python
"""Match simulation parameters to real robot measurements."""
import numpy as np
from scipy.optimize import minimize

def system_id_loss(sim_params):
    """Minimize difference between real and simulated trajectories."""
    damping, friction, mass = sim_params
    # Run simulation with these params
    sim_trajectory = run_sim(damping, friction, mass)
    # Compare to recorded real robot trajectory
    loss = np.mean((sim_trajectory - real_trajectory) ** 2)
    return loss

result = minimize(system_id_loss, x0=[0.1, 0.05, 0.1], bounds=[
    (0.001, 1.0), (0.001, 0.5), (0.01, 1.0)
])
```

**Layer 3: Online Adaptation (advanced)**
- Collect a small number of real-world trajectories (~50-100)
- Fine-tune the sim-trained policy on real data
- Use LeRobot's data format for seamless integration

---

## 4. Data & Datasets / 数据与数据集

### 4.1 Open X-Embodiment Dataset

The largest multi-robot manipulation dataset — 1M+ trajectories from 22 robot types.

```python
"""Download and use Open X-Embodiment data."""
# Via Hugging Face Datasets
from datasets import load_dataset

# Full dataset (large, ~1.5TB)
ds = load_dataset("google-research-datasets/open_x_embodiment", "default",
                   streaming=True)

# Specific robot subset (smaller)
ds_bridge = load_dataset("google-research-datasets/open_x_embodiment",
                          "bridge_dataset", streaming=True)

# Inspect a sample
sample = next(iter(ds["train"]))
print(f"Keys: {list(sample.keys())}")
# observation/image, observation/state, action, language_instruction
```

### 4.2 Key Datasets Summary

| Dataset | Trajectories | Robots | Tasks | Access |
|---------|-------------|--------|-------|--------|
| Open X-Embodiment | 1M+ | 22 types | Manipulation | HuggingFace |
| DROID | 76K | Franka | Kitchen tasks | HuggingFace |
| BridgeData V2 | 78K | WidowX | Tabletop | Google Cloud |
| RT-1 | 130K | 13 robots | Pick/place | Google |
| ALOHA (sim+real) | ~1K | ALOHA | Bimanual | LeRobot Hub |
| LeRobot Community | Growing | Many | Various | `lerobot/` on HF Hub |

### 4.3 LeRobot Dataset Format

Standard format for interoperability across the ecosystem:

```python
"""Create a LeRobot-format dataset from scratch."""
from lerobot.common.datasets.lerobot_dataset import LeRobotDataset
from lerobot.common.datasets.utils import Episode

# Define dataset features
features = {
    "observation.images.top": {
        "dtype": "image",
        "shape": (480, 640, 3),
        "names": ["height", "width", "channels"],
    },
    "observation.state": {
        "dtype": "float32",
        "shape": (14,),
        "names": ["state"],
    },
    "action": {
        "dtype": "float32",
        "shape": (14,),
        "names": ["action"],
    },
}

# Create and populate dataset
dataset = LeRobotDataset.create(
    repo_id="myusername/my_robot_task",
    features=features,
    fps=30,
    robot_type="koch_v1.1",
)

# Add episodes from recorded data
for episode_data in recorded_episodes:
    dataset.add_episode(episode_data)

# Push to Hub for sharing
dataset.push_to_hub()
```

### 4.4 Teleoperation Data Collection

```python
"""ALOHA teleoperation data collection via LeRobot."""
from lerobot.common.robot_devices.robots.manipulator_robot import ManipulatorRobot
from lerobot.common.robot_devices.motors.dynamixel import DynamixelMotorsBus

# Connect to ALOHA leader (teleoperation master) and follower (slave)
leader = DynamixelMotorsBus(port="/dev/ttyUSB0", motors={"shoulder": (1, "xl430-w250")})
follower = DynamixelMotorsBus(port="/dev/ttyUSB1", motors={"shoulder": (1, "xl430-w250")})

robot = ManipulatorRobot(
    leader_arms={"main": leader},
    follower_arms={"main": follower},
    cameras={"top": "path/to/camera_config"},
)

# Record episode
robot.connect()
episode = robot.teleop_step(record_data=True)
# Returns dict with observation.images.top, observation.state, action

# Use LeRobot's recording script for full pipeline:
# python lerobot/scripts/control_robot.py record \
#   --robot-path lerobot/configs/robot/aloha.yaml \
#   --fps 30 \
#   --root data \
#   --repo-id myuser/aloha_task \
#   --tags aloha tutorial \
#   --warmup-time-s 5 \
#   --episode-time-s 30 \
#   --reset-time-s 10 \
#   --num-episodes 50
```

**Gello teleoperation** (alternative, uses a miniature physical replica):
```bash
# Install Gello
git clone https://github.com/wuphilipp/gello_mechanical.git
cd gello_mechanical
pip install -e .

# Record with Gello + LeRobot integration
python gello_agent.py --robot franka --save-dir ./data/gello_episodes
```

---

## 5. Deployment / 部署

### 5.1 LeRobot Inference Pipeline

```python
"""Deploy a trained policy on real hardware with LeRobot."""
from lerobot.common.policies.diffusion.modeling_diffusion import DiffusionPolicy
from lerobot.common.robot_devices.robots.manipulator_robot import ManipulatorRobot
import torch

# Load trained policy
policy = DiffusionPolicy.from_pretrained("outputs/diffusion_policy_checkpoint")
policy.eval()
policy.to("cuda")

# Connect to robot
robot = ManipulatorRobot.from_config("lerobot/configs/robot/koch.yaml")
robot.connect()

# Inference loop
observation_queue = []
action_buffer = []

while True:
    # Get current observation
    obs = robot.capture_observation()

    # Stack observation history (policy expects n_obs_steps frames)
    observation_queue.append(obs)
    if len(observation_queue) > policy.config.n_obs_steps:
        observation_queue.pop(0)

    # Predict action chunk when buffer is empty
    if len(action_buffer) == 0:
        batch = {
            "observation.images.top": torch.tensor(obs["images"]["top"]).unsqueeze(0),
            "observation.state": torch.tensor(obs["state"]).unsqueeze(0),
        }
        with torch.inference_mode():
            actions = policy.select_action(batch)  # (1, chunk_size, action_dim)
        action_buffer = list(actions.squeeze(0).cpu().numpy())

    # Execute next action
    action = action_buffer.pop(0)
    robot.send_action(action)
```

### 5.2 ROS2 Bridge for Real Robot Control

```python
"""Bridge between LeRobot policy and ROS2 robot control."""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState, Image
from std_msgs.msg import Float64MultiArray
from cv_bridge import CvBridge
import numpy as np

class RobotPolicyBridge(Node):
    def __init__(self, policy):
        super().__init__("policy_bridge")
        self.policy = policy
        self.bridge = CvBridge()

        # Subscribe to robot state
        self.state_sub = self.create_subscription(
            JointState, "/joint_states", self.state_callback, 10)

        # Subscribe to camera
        self.cam_sub = self.create_subscription(
            Image, "/camera/color/image_raw", self.image_callback, 10)

        # Publish actions
        self.cmd_pub = self.create_publisher(
            Float64MultiArray, "/joint_trajectory_controller/joint_commands", 10)

        self.current_state = None
        self.current_image = None

    def state_callback(self, msg):
        self.current_state = np.array(msg.position, dtype=np.float32)

    def image_callback(self, msg):
        self.current_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")

    def run_policy(self):
        if self.current_state is None or self.current_image is None:
            return

        obs = {
            "observation.images.top": self.current_image,
            "observation.state": self.current_state,
        }
        action = self.policy.predict(obs)

        msg = Float64MultiArray()
        msg.data = action.tolist()
        self.cmd_pub.publish(msg)

# Usage
rclpy.init()
node = RobotPolicyBridge(policy=loaded_policy)
rate = node.create_rate(30)  # 30 Hz
while rclpy.ok():
    rclpy.spin_once(node, timeout_sec=0)
    node.run_policy()
    rate.sleep()
```

### 5.3 ONNX / TensorRT Export for Edge Deployment

```python
"""Export policy to ONNX for edge deployment (Jetson, Raspberry Pi)."""
import torch
import onnxruntime as ort

# Export PyTorch policy to ONNX
dummy_obs = {
    "observation.images.top": torch.randn(1, 3, 480, 640),
    "observation.state": torch.randn(1, 14),
}

torch.onnx.export(
    policy,
    (dummy_obs,),
    "policy.onnx",
    input_names=["image", "state"],
    output_names=["action"],
    dynamic_axes={"image": {0: "batch"}, "state": {0: "batch"}, "action": {0: "batch"}},
    opset_version=17,
)

# Convert ONNX to TensorRT (for NVIDIA Jetson, 2-5x speedup)
import tensorrt as trt

logger = trt.Logger(trt.Logger.INFO)
builder = trt.Builder(logger)
network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))
parser = trt.OnnxParser(network, logger)

with open("policy.onnx", "rb") as f:
    parser.parse(f.read())

config = builder.create_builder_config()
config.set_flag(trt.BuilderFlag.FP16)  # FP16 for edge devices

engine = builder.build_serialized_network(network, config)
with open("policy.engine", "wb") as f:
    f.write(engine)

# Run inference with TensorRT runtime
runtime = trt.Runtime(logger)
engine = runtime.deserialize_cuda_engine(open("policy.engine", "rb").read())
context = engine.create_execution_context()
# ... allocate buffers and run
```

---

## 6. Debugging & Visualization / 调试与可视化

### 6.1 MuJoCo Interactive Viewer

```python
"""Interactive MuJoCo viewer for debugging scenes and controllers."""
import mujoco
import mujoco.viewer

model = mujoco.MjModel.from_xml_path("robot_task.xml")
data = mujoco.MjData(model)

# Launch interactive viewer (GUI)
# Use mouse to orbit/zoom, keyboard shortcuts for pause/step
with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        mujoco.mj_step(model, data)
        viewer.sync()
```

```python
# Programmatic control with viewer
def controller_callback(model, data):
    """Custom controller called at each timestep."""
    # Example: PD controller to target joint positions
    target = np.array([0, -0.785, 0, -2.356, 0, 1.571, 0.785])
    kp = np.array([100, 100, 100, 100, 50, 50, 50])
    kd = np.array([10, 10, 10, 10, 5, 5, 5])
    error = target - data.qpos[:7]
    data.ctrl[:7] = kp * error - kd * data.qvel[:7]

with mujoco.viewer.launch_passive(model, data, key_callback=controller_callback) as viewer:
    while viewer.is_running():
        controller_callback(model, data)
        mujoco.mj_step(model, data)
        viewer.sync()
```

### 6.2 Isaac Sim GUI and Headless Modes

```bash
# Launch Isaac Sim with GUI (for scene debugging)
python scripts/run_scene.py --headless 0

# Headless mode (for training on remote servers)
python scripts/train.py --headless --num-envs 1024

# Enable live-streaming of headless rendering
# Set environment variable for WebRTC streaming:
export ISAAC_LIVESTREAM=1  # enables browser-based viewer
```

### 6.3 Rerun.io for Multi-Modal Logging

```python
"""Log robot state, images, and policy outputs to Rerun for debugging."""
import rerun as rr
import numpy as np

rr.init("embodied_intelligence_debug", spawn=True)

for step, (obs, action, reward) in enumerate(rollout_data):
    # Log camera image
    rr.log("camera/top", rr.Image(obs["image"]))

    # Log robot joint state
    rr.log("robot/joints", rr.Scalar(action.tolist()))

    # Log end-effector trajectory (3D points)
    ee_positions = compute_ee_trajectory(obs["state"])
    rr.log("robot/end_effector", rr.Points3D(ee_positions, radii=0.005))

    # Log reward curve
    rr.log("training/reward", rr.Scalar(reward))

    # Log action prediction vs ground truth
    rr.log("policy/predicted", rr.Scalar(action[0]))
    rr.log("policy/ground_truth", rr.Scalar(gt_action[0]))
```

### 6.4 Policy Rollout Evaluation

```python
"""Evaluate policy success rate across multiple rollouts."""
import numpy as np

def evaluate_policy(env, policy, n_episodes=100, max_steps=500):
    """Run policy rollouts and compute success rate metrics."""
    successes = []
    returns = []
    episode_lengths = []

    for ep in range(n_episodes):
        obs, _ = env.reset()
        total_reward = 0
        success = False

        for step in range(max_steps):
            action = policy.predict(obs)
            obs, reward, terminated, truncated, info = env.step(action)
            total_reward += reward

            if "is_success" in info and info["is_success"]:
                success = True
                break

            if terminated or truncated:
                break

        successes.append(success)
        returns.append(total_reward)
        episode_lengths.append(step + 1)

    results = {
        "success_rate": np.mean(successes),
        "mean_return": np.mean(returns),
        "std_return": np.std(returns),
        "mean_episode_length": np.mean(episode_lengths),
        "n_episodes": n_episodes,
    }

    print(f"Success Rate: {results['success_rate']:.1%}")
    print(f"Mean Return:  {results['mean_return']:.2f} ± {results['std_return']:.2f}")
    print(f"Mean Length:  {results['mean_episode_length']:.0f} steps")

    return results

# Run evaluation
results = evaluate_policy(env, policy, n_episodes=100)

# Sim-to-real evaluation: run same policy on real robot
# Record success/failure per task attempt, compare to sim results
# Target: real-world success rate ≥ 80% of simulated success rate
```

---

## 7. Key Patterns / 最佳实践

### Start Simple, Scale Up
Always begin with a simple task before complex manipulation:
1. **Reach** — move end-effector to a 3D target (validates state/action spaces)
2. **Push** — slide an object to a goal (tests contact dynamics)
3. **Pick** — grasp and lift an object (tests gripper control)
4. **Place** — pick and place at target location (tests sequential reasoning)
5. **Complex manipulation** — stacking, insertion, tool use

### Tool Selection Guide
| Scenario | Recommended Tool | Why |
|----------|-----------------|-----|
| Quick prototyping | LeRobot + MuJoCo | Fastest iteration, Hub datasets |
| Large-scale RL training | Isaac Lab (1024+ envs) | GPU-parallel, built-in PPO |
| Massively parallel (4096+ envs) | Genesis | 10-80x faster than MuJoCo |
| Visual sim2real | Isaac Sim | Photorealistic RTX rendering |
| Language-conditioned tasks | OpenVLA / Pi0 | Pre-trained VLA + fine-tune |
| Bimanual manipulation | LeRobot + ACT | ALOHA ecosystem, proven results |
| Data collection | LeRobot recorder | Standard format, Hub integration |

### Data Collection Best Practices
- Record all teleoperation data in LeRobot format for interoperability
- Collect at least 50 episodes for imitation learning (ACT/Diffusion)
- Collect 200+ episodes for robust sim-to-real transfer
- Vary object poses, lighting, and camera angles during collection
- Include failure recovery demonstrations (teach the policy to recover from mistakes)

### Sim-to-Real Checklist
Before deploying a sim-trained policy on real hardware:
- [ ] Match camera intrinsics (FOV, resolution) between sim and real
- [ ] Match lighting conditions (intensity, direction, color temperature)
- [ ] Calibrate friction coefficients via system identification
- [ ] Add camera position/angle noise in simulation (±2cm, ±5 degrees)
- [ ] Randomize object appearance (color, texture, size) in simulation
- [ ] Test policy in sim with worst-case randomization parameters
- [ ] Verify action space bounds match real robot limits
- [ ] Add safety bounds on joint velocities and forces

---

## 8. Pitfalls / 常见陷阱

### MuJoCo
- **MJCF vs URDF coordinate frames:** MuJoCo uses Z-up by default; some URDFs assume Y-up or different conventions. Always verify with a test render before trusting joint angles.
- **Timestep sensitivity:** `timestep=0.002` works for most tasks; contact-rich manipulation may need `0.001` or lower. Using too-large timesteps causes tunneling (objects passing through each other).
- **Implicit vs explicit integrators:** Use `integrator="implicitfast"` for stable contact. Default explicit Euler can explode with stiff contacts.

### Isaac Sim
- **GPU requirement:** Requires NVIDIA GPU with RTX support (Turing+). Will not run on integrated graphics or AMD GPUs.
- **First launch is slow:** First-time startup downloads/shaders can take 10-30 minutes. Subsequent launches are faster.
- **Memory management:** Each parallel environment consumes VRAM. Monitor with `nvidia-smi`; 512 envs typically needs 12GB+ VRAM.
- **Omniverse dependency:** Isaac Sim depends on NVIDIA Omniverse. Version mismatches between Isaac Sim and Isaac Lab cause cryptic import errors — always check the compatibility matrix.

### VLA Models
- **VRAM requirements:** OpenVLA (7B) needs 24GB+ for inference, 48GB+ for fine-tuning. Use 4-bit quantization (`bitsandbytes`) to reduce to 8GB for inference.
- **Action discretization:** OpenVLA discretizes continuous actions into 256 bins. This quantization can hurt precision for fine manipulation — evaluate if it matters for your task.
- **Prompt sensitivity:** VLA models are sensitive to instruction wording. "Pick up the red block" vs "grasp the red cube" can produce different behaviors. Be consistent.

### Real Robot Safety
- **ALWAYS have a physical emergency stop button** within arm's reach during testing
- **Start with reduced speed/force** (20% of max) when first deploying a new policy
- **Add software joint limits** tighter than hardware limits as a safety margin
- **Log everything** — camera images, joint states, actions, torques — for post-mortem analysis
- **Never leave the robot unattended** during initial policy deployment
- **Use a safety cage or soft barriers** when testing manipulation with objects that could be thrown

### Data Collection
- **Teleoperation drift:** Leader arm calibration drifts over time. Re-calibrate every 10-20 episodes.
- **Camera sync:** Ensure camera timestamps are synchronized with robot state. Mismatched timestamps cause the policy to learn wrong state-action associations.
- **Action space mismatch:** Ensure the action space used during data collection exactly matches what the policy outputs. Common bug: collecting in absolute joint positions but policy predicts delta actions.

---

## 9. Verification / 验证

Run these checks to confirm your environment is properly set up:

```bash
# 1. MuJoCo core
python -c "import mujoco; m=mujoco.MjModel.from_xml_string('<mujoco/>'); print('MuJoCo OK')"

# 2. MuJoCo MJX (GPU)
python -c "import mujoco.mjx; print('MJX (GPU) OK')"

# 3. Gymnasium MuJoCo envs
python -c "import gymnasium as gym; env=gym.make('HalfCheetah-v5'); print(f'Gymnasium MuJoCo OK, action_dim={env.action_space.shape}')"

# 4. LeRobot
python -c "from lerobot.common.datasets.lerobot_dataset import LeRobotDataset; print('LeRobot OK')"

# 5. Isaac Lab (if installed)
python -c "from isaaclab.envs import ManagerBasedRLEnv; print('Isaac Lab OK')"

# 6. Genesis (if installed)
python -c "import genesis as gs; gs.init(); print('Genesis OK')"

# 7. Stable-Baselines3
python -c "from stable_baselines3 import PPO; print('SB3 OK')"

# 8. Rerun (visualization)
python -c "import rerun as rr; print(f'Rerun {rr.__version__} OK')"

# 9. End-to-end MuJoCo render test
python -c "
import mujoco, numpy as np
m = mujoco.MjModel.from_xml_string('''
<mujoco>
  <worldbody>
    <light diffuse='.5 .5 .5' pos='0 0 3' dir='0 0 -1'/>
    <geom type='plane' size='1 1 0.1' rgba='1 0.8 0.6 1'/>
    <body pos='0 0 0.1'>
      <joint type='free'/>
      <geom type='box' size='.05 .05 .05' rgba='0 0.7 0.1 1'/>
    </body>
  </worldbody>
</mujoco>
''')
d = mujoco.MjData(m)
r = mujoco.Renderer(m, 480, 640)
mujoco.mj_forward(m, d)
r.update_scene(d)
img = r.render()
assert img.shape == (480, 640, 3), f'Unexpected shape: {img.shape}'
print(f'Render OK: {img.shape}, dtype={img.dtype}')
"
```

---

## 10. Reference Architecture / 参考架构

```
embodied-intelligence-project/
├── sim/
│   ├── mujoco/
│   │   ├── robot_task.xml          # MJCF scene definition
│   │   ├── meshes/                 # STL/OBJ robot meshes
│   │   └── env.py                  # Gymnasium wrapper
│   ├── isaac_lab/
│   │   ├── env_cfg.py              # Isaac Lab environment config
│   │   └── train.py                # RL training script
│   └── genesis/
│       └── parallel_env.py         # Genesis parallel setup
├── policies/
│   ├── diffusion/
│   │   ├── config.yaml
│   │   ├── train.py
│   │   └── evaluate.py
│   ├── act/
│   │   ├── config.yaml
│   │   └── train.py
│   ├── rl/
│   │   ├── ppo_train.py
│   │   └── sac_train.py
│   └── vla/
│       ├── finetune_openvla.py
│       └── infer_pi0.py
├── data/
│   ├── teleop_recordings/          # LeRobot-format episodes
│   └── datasets/                   # Downloaded datasets
├── deployment/
│   ├── inference_server.py         # Policy serving
│   ├── ros2_bridge.py              # ROS2 integration
│   └── export_onnx.py             # Edge export
├── eval/
│   ├── rollout.py                  # Sim evaluation
│   └── real_robot_test.py          # Real robot eval
├── configs/
│   ├── robot/                      # Robot hardware configs
│   ├── task/                       # Task definitions
│   └── training/                   # Training hyperparams
└── notebooks/
    ├── 01_explore_dataset.ipynb
    ├── 02_visualize_sim.ipynb
    └── 03_analyze_rollouts.ipynb
```

---

## 11. Key References / 核心参考

| Paper / Resource | Key Contribution |
|------------------|-----------------|
| Diffusion Policy (Chi et al., 2023) | Denoising-based action generation for manipulation |
| ACT (Zhao et al., 2023) | Action Chunking with Transformers + CVAE |
| ALOHA (Zhao et al., 2023) | Low-cost bimanual teleoperation + imitation learning |
| OpenVLA (Kim et al., 2024) | 7B VLA model, fine-tunable on DROID/custom data |
| Pi0 (Black et al., 2024) | Flow-matching VLA for dexterous manipulation |
| RT-2 (Brohan et al., 2023) | VLM → VLA, language-conditioned robotics |
| Open X-Embodiment (2023) | 1M+ trajectory multi-robot dataset |
| LeRobot | Unified robotics framework by Hugging Face |
| Isaac Lab (2024) | NVIDIA's RL framework for Isaac Sim |
| Genesis (2024) | Taichi-based ultra-fast parallel simulator |
