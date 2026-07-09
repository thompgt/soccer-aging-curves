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
# Run this once (it hits the network). Uncomment when ready:

# %%
# from src.data_collection import collect_fbref_player_stats
# stats = collect_fbref_player_stats()

# %% [markdown]
# ## Step 2 — load what we saved and look around

# %%
# from src.analysis import load_raw
# df = load_raw()
# df.head()

# %% [markdown]
# From here we'll clean the data, compute per-90 metrics, and start plotting
# performance against age. We'll build `src/analysis.py:clean` together.
