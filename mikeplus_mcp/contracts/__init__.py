"""Engine-agnostic contracts — the 'narrow waist'.

schema / units / plot_style are deliberately kept pure (no mikeplus/mikeio
imports at module top) so they can be reused by any engine adapter (MIKE+, SWMM,
LSTM) and imported anywhere.
"""
