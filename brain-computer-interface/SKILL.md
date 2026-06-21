---
name: brain-computer-interface
description: Build BCI systems with MNE-Python, BrainFlow, MOABB, Braindecode. Covers EEG/MEG signal processing, neural decoding, BCI paradigms (P300/SSVEP/motor imagery), Riemannian classification, and real-time BCI applications. Use when working with brain signals, EEG data, or neural interfaces.
version: 1.0.0
---

# Brain-Computer Interface (脑机接口)

## Environment Setup (环境配置)

### Core Libraries
```bash
# Signal processing
pip install mne mne-bids mne-connectivity mne-icalabel

# Hardware-agnostic acquisition
pip install brainflow

# Benchmark framework (30+ datasets)
pip install moabb

# Deep learning for EEG
pip install braindecode

# Riemannian geometry classifiers
pip install pyriemann

# Artifact correction
pip install autoreject meegkit

# Visualization
pip install mne-qt-browser
```

### Optional
```bash
pip install eeglabio          # EEGLAB interop
pip install yasa               # Sleep spindle/slow-wave analysis
pip install antropy            # Signal complexity measures
pip install neurodsp           # NeuroDSP time-series tools
pip install fooof              # FOOOF spectral parameterization
```

### Device-Specific (via BrainFlow)
```python
from brainflow.board_shim import BoardShim, BrainFlowInputParams
params = BrainFlowInputParams()
params.serial_port = 'COM3'       # OpenBCI
# params.mac_address = 'XX:XX'    # Muse BLE
# params.ip_address = '192.168.1.100'  # g.tec, ANT
board = BoardShim(board_id, params)  # board_id: 0=Cyton, 1=Ganglion, etc.
```

## Signal Acquisition & Preprocessing (信号采集与预处理)

### BrainFlow Streaming
```python
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds

params = BrainFlowInputParams()
board = BoardShim(BoardIds.CYTON_BOARD.value, params)
board.prepare_session()
board.start_stream(45000)  # ring buffer size

import time; time.sleep(10)  # collect 10 seconds
data = board.get_board_data()
board.stop_stream()
board.release_session()
```

### MNE-Python Preprocessing Pipeline
```python
import mne

# Load raw data (EDF, BDF, FIF, BrainVision, etc.)
raw = mne.io.read_raw_edf('subject.edf', preload=True)

# Basic info
print(raw.info)
raw.plot_psd(fmax=50)

# Filtering
raw.filter(l_freq=1.0, h_freq=40.0)        # bandpass
raw.notch_filter(freqs=[50], picks='eeg')   # 50Hz line noise (use 60 for US)

# Bad channel detection & interpolation
raw.info['bads'] = ['Fp1', 'T7']  # mark bad channels
raw.interpolate_bads()

# Re-reference
raw.set_eeg_reference('average')

# ICA for artifact removal
from mne.preprocessing import ICA
ica = ICA(n_components=20, random_state=42)
ica.fit(raw)
# Auto-detect EOG artifacts
eog_indices, eog_scores = ica.find_bads_eog(raw)
ica.exclude = eog_indices
raw_clean = ica.apply(raw.copy())

# Epoching
events = mne.find_events(raw, stim_channel='STI 014')
epochs = mne.Epochs(raw_clean, events, event_id={'left': 1, 'right': 2},
                    tmin=-0.5, tmax=1.0, baseline=(None, 0),
                    reject=dict(eeg=100e-6))  # reject epochs >100uV

# Auto-reject with autoreject
import autoreject
ar = autoreject.AutoReject()
epochs_clean = ar.fit_transform(epochs)
```

### BIDS Format
```python
import mne_bids
bids_path = mne_bids.BIDSPath(subject='01', session='01', task='motorimagery',
                               datatype='eeg', root='./bids_root')
mne_bids.write_raw_bids(raw, bids_path, overwrite=True)
```

## BCI Paradigms (BCI范式)

