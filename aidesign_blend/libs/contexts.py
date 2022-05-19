"""Contexts."""

# Copyright 2022 Yucheng Liu. GNU GPL3 license.
# GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt
# First added by username: liu-yucheng
# Last updated by username: liu-yucheng

from aidesign_blend.libs import utils

# Aliases

_DotDict = utils.DotDict

# End


class Context(_DotDict):
    pass


class BlenderContext(Context):
    """Blender context."""

    rand_mode = None
    """Random mode."""
    rand_seed = None
    """Random seed."""
    rand_frags = None
    """Random fragments."""
    avoid_rand_dups = None
    """Avoid random fragment duplicates."""
    rand_flip = None
    """Random flipping."""
    rand_rot = None
    """Random rotating."""
    save_frags_grid = None
    """Save fragments grid."""
    save_frag_locs = None
    """Save fragment locations."""

    frag_width = None
    """Fragment width."""
    frag_height = None
    """Fragment height."""
    x_frag_count = None
    """X fragment count."""
    y_frag_count = None
    """Y fragment count."""

    frags_path = None
    """Fragments path."""
    frags_name = None
    """Fragments name."""
    frag_count = None
    """Fragment count."""
    frag_locs = None
    """Fragment locations."""

    index_matrix = None
    """Index matrix. Subscripts [y][x]."""
    flip_matrix = None
    """Flipping matrix. Subscripts [y][x]."""
    rot_matrix = None
    """Rotation matrix. Subscripts [y][x]."""
    bm_width = None
    """Blend matrix width."""
    bm_height = None
    """Blend matrix height."""
    ulbm = None
    """Upper left blend matrix. Numpy array. Subscript [x, y]."""
    urbm = None
    """Upper right blend matrix. Numpy array. Subscript [x, y]."""
    llbm = None
    """Lower left blend matrix.Numpy array. Subscript [x, y]."""
    lrbm = None
    """Lower right blend matrix. Numpy array. Subscript [x, y]."""

    canvas_width = None
    """Canvas width."""
    canvas_height = None
    """Canvas height."""
    canvas = None
    """Canvas. Numpy array. Subscript [x, y]."""

    frags_grid_pad = None
    """Fragments grid padding."""
    frags_grid_pad_bright = None
    """Fragments grid padding brightness."""
    frags_grid_width = None
    """Fragments grid width."""
    frags_grid_height = None
    """Fragments grid height."""
    frags_grid = None
    """Fragments grid. Numpy array. Subscript [x, y]."""

    custom_grad_enabled = None
    """Custom gradient function enabled."""
    grad_func = None
    """Gradient function. Used to calculate the gradient progress. Input and output range [0, 1]."""

    frag_locs_text = None
    """Fragment locations text."""
