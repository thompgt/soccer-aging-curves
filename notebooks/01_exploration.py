# %% [markdown]
# # 01 — First look at the data
#
# This is a "notebook as script" (works with Jupyter's `# %%` cells in VS Code,
# or convert to .ipynb later). Run cells top to bottom.

# %%
import sys
from pathlib import Path

# Make `src` importable when running from the notebooks/ folder.
sys.path.append(str(Path.cwd().parent))

import pandas as pd
from src import config

pd.set_option("display.max_columns", 50)

# %% [markdown]
# ## Step 1 — collect data
# Run this once (downloads from Kaggle; needs a Kaggle token). Uncomment when ready:

# %%
# from src.data_collection import main as collect
# collect()

# %% [markdown]
# ## Step 2 — load the staged tables and look around

# %%
# from src.analysis import load_raw
# tables = load_raw()
# tables["players"].head()

# %% [markdown]
# From here we'll aggregate appearances into player-seasons, compute age and
# per-90 metrics, attach market value, and start plotting performance vs. age.
# We'll build `src/analysis.py:build_player_seasons` together.
