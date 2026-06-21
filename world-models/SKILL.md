---
name: world-models
description: Build world models with DreamerV3, V-JEPA, I-JEPA, NVIDIA Cosmos, Diamond. Covers latent dynamics models, video prediction, environment simulation, and using world models for RL/planning. Use when working with world simulation, video generation as world models, or model-based RL.
version: 1.0.0
---

# World Models (世界模型)

## Environment Setup (环境配置)

### DreamerV3 / DreamerV4
```bash
git clone https://github.com/danijar/dreamerv3.git
cd dreamerv3 && pip install -e .
# DreamerV4: real-time interactive inference on single GPU
# Learns Minecraft purely from offline data
```

### I-JEPA / V-JEPA 2 (Meta)
```bash
git clone https://github.com/facebookresearch/jepa.git
cd jepa && pip install -r requirements.txt
# I-JEPA: image-based, predict masked patches in latent space
# V-JEPA 2: video+audio, spatiotemporal prediction (fully open-sourced)
```

### Diamond (Diffusion World Model)
```bash
git clone https://github.com/eloialonso/diamond.git
cd diamond && pip install -e .
# Matches human performance on Atari with diffusion-based world model
```

### NVIDIA Cosmos
```bash
pip install nvidia-cosmos
# World foundation model bridging to Isaac Lab for robot training
```

### Genesis (Fast Physics Simulation)
```bash
pip install genesis-world
# 10-80x faster than MuJoCo for parallel simulation
```

## Core Architectures (核心架构)

### RSSM (Recurrent State-Space Model) — DreamerV3
```
Encoder: obs_t -> CNN/ViT -> stochastic (z_t) + deterministic (h_t)
Dynamics: h_t, z_t, a_t -> predict h_{t+1}, z_{t+1}
Reward: h_t, z_t -> predict r_t
Actor: h_t, z_t -> action a_t (trained in imagined rollouts)
Critic: h_t, z_t -> value V_t
```

Key: Symlog reward prediction, free bits KL, unimix categorical, scales Atari->Minecraft without tuning.

### JEPA (Joint Embedding Predictive Architecture)
```
I-JEPA: visible patches -> representations; EMA target encoder; predict masked target repr
        NO negative pairs (unlike MAE, BYOL)
V-JEPA 2: extends to video + audio; spatiotemporal masking in latent space
```

### Diamond (Diffusion World Model)
```
Given: (s_t, a_t, ..., a_{t+k-1})
Predict: s_{t+1}, ..., s_{t+k} via iterative denoising
Training: add noise to future frames, denoise conditioned on actions
Planning: generate many rollouts, pick best action sequence
```

## Training Pipeline (训练流程)

### DreamerV3 Workflow
```python
from dreamerv3 import api

env = api.make_env('atari', task='pong')
config = api.defaults.update({'batch_size': 16, 'run.steps': 1e6})
agent = api.Agent(env, config)

# 1. Pretrain world model
agent.train(steps=100_000)
# 2. Train actor-critic in imagination
agent.train_actor_critic(steps=500_000)
# 3. Evaluate
agent.eval(episodes=10)
```

### V-JEPA Pretraining
```python
from jepa.models.vjepa2 import VideoJEPA2

model = VideoJEPA2(
    patch_size=(2, 16, 16),
    embed_dim=1024, depth=24, num_heads=16,
    predictor_embed_dim=4096, predictor_depth=12,
)
# Train: mask spatiotemporal tubes, predict in latent space
# Datasets: Something-Something V2, Kinetics, Epic-Kitchen
```

## Key Benchmarks (基准测试)

| Benchmark | Description | Top Models | Metric |
|-----------|-------------|-----------|--------|
| Atari 100k | 2M frames, sample-efficient RL | Diamond, DreamerV3 | HNS |
| Crafter | Open-world survival, 22 achievements | DreamerV3 | Reward |
| DMControl | Continuous control, 6 tasks | DreamerV3, TD-MPC2 | Return |
| MineDojo/VPT | Minecraft, 70k hrs | VPT, DreamerV3 | Completion |
| Procgen | Procedural generalization | DreamerV3 | Test return |