### Motor Imagery (运动想象)
```python
# CSP (Common Spatial Patterns)
from mne.decoding import CSP
csp = CSP(n_components=6, reg=None, log=True, norm_trace=False)
X_csp = csp.fit_transform(epochs_data, labels)

# Classification
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import cross_val_score
lda = LinearDiscriminantAnalysis()
scores = cross_val_score(lda, X_csp, labels, cv=5)
print(f'CSP+LDA accuracy: {scores.mean():.3f} +/- {scores.std():.3f}')

# Riemannian approach (often better on small datasets)
from pyriemann.estimation import Covariances
from pyriemann.classification import MDM
covs = Covariances(estimator='lwf').fit_transform(epochs_data)
mdm = MDM(metric=dict(mean='riemann', distance='riemann'))
scores_r = cross_val_score(mdm, covs, labels, cv=5)
print(f'Riemannian MDM accuracy: {scores_r.mean():.3f}')

# Tangent Space + SVM (state-of-the-art for MI)
from pyriemann.tangentspace import TangentSpace
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
ts_svm = make_pipeline(
    Covariances('lwf'),
    TangentSpace(metric='riemann'),
    SVC(kernel='linear')
)
scores_ts = cross_val_score(ts_svm, epochs_data, labels, cv=5)
```

### P300 (事件相关电位)
```python
# Epoch extraction
epochs_p300 = mne.Epochs(raw, events, event_id={'target': 1, 'nontarget': 2},
                          tmin=0, tmax=0.8, baseline=(0, 0.1))

# xDAVER / Stepwise LDA
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

clf = make_pipeline(StandardScaler(), LogisticRegression())
# Train on averaged epochs per trial
scores = cross_val_score(clf, X_epochs, y_labels, cv=5)

# Channel selection for P300: Pz, Cz, Fz, P3, P4 are key
picks_p300 = mne.pick_channels(epochs_p300.ch_names, ['Pz', 'Cz', 'Fz', 'P3', 'P4'])
```

### SSVEP (稳态视觉诱发电位)
```python
import numpy as np
from scipy.signal import welch

def cca_ssvep(eeg_data, freqs, fs, n_harmonics=5):
    """CCA-based SSVEP frequency detection."""
    best_freq = None
    best_corr = -1
    T = eeg_data.shape[1] / fs
    t = np.arange(eeg_data.shape[1]) / fs

    for freq in freqs:
        # Build reference signal
        ref = []
        for h in range(1, n_harmonics + 1):
            ref.extend([np.sin(2 * np.pi * h * freq * t),
                        np.cos(2 * np.pi * h * freq * t)])
        ref = np.array(ref)

        # CCA correlation
        from sklearn.cross_decomposition import CCA
        cca = CCA(n_components=1)
        cca.fit(eeg_data.T, ref.T)
        X_c, Y_c = cca.transform(eeg_data.T, ref.T)
        corr = np.corrcoef(X_c[:, 0], Y_c[:, 0])[0, 1]
        if corr > best_corr:
            best_corr = corr
            best_freq = freq
    return best_freq, best_corr

# TRCA (Task-Related Component Analysis) - state-of-the-art for SSVEP
# Implementation available in braindecode and neurotech packages
```

## Deep Learning for EEG (深度学习)

### Braindecode Pipeline
```python
import torch
from braindecode.models import EEGNetv4, EEGConformer, EEGInceptionERP
from braindecode.datasets import WindowsDataset, create_from_windows_dataset
from braindecode.training import CroppedLoss
from braindecode.util import set_random_seeds

set_random_seeds(seed=42, cuda=True)

# Model selection
model = EEGConformer(
    n_channels=n_channels,
    n_classes=n_classes,
    input_window_samples=n_timesamples,
    final_conv_length='auto'
)

# Training
from braindecode.training import EEGClassifier
from skorch.callbacks import EpochScoring
clf = EEGClassifier(
    module=model,
    criterion=torch.nn.CrossEntropyLoss,
    optimizer=torch.optim.Adam,
    lr=0.001,
    batch_size=64,
    max_epochs=200,
    train_split=None,
    callbacks=[
        EpochScoring('accuracy', lower_is_better=False, on_train=True),
    ],
    device='cuda' if torch.cuda.is_available() else 'cpu'
)
clf.fit(X_train, y_train)
```

