# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_dynamic_libs, collect_data_files

# ── Бинарные файлы (DLL) для torch ──
torch_binaries = collect_dynamic_libs('torch')

# ── Данные для transformers и datasets ──
torch_datas = collect_data_files('torch')
transformers_datas = collect_data_files('transformers')
datasets_datas = collect_data_files('datasets')

all_binaries = torch_binaries
all_datas = torch_datas + transformers_datas + datasets_datas

# ── Только нужные скрытые импорты ──
hidden_imports = [
    # torch core
    'torch',
    'torch._C',
    'torch.nn',
    'torch.nn.functional',
    'torch.optim',
    'torch.utils',
    'torch.utils.data',
    'torch.cuda',
    'torch.backends',
    'torch.backends.cudnn',

    # transformers
    'transformers',
    'transformers.models',
    'transformers.models.bert',
    'transformers.models.bert.modeling_bert',
    'transformers.models.bert.tokenization_bert',
    'transformers.models.bert.tokenization_bert_fast',
    'transformers.training_args',
    'transformers.trainer',
    'transformers.data',
    'transformers.data.data_collator',

    # datasets
    'datasets',
    'datasets.arrow_dataset',
    'datasets.formatting',
    'datasets.formatting.torch_formatter',

    # sklearn
    'sklearn',
    'sklearn.model_selection',
    'sklearn.metrics',
    'sklearn.utils',
    'sklearn.utils._typedefs',
    'sklearn.utils._heap',
    'sklearn.utils._sorting',
    'sklearn.utils._vector_sentinel',
    'sklearn.neighbors._partition_nodes',
    'sklearn.tree._utils',

    # прочие зависимости
    'tokenizers',
    'huggingface_hub',
    'safetensors',
    'filelock',
    'regex',
    'requests',
    'tqdm',
    'packaging',
    'numpy',
    'pandas',
    'pyarrow',

    # PyQt6
    'PyQt6',
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    'PyQt6.sip',

    # ваши модули
    'rubert_trainer',
    'rubert_trainer.__main__',
    'rubert_trainer.gui',
    'rubert_trainer.gui.main_window',
    'rubert_trainer.gui.metric_card',
    'rubert_trainer.controllers',
    'rubert_trainer.controllers.training_controller',
    'rubert_trainer.services',
    'rubert_trainer.services.training_service',
    'rubert_trainer.models',
    'rubert_trainer.models.training_config',
    'rubert_trainer.utils',
    'rubert_trainer.utils.logging_utils',
]

# ══════════════════════════════════════════
#  ИСКЛЮЧАЕМ всё лишнее — особенно tensorflow!
# ══════════════════════════════════════════
excludes = [
    'tensorflow',
    'tensorflow_core',
    'tensorboard',
    'tf2onnx',
    'keras',
    'jax',
    'jaxlib',
    'flax',
    'optax',
    'matplotlib',
    'IPython',
    'notebook',
    'jupyter',
    'pytest',
    'sphinx',
    'setuptools',
    'pip',
    'conda',
    'tkinter',
]

a = Analysis(
    ['run_trainer.py'],
    pathex=[],
    binaries=all_binaries,
    datas=all_datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='run_trainer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='run_trainer',
)