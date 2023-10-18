"""Contexts."""

# Copyright 2022-2023 Yucheng Liu. GNU GPL3 license.
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

    # Items directly related to blenders config

    rand_mode: str = None
    """Random mode."""
    rand_seed: int = None
    """Random seed."""
    rand_frags: bool = None
    """Random fragments."""
    avoid_rand_dups: bool = None
    """Avoid random fragment duplicates."""
    rand_flip: bool = None
    """Random flipping."""
    rand_rot: bool = None
    """Random rotating."""
    frag_width: int = None
    """Fragment width."""
    frag_height: int = None
    """Fragment height."""
    x_frag_count: int = None
    """X fragment count."""
    y_frag_count: int = None
    """Y fragment count."""
    save_frag_locs: bool = None
    """Save fragment locations."""

    save_frags_grid: bool = None
    """Save fragments grid."""
    frags_grid_pad: int = None
    """Fragments grid padding."""
    frags_grid_pad_red = None
    """Fragments grid padding red."""
    frags_grid_pad_green = None
    """Fragments grid padding green."""
    frags_grid_pad_blue = None
    """Fragments grid padding blue."""

    custom_grad_enabled: bool = None
    """Custom gradient function enabled."""

    # End

    # The grad func item
    grad_func = None
    """Gradient function. Used to calculate the gradient progress. Input and output range [0, 1]."""

    # Frags folder related items

    frags_path = None
    """Fragments path."""
    frags_name = None
    """Fragments name."""
    frag_count = None
    """Fragment count."""
    frag_locs = None
    """Fragment locations."""

    # End
    # Helper matrix items

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

    # End
    # Canvas related items

    canvas_width = None
    """Canvas width."""
    canvas_height = None
    """Canvas height."""
    canvas = None
    """Canvas. Numpy array. Subscript [x, y]."""

    # End
    # Frags grid related items

    frags_grid_width = None
    """Fragments grid width."""
    frags_grid_height = None
    """Fragments grid height."""
    frags_grid = None
    """Fragments grid. Numpy array. Subscript [x, y]."""

    # End

    # The frag locs item
    frag_locs_text = None
    """Fragment locations text."""