### Key Models Comparison
| Model | Parameters | Best For | Notes |
|-------|-----------|----------|-------|
| EEGNet | 2.6K | Low-data, embedded | Compact, good baseline |
| EEGConformer | 600K | General BCI | CNN+Transformer, SOTA on many benchmarks |
| EEG-Inception | 400K | P300, ERP | Multi-scale inception blocks |
| EEG-Inception-Times | 400K | MI, temporal | Time-domain variant |
| ShallowConvNet | 30K | Quick prototyping | Simple but effective |
| DeepConvNet | 100K | Large datasets | Needs more data |

## MOABB Evaluation (基准评测)

```python
from moabb.datasets import BNCI2014_001, PhysionetMI, Wang2016
from moabb.paradigms import LeftRightImagery, P300, SSVEP
from moabb.evaluations import WithinSessionEvaluation, CrossSessionEvaluation, CrossSubjectEvaluation
from moabb.pipelines import create_pipeline_from_options

# Select paradigm
paradigm = LeftRightImagery()

# Select datasets
datasets = [BNCI2014_001(), PhysionetMI()]

# Select pipelines
pipelines = {
    'CSP+LDA': create_pipeline_from_options(
        paradigm='imagery',
        method='csp',
        classifier='lda'
    ),
    'Riemannian MDM': create_pipeline_from_options(
        paradigm='imagery',
        method='riemann',
        classifier='mdm'
    ),
    'Tangent+SVM': create_pipeline_from_options(
        paradigm='imagery',
        method='tangentspace',
        classifier='svm'
    ),
}

# Evaluate
evaluation = WithinSessionEvaluation(
    paradigm=paradigm,
    datasets=datasets,
    n_jobs=4,
    overwrite=False
)
results = evaluation.process(pipelines)
print(results.groupby('pipeline')['score'].agg(['mean', 'std']))
```

## Real-Time BCI (实时系统)

```python
import numpy as np
from brainflow.board_shim import BoardShim, BoardIds, BrainFlowInputParams
from sklearn.pipeline import make_pipeline
import time

class RealTimeBCI:
    def __init__(self, classifier, window_sec=2.0, overlap=0.5, fs=250):
        self.clf = classifier
        self.window_samples = int(window_sec * fs)
        self.step_samples = int(window_sec * overlap * fs)
        self.fs = fs
        self.buffer = np.empty((8, 0))  # 8-channel EEG

    def run(self, board):
        """Main BCI loop."""
        board.start_stream(45000)
        print("BCI running... Ctrl+C to stop.")
        try:
            while True:
                data = board.get_current_board_data(self.window_samples)
                eeg = data[1:9]  # EEG channels

                if eeg.shape[1] >= self.window_samples:
                    # Preprocess (bandpass 8-30 Hz for MI)
                    from scipy.signal import butter, filtfilt
                    b, a = butter(4, [8/(self.fs/2), 30/(self.fs/2)], btype='band')
                    eeg_filt = filtfilt(b, a, eeg, axis=1)

                    # Classify
                    X = eeg_filt[np.newaxis, :, :]  # (1, channels, time)
                    pred = self.clf.predict(X)[0]
                    prob = self.clf.predict_proba(X)[0]

                    print(f"Prediction: {'Left' if pred==0 else 'Right'} "
                          f"(conf: {max(prob):.2%})")

                time.sleep(self.step_samples / self.fs)
        except KeyboardInterrupt:
            board.stop_stream()
            board.release_session()
```

## Visualization (可视化)

### Topographic Maps
```python
# ERP topomap at specific latency
mne.viz.plot_topomap(epochs['target'].average().data[:, 150],
                      epochs.info, times=[0.15], cmap='RdBu_r')

# Evolution over time
fig = epochs['target'].average().plot_topomap(times=np.linspace(0, 0.6, 12))
```