## Integration with RL (强化学习集成)

### Model-Based RL Pipeline
```
1. Collect data: (s_t, a_t, r_t, s_{t+1})
2. Train dynamics model: predict s_{t+1}, r_{t+1}
3. Train policy in imagined rollouts (H steps)
4. Execute policy in real environment, add to buffer
5. Repeat
```

### Model-Predictive Control
```python
def mpc_planning(world_model, state, horizon=10, n_samples=1000):
    best_action, best_return = None, -float('inf')
    for _ in range(n_samples):
        actions = sample_action_sequence(horizon)
        states = world_model.rollout(state, actions)
        ret = compute_return(states)
        if ret > best_return:
            best_return = ret
            best_action = actions[0]
    return best_action
```

### World Model as Reward Model
```python
class WorldModelReward:
    def __init__(self, world_model, target_state):
        self.wm = world_model
        self.target = target_state

    def reward(self, state, action):
        predicted = self.wm.predict(state, action)
        return -torch.norm(predicted - self.target)
```

## Evaluation (评估方法)

### Reconstruction Quality
- **FVD** (Frechet Video Distance): gold standard for video generation quality
- **PSNR / SSIM / LPIPS**: per-frame metrics
- **Diversity + temporal coherence**: beyond FVD

### Planning Ability
- Success rate in imagined rollouts
- Compare real vs imagined trajectory similarity

### Sample Efficiency
- Learning curves: episodes vs reward
- Compare against model-free baselines (PPO, SAC)

## Visualization (可视化)

### Dream Sequences
```python
# Render imagined future frames
imagined = agent.imagine_horizon(start_state, horizon=50)
frames = [render_state(s) for s in imagined]
# Save as GIF
```

### Latent Space
```python
from sklearn.manifold import TSNE
embedded = TSNE(n_components=2).fit_transform(latent_states)
plt.scatter(embedded[:, 0], embedded[:, 1], c=rewards, cmap='viridis')
```

### Real vs Imagined
- Side-by-side comparison of real environment frames vs world model predictions
- Helps diagnose hallucination and compounding errors

## Key Papers & Resources (关键论文)

| Paper | Year | Contribution | Code |
|-------|------|-------------|------|
| DreamerV3 | 2023 | RSSM + symlog + free bits | github.com/danijar/dreamerv3 |
| I-JEPA | 2023 | Latent prediction, no negatives | github.com/facebookresearch/ijepa |
| V-JEPA 2 | 2024 | Video+audio, fully open | github.com/facebookresearch/jepa |
| Diamond | 2024 | Diffusion world model, Atari SOTA | github.com/eloialonso/diamond |
| DreamerV4 | 2025 | Real-time, offline data | danijar.com/project/dreamer4 |
| NVIDIA Cosmos | 2025 | World foundation for robotics | github.com/NVIDIA/Cosmos |
| UniSim | 2023 | Universal simulator | — |
| GAIA-1 | 2023 | AD world model (Wayve) | — |
| Genie 2 | 2024 | Interactive 3D (DeepMind) | — |

## Pitfalls (常见陷阱)

- World models hallucinate — always validate with real environment rollouts
- FVD alone insufficient; check diversity and physical plausibility
- DreamerV3 hyperparameters (horizon, batch size, KL coeff) need tuning for new domains
- Diffusion models slow at inference; use DDIM or flow matching
- V-JEPA pretrained weights large (ViT-L/H); need multi-GPU
- Long-horizon predictions accumulate compounding errors
- Distribution shift: model trained on one policy may not generalize
- Reward hacking: agent exploits world model inaccuracies

## Verification (验证)

```bash
python -c "from dreamerv3 import api; print('DreamerV3 OK')"
python -c "import genesis as gs; print('Genesis', gs.__version__)"
python -c "import torch; print(f'PyTorch {torch.__version__}, CUDA: {torch.cuda.is_available()}')"
```
