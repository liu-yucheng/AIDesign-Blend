<!---
Copyright 2022 Yucheng Liu. GNU GPL3 license.
GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt
First added by username: liu-yucheng
Last updated by username: liu-yucheng
--->

# AIDesign-Blend Project Folder

A folder that holds the subfolders and files that an AIDesign-Blend project needs.

# Documentation Files

Texts.

## `README.md`

This file itself.

# Configuration Files

Texts.

## `blenders_config.json`

Blenders configuration.

Configuration items. Type `dict[str, typing.Union[dict, list, str, bool, int, float, None]]`.

Configuration item descriptions are listed below.

- `manual_seed`. Manual random seed. Type `typing.Union[None, int]`. Range [0, ).
- `random_frags`. Random fragments. Type `bool`.
- `avoid_random_duplicates`. Type `bool`.
- `random_flipping`. Type `bool`.
- `frag_resolution`. Fragment resolution in pixels. Type `int`. Range [2, ). Will be converted to the nearest bigger even number.
- `x_frag_count`. X-axis fragment count. Type `int`. Range [2, ).
- `y_frag_count`. Y-axis fragment count. Type `int`. Range [2, ).
- `frags_grid`. Fragments grid configuration. Type `dict`.
  - `save`. Whether to save the fragments grid. Type `bool`.
  - `padding`. Type `int`. Range [0, ).
  - `padding_brightness`. Type `int`. Range [0, 255].
- `custom_gradient`. Custom gradient configuration. Type `dict`.
  - `enabled`. Whether to enable custom gradient. Type `bool`.
  - `coefficients`. Gradient polynomial coefficients. Type `list[float]`.
  - `exponents`. Gradient polynomial coefficients. Type `list[float]`.

# Result Files

Texts and images.

## `Blended-From-<source>-Time-<time>.jpg`

**Note:** Not present until an AIDesign-Blend blending session completes.

Blended images.

## `Frags-From-<source>-Time-<time>.jpg`

**Note:** Not present until an AIDesign-Blend blending session with the configuration item `frags_grid.save = true` completes.

Grids of fragments.

## `log.txt`

**Note:** Not present until an AIDesign-Blend blending session completes.

Log.