### Time-Frequency Analysis
```python
# Morlet wavelet decomposition
freqs = np.arange(7, 30, 3)
power = epochs.compute_psd(method='multitaper', fmin=7, fmax=30)
power.plot_topo(baseline=(-0.5, 0), mode='logratio', cmap='RdBu_r')

# Event-related synchronization/desynchronization (ERS/ERD)
power.plot([ch for ch in epochs.ch_names if ch in ['C3', 'Cz', 'C4']])
```

### Connectivity
```python
from mne_connectivity import spectral_connectivity_epochs
con = spectral_connectivity_epochs(
    epochs, method='pli', mode='multitaper',
    sfreq=epochs.info['sfreq'], fmin=4, fmax=40,
    faverage=True, n_jobs=4
)
# Plot connectivity matrix
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.imshow(con.get_data('dense')[:, :, 0], cmap='viridis')
ax.set_xticks(range(len(epochs.ch_names)))
ax.set_xticklabels(epochs.ch_names, rotation=90, fontsize=6)
```

## Neural Decoding Pipelines (神经解码)

### Quick Decision Guide
```
Small dataset (<100 trials) → Riemannian (pyriemann MDM/TangentSpace)
Medium dataset (100-1000)  → CSP + LDA/SVM for MI; xDAVER for P300
Large dataset (>1000)      → Deep learning (EEGConformer, EEGNet)
Cross-subject              → MOABB CrossSubjectEvaluation + transfer learning
Real-time                  → BrainFlow + lightweight model (EEGNet or CSP+LDA)
```

### Transfer Learning
```python
from moabb.evaluations import CrossSubjectEvaluation
from sklearn.model_selection import StratifiedKFold

# Train on multiple subjects, evaluate on held-out subject
evaluation = CrossSubjectEvaluation(
    paradigm=paradigm,
    datasets=[BNCI2014_001()],
    n_jobs=4
)
# Use MOABB's built-in transfer learning pipelines
```

## Key Datasets (via MOABB)

| Dataset | Subjects | Paradigm | Classes | Notes |
|---------|----------|----------|---------|-------|
| BNCI2014_001 | 9 | Motor Imagery | 4 | BCI Competition IV-2a, gold standard |
| PhysionetMI | 109 | Motor Imagery | 4 | Large-scale, freely available |
| Wang2016 | 35 | SSVEP | 12 freq | 40-trial SSVEP benchmark |
| Cho2017 | 52 | Motor Imagery | 2 | Two-class MI, good for beginners |
| Schirrmeister2017 | 14 | Motor Imagery | 4 | High-gamma, deep learning benchmark |
| Sosulski2019 | 13 | Auditory P300 | 2 | Passive BCI, real-world scenario |

## Pitfalls (常见陷阱)

- **Line noise**: Use 50Hz notch for Europe/China, 60Hz for US/Japan
- **Electrode impedance**: Keep below 5 kOhm for quality signals
- **Cross-subject gap**: Always use MOABB for fair comparison; Riemannian methods usually beat deep learning on small BCI datasets
- **Data leakage**: Never shuffle epochs across time; use temporal cross-validation
- **Reference**: Average reference is standard; linked mastoids for some paradigms
- **Epoch rejection**: Too aggressive = lose data; too lenient = noise. Use autoreject for adaptive thresholds
- **Filter design**: Use FIR filters (mne default) for phase preservation; avoid ICA on filtered data below 1Hz
- **Online calibration**: Always recalibrate at session start; neural signals drift across days

## Verification (验证)

```bash
python -c "import mne; print('MNE', mne.__version__)"
python -c "from brainflow.board_shim import BoardShim; print('BrainFlow OK')"
python -c "from moabb.datasets import BNCI2014_001; ds = BNCI2014_001(); print(f'{len(ds.subject_list)} subjects')"
python -c "from braindecode.models import EEGConformer; print('Braindecode OK')"
python -c "from pyriemann.classification import MDM; print('pyriemann OK')"
```
