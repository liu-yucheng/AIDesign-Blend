"""Blenders."""

# Copyright 2022 Yucheng Liu. GNU GPL3 license.
# GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt
# First added by username: liu-yucheng
# Last updated by username: liu-yucheng

import datetime
import imghdr
import numpy
import os
import pathlib
import random
import typing

from os import path as ospath
from PIL import Image as pil_image

from aidesign_blend.libs import contexts
from aidesign_blend.libs import defaults
from aidesign_blend.libs import grads
from aidesign_blend.libs import utils

# Aliases

_BlenderContext = contexts.BlenderContext
_Callable = typing.Callable
_clamp = utils.clamp_float
_isfile = ospath.isfile
_join = ospath.join
_listdir = os.listdir
_load_json = utils.load_json
_logstr = utils.logstr
_LU = grads.LU
_now = datetime.datetime.now
_nparray = numpy.array
_npclip = numpy.clip
_npmultiply = numpy.multiply
_npseed = numpy.random.seed
_npsingle = numpy.single
_nptranspose = numpy.transpose
_npubyte = numpy.ubyte
_np_ndarray = numpy.ndarray
_Path = pathlib.Path
_pil_image_fromarray = pil_image.fromarray
_pil_image_open = pil_image.open
_Poly1V = grads.Poly1V
_randint = random.randint
_rand_bool = utils.rand_bool
_save_text = utils.save_text
_seed = random.seed
_shuffle = random.shuffle
_what = imghdr.what

# End


class Blender:
    """Blender."""

    def __init__(self, frags_path, proj_path, logs, debug_level=0):
        """Inits self with the given args."""
        self._frags_path = frags_path
        """Fragments path"""
        self._proj_path = proj_path
        """Project path"""
        self._logs = logs
        """Logs."""
        self._debug_level = debug_level
        """Debug level."""
        self._config = {}
        """Configuration."""
        self._context = _BlenderContext()
        """Context."""

    def logstr(self, string="", debug_level=0):
        """Logs a string.

        Args:
            string: the string
            debug_level: the debug level
        """
        if debug_level <= self._debug_level:
            _logstr(self._logs, string)

    def logln(self, line="", debug_level=0):
        """Logs a line.

        Args:
            line: the line
            debug_level: the debug level
        """
        line += "\n"
        self.logstr(line, debug_level)

    def _read_config(self):
        config_loc = _join(self._proj_path, defaults.blenders_config_name)
        self.logln(f"Blenders config location: {config_loc}", 1)
        self._config = _load_json(config_loc)
        self.logln("Completed reading blenders config", 1)

    def _pad_coefs_exps(self, coefs, exps):
        """Returns coefs, exps."""
        coefs = list(coefs)
        exps = list(exps)

        coefs_len = len(coefs)
        exps_len = len(exps)

        if coefs_len == 0:
            coefs.append(float(0))

        if exps_len == 0:
            exps.append(float(0))

        coefs_len = len(coefs)
        exps_len = len(exps)

        if coefs_len < exps_len:
            pad_len = exps_len - coefs_len
            pad = [float(0) for _ in range(pad_len)]
            coefs += pad
        elif coefs_len > exps_len:
            pad_len = coefs_len - exps_len
            pad = [float(0) for _ in range(pad_len)]
            exps += pad
        else:  # elif coefs_len == exps_len:
            pass
        # end if

        coefs = [float(elem) for elem in coefs]
        exps = [float(elem) for elem in exps]
        return coefs, exps

    def _parse_config(self):
        c = self._context

        # Parse manual_seed

        manual_seed = self._config["manual_seed"]
        self.logln(f"manual_seed: {manual_seed}", 101)

        if manual_seed is not None:
            manual_seed = int(manual_seed)
            manual_seed = manual_seed % (2 ** 32 - 1)

        if manual_seed is None:
            rand_mode = "Auto"
            _seed(None)
            rand_seed = _randint(0, 2 ** 32 - 1)
        else:  # elif manual_seed is not None:
            rand_mode = "Manual"
            rand_seed = manual_seed
        # end if

        _seed(rand_seed)
        _npseed(rand_seed)
        c.rand_mode = rand_mode
        c.rand_seed = rand_seed
        self.logln(f"Random:  Mode: {rand_mode}  Seed: {rand_seed}", 1)

        # End parse manual seed
        # Parse random_frags

        rand_frags = self._config["random_frags"]
        self.logln(f"random_frags: {rand_frags}", 101)
        rand_frags = bool(rand_frags)
        c.rand_frags = rand_frags
        self.logln(f"Random fragments: {rand_frags}", 1)

        # End parse random_frags
        # Parse avoid_random_duplicates

        avoid_rand_dups_key = "avoid_random_duplicates"
        avoid_rand_dups = False

        if avoid_rand_dups_key in self._config:
            avoid_rand_dups = self._config[avoid_rand_dups_key]
            self.logln(f"avoid_rand_dups: {avoid_rand_dups}", 101)

        avoid_rand_dups = bool(avoid_rand_dups)
        c.avoid_rand_dups = avoid_rand_dups
        self.logln(f"Avoid random fragment duplicates: {avoid_rand_dups}", 1)

        # End parse avoid_random_duplicates
        # Parse random_flipping

        rand_flip = self._config["random_flipping"]
        self.logln(f"rand_flip: {rand_flip}", 101)
        rand_flip = bool(rand_flip)
        c.rand_flip = rand_flip
        self.logln(f"Random flipping: {rand_flip}", 1)

        # End parse random_flipping
        # Parse random_rotating

        rand_rot_key = "random_rotating"

        if rand_rot_key in self._config:
            rand_rot = self._config[rand_rot_key]
            self.logln(f"rand_rot: {rand_rot}", 101)
            rand_rot = bool(rand_rot)
            c.rand_rot = rand_rot
        else:
            rand_rot = False
        # end if

        self.logln(f"Random rotating: {rand_rot}", 1)

        # End parse random_rotating
        # Parse frag_resolution

        frag_res = self._config["frag_resolution"]
        self.logln(f"frag_res: {frag_res}", 101)
        frag_res = int(frag_res)

        if frag_res < 0:
            frag_res *= -1

        if frag_res < 2:
            frag_res = 2

        if not frag_res % 2 == 0:
            frag_res += 1

        c.frag_width = frag_res
        c.frag_height = frag_res
        self.logln(f"Fragment:  Width: {frag_res}  Height: {frag_res}", 1)

        # End parse frag_resolution
        # Parse x_frag_count

        x_frag_count = self._config["x_frag_count"]
        self.logln(f"x_frag_count: {x_frag_count}", 101)
        x_frag_count = int(x_frag_count)

        if x_frag_count < 0:
            x_frag_count *= -1

        if x_frag_count < 2:
            x_frag_count = 2

        c.x_frag_count = x_frag_count

        # End parse x_frag_count
        # Parse y_frag_count

        y_frag_count = self._config["y_frag_count"]
        self.logln(f"y_frag_count: {y_frag_count}", 101)
        y_frag_count = int(y_frag_count)

        if y_frag_count < 0:
            y_frag_count *= -1

        if y_frag_count < 2:
            y_frag_count = 2

        c.y_frag_count = y_frag_count
        total_frag_count = x_frag_count * y_frag_count
        self.logln(f"Fragment count:  X: {x_frag_count}  Y: {y_frag_count}  Total: {total_frag_count}", 1)

        # End parse y_frag_count
        # Parse save_frag_locations

        save_frag_locs_key = "save_frag_locations"

        if save_frag_locs_key in self._config:
            save_frag_locs = bool(self._config[save_frag_locs_key])
        else:
            save_frag_locs = False
        # end if

        self.logln(f"save_frag_locs: {save_frag_locs}", 101)
        c.save_frag_locs = save_frag_locs
        self.logln(f"Save fragment locations: {save_frag_locs}", 1)

        # End parse save_frag_locations
        # Parse frags_grid

        frags_grid_key = "frags_grid"
        save_key = "save"
        save_frags_grid = False

        if frags_grid_key in self._config:
            fgrid_config = self._config[frags_grid_key]

        if save_key in fgrid_config:
            save_frags_grid = bool(fgrid_config[save_key])

        self.logln(f"save_frags_grid: {save_frags_grid}", 101)

        if save_frags_grid:
            frags_grid_pad = fgrid_config["padding"]
            frags_grid_pad = int(frags_grid_pad)

            if frags_grid_pad < 0:
                frags_grid_pad *= -1

            frags_grid_pad_bright = fgrid_config["padding_brightness"]
            frags_grid_pad_bright = int(frags_grid_pad_bright)

            if frags_grid_pad_bright < 0:
                frags_grid_pad_bright *= -1

            if frags_grid_pad_bright > 255:
                frags_grid_pad_bright = 255

        else:  # elif not save_fgrid:
            frags_grid_pad = None
            frags_grid_pad_bright = None
        # end if

        if save_frags_grid:
            info = str(
                f"frags_grid_pad: {frags_grid_pad}\n"
                f"frags_grid_pad_bright: {frags_grid_pad_bright}\n"
            )

            self.logstr(info, 101)
        # end if

        c.save_frags_grid = save_frags_grid
        c.frags_grid_pad = frags_grid_pad
        c.frags_grid_pad_bright = frags_grid_pad_bright
        self.logln(f"Save fragments grid: {save_frags_grid}", 1)

        if save_frags_grid:
            self.logln(f"Fragments grid:  Padding: {frags_grid_pad}  Padding brightness: {frags_grid_pad_bright}", 1)

        # End parse frags_grid
        # Parse custom_gradient

        custom_grad_key = "custom_gradient"

        if custom_grad_key in self._config:
            custom_grad_enabled = bool(self._config[custom_grad_key]["enabled"])
        else:
            custom_grad_enabled = False
        # end if

        if custom_grad_enabled:
            custom_grad_config = self._config[custom_grad_key]
            coefs = custom_grad_config["coefficients"]
            exps = custom_grad_config["exponents"]
            coefs, exps = self._pad_coefs_exps(coefs, exps)
            grad_func = _Poly1V(coefs, exps)
        else:  # elif not cust_grad_enabled:
            grad_func = _LU()
        # end if

        c.custom_grad_enabled = custom_grad_enabled
        c.grad_func = grad_func

        if custom_grad_enabled:
            grad_name = "custom"
        else:  # elif not cust_grad_enabled:
            grad_name = "default"
        # end if

        self.logln(f"Prepared gradient function: {grad_name}", 1)
        self.logln(f"Gradient function: \" {grad_func.fnstr()} \"", 1)

        # End parse custom_gradient

        self.logln("Completed parsing blenders config", 1)

    def _read_frags_path(self, frags_path):
        frag_names = _listdir(frags_path)
        frag_names.sort()
        self.logln(f"frag_names: {frag_names}", 102)
        frag_locs = []

        for name in frag_names:
            loc = _join(frags_path, name)
            frag_locs.append(loc)

        orig_frag_locs = frag_locs
        frag_locs = []

        for loc in orig_frag_locs:
            is_file = _isfile(loc)
            is_img = is_file and _what(loc) is not None

            if is_img:
                frag_locs.append(loc)
        # end for

        self.logln(f"frag_locs: {frag_locs}", 102)
        frag_count = len(frag_locs)
        self.logln(f"frag_count: {frag_count}", 101)
        return frag_locs

    def _prep_frags(self):
        c = self._context

        frags_path = self._frags_path
        frag_locs = self._read_frags_path(frags_path)
        frag_count = len(frag_locs)

        if frag_count <= 0:
            frags_path = defaults.default_frags_path
            self.logln(f"Found no fragments in frags_path, defaulting frags_path to: {frags_path}", 1)
            frag_locs = self._read_frags_path(frags_path)
            frag_count = len(frag_locs)
        # end if

        frags_name = _Path(frags_path).name
        c.frags_path = frags_path
        self.logln(f"Fragments path: {frags_path}", 1)
        c.frags_name = frags_name
        self.logln(f"Fragments name: {frags_name}", 1)
        c.frag_count = frag_count
        self.logln(f"Fragment count: {frag_count}", 1)
        c.frag_locs = frag_locs
        self.logln("Prepared fragment locations")

    def _make_2d_matrix(self, y_size, x_size):
        matrix = [
            [
                None
                for _ in range(x_size)
            ]
            for _ in range(y_size)
        ]

        return matrix

    def _make_numpy_2d_matrix(self, x_size, y_size):
        matrix = _np_ndarray((x_size, y_size), dtype=_npsingle)
        return matrix

    def _grad_prog(self, index, count):
        index = int(index)
        count = int(count)
        c = self._context

        last_index = count - 1
        float_index = float(index)
        float_last_index = float(last_index)
        line_prog = float_index / float_last_index

        grad_func: _Callable[..., float] = c.grad_func
        prog = grad_func(line_prog)
        return prog

    def _gen_rand_frag_indices(self):
        c = self._context

        idxs = [idx for idx in range(c.frag_count)]
        _shuffle(idxs)

        result = idxs
        return result

    def _prep_matrices(self):
        c = self._context

        # Make index matrix

        index_matrix = self._make_2d_matrix(c.y_frag_count, c.x_frag_count)

        if c.avoid_rand_dups:
            remain_indices = self._gen_rand_frag_indices()
        else:  # elif not c.avoid_rand_dups:
            remain_indices = None
        # end if

        if c.rand_frags:
            for iy in range(c.y_frag_count):
                for ix in range(c.x_frag_count):
                    if c.avoid_rand_dups:
                        remain_indices_len = len(remain_indices)

                        if remain_indices_len <= 0:
                            remain_indices = self._gen_rand_frag_indices()

                        index_matrix[iy][ix] = remain_indices.pop(0)
                    else:  # elif not c.avoid_rand_dups:
                        index_matrix[iy][ix] = _randint(0, c.frag_count - 1)
                    # end if
                # end for
            # end for
        else:  # elif not c.rand_frags:
            index = 0

            for iy in range(c.y_frag_count):
                for ix in range(c.x_frag_count):
                    index_matrix[iy][ix] = index
                    index = (index + 1) % c.frag_count
                # end for
            # end for
        # end if

        self.logln(f"index_matrix: {index_matrix}", 103)

        # End make index matrix
        # Make flip matrix

        flip_matrix = self._make_2d_matrix(c.y_frag_count, c.x_frag_count)

        if c.rand_flip:
            for iy in range(c.y_frag_count):
                for ix in range(c.x_frag_count):
                    flip_x = _rand_bool()
                    flip_y = _rand_bool()
                    flip = ""

                    if flip_x:
                        flip += "x"

                    if flip_y:
                        flip += "y"

                    flip_matrix[iy][ix] = flip
                # end for
            # end for
        else:  # elif not c.rand_flip:
            for iy in range(c.y_frag_count):
                for ix in range(c.x_frag_count):
                    flip_matrix[iy][ix] = ""
                # end for
            # end for
        # end if

        self.logln(f"flip_matrix: {flip_matrix}", 103)

        # End make flip matrix
        # Make rotation matrix

        rot_matrix = self._make_2d_matrix(c.y_frag_count, c.x_frag_count)

        if c.rand_rot:
            for iy in range(c.y_frag_count):
                for ix in range(c.x_frag_count):
                    rot_180 = utils.rand_bool()

                    if rot_180:
                        rot = "180"
                    else:
                        rot = ""
                    # end if

                    rot_matrix[iy][ix] = rot
                # end for
            # end for
        else:
            for iy in range(c.y_frag_count):
                for ix in range(c.x_frag_count):
                    rot_matrix[iy][ix] = ""
                # end for
            # end for
        # end if

        self.logln(f"rot_matrix: {rot_matrix}", 103)

        # End make rotation matrix
        # Make blend matrices

        width = c.frag_width // 2
        height = c.frag_height // 2
        ulbm = self._make_numpy_2d_matrix(width, height)
        urbm = self._make_numpy_2d_matrix(width, height)
        llbm = self._make_numpy_2d_matrix(width, height)
        lrbm = self._make_numpy_2d_matrix(width, height)

        for iy in range(height):
            for ix in range(width):
                x_prog = self._grad_prog(ix, width)
                y_prog = self._grad_prog(iy, height)

                # The pre-0.7.0 blend factor formulas
                # ul_fac = (1 - y_prog) * (1 - x_prog)
                # ur_fac = (1 - y_prog) * x_prog
                # ll_fac = y_prog * (1 - x_prog)
                # lr_fac = y_prog * x_prog

                # Use normalized 2-d distances to find blend factors

                last_ix = width - 1
                last_iy = height - 1
                x_remain = self._grad_prog(last_ix - ix, width)
                y_remain = self._grad_prog(last_iy - iy, height)

                ul_prog = (x_prog ** 2 + y_prog ** 2) ** 0.5
                ur_prog = (x_remain ** 2 + y_prog ** 2) ** 0.5
                ll_prog = (x_prog ** 2 + y_remain ** 2) ** 0.5
                lr_prog = (x_remain ** 2 + y_remain ** 2) ** 0.5

                max_prog = 1
                ul_remain = max_prog - ul_prog
                ur_remain = max_prog - ur_prog
                ll_remain = max_prog - ll_prog
                lr_remain = max_prog - lr_prog

                ul_remain = _clamp(ul_remain, 0, 1)
                ur_remain = _clamp(ur_remain, 0, 1)
                ll_remain = _clamp(ll_remain, 0, 1)
                lr_remain = _clamp(lr_remain, 0, 1)

                remain_sum = ul_remain + ur_remain + ll_remain + lr_remain

                ul_fac = ul_remain / remain_sum
                ur_fac = ur_remain / remain_sum
                ll_fac = ll_remain / remain_sum
                lr_fac = lr_remain / remain_sum

                # End use normalized 2-d distances to find blend factors

                ulbm[ix, iy] = ul_fac
                urbm[ix, iy] = ur_fac
                llbm[ix, iy] = ll_fac
                lrbm[ix, iy] = lr_fac
            # end for
        # end for

        info = str(
            f"Blend matrices:\n"
            f"  ulbm:\n"
            f"{ulbm}\n"
            f"  urbm:\n"
            f"{urbm}\n"
            f"  llbm:\n"
            f"{llbm}\n"
            f"  lrbm:\n"
            f"{lrbm}\n"
        )

        self.logstr(info, 103)

        # End make blend matrices

        c.index_matrix = index_matrix
        self.logln("Prepared the index matrix", 1)
        c.flip_matrix = flip_matrix
        self.logln("Prepared the flipping matrix", 1)
        c.rot_matrix = rot_matrix
        self.logln("Prepared the rotation matrix", 1)
        c.bm_width = width
        c.bm_height = height
        c.ulbm = ulbm
        c.urbm = urbm
        c.llbm = llbm
        c.lrbm = lrbm
        self.logln("Prepared 4 blend matrices:  Upper-left  Upper-right  Lower-left  Lower-right", 1)
        self.logln(f"Blend matrices:  Width: {width}  Height: {height}", 1)

    def _make_numpy_3d_matrix(self, x_size, y_size, z_size):
        matrix = _np_ndarray((x_size, y_size, z_size), dtype=_npsingle)
        return matrix

    def _prep_canvas(self):
        c = self._context

        width = c.bm_width * (c.x_frag_count - 1)
        height = c.bm_height * (c.y_frag_count - 1)
        canvas = self._make_numpy_3d_matrix(width, height, 3)

        c.canvas_width = width
        c.canvas_height = height
        c.canvas = canvas

        self.logln(f"Prepared the canvas:  Width: {width}  Height: {height}", 1)

    def _prep_frags_grid(self):
        c = self._context

        if c.save_frags_grid:
            width = c.frags_grid_pad + c.x_frag_count * (c.frag_width + c.frags_grid_pad)
            height = c.frags_grid_pad + c.y_frag_count * (c.frag_height + c.frags_grid_pad)
            frags_grid = self._make_numpy_3d_matrix(width, height, 3)

            info = str(
                f"width: {width}\n"
                f"height: {height}\n"
            )

            self.logstr(info, 101)

            info = str(
                f"frags_grid:\n"
                f"{frags_grid}\n"
            )

            self.logstr(info, 104)
            c.frags_grid_width = width
            c.frags_grid_height = height
            c.frags_grid = frags_grid
            self.logln(f"Prepared the fragments grid:  Width: {width}  Height: {height}", 1)
        # end if

    def _tweak_pil_safety(self):
        max_width = 65535
        max_height = 65535
        max_pixels = max_width * max_height
        pil_image.MAX_IMAGE_PIXELS = max_pixels
        self.logln(f"Tweaked PIL safety max pixels:  Width: {max_width}  Height: {max_height}  Total: {max_pixels}", 1)

    def _blend_block(self, block_y, block_x):
        c = self._context

        canvas_x1 = block_x * c.bm_width
        canvas_y1 = block_y * c.bm_height
        canvas_x2 = canvas_x1 + c.bm_width
        canvas_y2 = canvas_y1 + c.bm_height

        ul_box = c.bm_width, c.bm_height, c.frag_width, c.frag_height
        ur_box = 0, c.bm_height, c.bm_width, c.frag_height
        ll_box = c.bm_width, 0, c.frag_width, c.bm_height
        lr_box = 0, 0, c.bm_width, c.bm_height

        uly, ulx = block_y, block_x
        ury, urx = uly, ulx + 1
        lly, llx = uly + 1, ulx
        lry, lrx = uly + 1, ulx + 1

        ul_index = c.index_matrix[uly][ulx]
        ur_index = c.index_matrix[ury][urx]
        ll_index = c.index_matrix[lly][llx]
        lr_index = c.index_matrix[lry][lrx]

        ul_flip = c.flip_matrix[uly][ulx]
        ur_flip = c.flip_matrix[ury][urx]
        ll_flip = c.flip_matrix[lly][llx]
        lr_flip = c.flip_matrix[lry][lrx]

        ul_rot = c.rot_matrix[uly][ulx]
        ur_rot = c.rot_matrix[ury][urx]
        ll_rot = c.rot_matrix[lly][llx]
        lr_rot = c.rot_matrix[lry][lrx]

        ul_loc = c.frag_locs[ul_index]
        ur_loc = c.frag_locs[ur_index]
        ll_loc = c.frag_locs[ll_index]
        lr_loc = c.frag_locs[lr_index]

        ul_image = _pil_image_open(ul_loc)
        ur_image = _pil_image_open(ur_loc)
        ll_image = _pil_image_open(ll_loc)
        lr_image = _pil_image_open(lr_loc)

        size = c.frag_width, c.frag_height
        resample = pil_image.BICUBIC
        ul_image = ul_image.resize(size=size, resample=resample)
        ur_image = ur_image.resize(size=size, resample=resample)
        ll_image = ll_image.resize(size=size, resample=resample)
        lr_image = lr_image.resize(size=size, resample=resample)

        x_flip = pil_image.FLIP_TOP_BOTTOM
        y_flip = pil_image.FLIP_LEFT_RIGHT

        if "x" in ul_flip:
            ul_image = ul_image.transpose(x_flip)

        if "y" in ul_flip:
            ul_image = ul_image.transpose(y_flip)

        if "x" in ur_flip:
            ur_image = ur_image.transpose(x_flip)

        if "y" in ur_flip:
            ur_image = ur_image.transpose(y_flip)

        if "x" in ll_flip:
            ll_image = ll_image.transpose(x_flip)

        if "y" in ll_flip:
            ll_image = ll_image.transpose(y_flip)

        if "x" in lr_flip:
            lr_image = lr_image.transpose(x_flip)

        if "y" in lr_flip:
            lr_image = lr_image.transpose(y_flip)

        rot_180 = pil_image.ROTATE_180

        if ul_rot == "180":
            ul_image = ul_image.transpose(rot_180)

        if ur_rot == "180":
            ur_image = ur_image.transpose(rot_180)

        if ll_rot == "180":
            ll_image = ll_image.transpose(rot_180)

        if lr_rot == "180":
            lr_image = lr_image.transpose(rot_180)

        ul_image = ul_image.crop(ul_box)
        ur_image = ur_image.crop(ur_box)
        ll_image = ll_image.crop(ll_box)
        lr_image = lr_image.crop(lr_box)

        ulnp = _nparray(ul_image, dtype=_npsingle)
        urnp = _nparray(ur_image, dtype=_npsingle)
        llnp = _nparray(ll_image, dtype=_npsingle)
        lrnp = _nparray(lr_image, dtype=_npsingle)

        axis_order = [1, 0, 2]
        ulnp = _nptranspose(ulnp, axis_order)
        urnp = _nptranspose(urnp, axis_order)
        llnp = _nptranspose(llnp, axis_order)
        lrnp = _nptranspose(lrnp, axis_order)
        self.logln(f"Transposed the UL, UR, LL, LR images with axis order: {axis_order}", 103)

        info = str(
            f"Image NumPy arrays:\n"
            f"  ulnp:\n"
            f"{ulnp}\n"
            f"  urnp:\n"
            f"{urnp}\n"
            f"  llnp:\n"
            f"{llnp}\n"
            f"  lrnp:\n"
            f"{lrnp}\n"
        )

        self.logstr(info, 105)

        info = str(
            f"Image NumPy array shapes\n"
            f"  ulnp shape: {ulnp.shape}\n"
            f"  urnp shape: {urnp.shape}\n"
            f"  llnp shape: {llnp.shape}\n"
            f"  lrnp shape: {lrnp.shape}\n"
        )

        self.logstr(info, 103)

        block_r = _npmultiply(c.ulbm, ulnp[:, :, 0]) + \
            _npmultiply(c.urbm, urnp[:, :, 0]) + \
            _npmultiply(c.llbm, llnp[:, :, 0]) + \
            _npmultiply(c.lrbm, lrnp[:, :, 0])

        block_g = _npmultiply(c.ulbm, ulnp[:, :, 1]) + \
            _npmultiply(c.urbm, urnp[:, :, 1]) + \
            _npmultiply(c.llbm, llnp[:, :, 1]) + \
            _npmultiply(c.lrbm, lrnp[:, :, 1])

        block_b = _npmultiply(c.ulbm, ulnp[:, :, 2]) + \
            _npmultiply(c.urbm, urnp[:, :, 2]) + \
            _npmultiply(c.llbm, llnp[:, :, 2]) + \
            _npmultiply(c.lrbm, lrnp[:, :, 2])

        _npclip(block_r, 0, 255, block_r)
        _npclip(block_g, 0, 255, block_g)
        _npclip(block_b, 0, 255, block_b)

        info = str(
            f"Image block RGB channels:\n"
            f"  block_r: \n"
            f"{block_r}\n"
            f"  block_g: \n"
            f"{block_g}\n"
            f"  block_b: \n"
            f"{block_b}\n"
        )

        self.logstr(info, 104)
        c.canvas[canvas_x1: canvas_x2, canvas_y1: canvas_y2, 0] = block_r
        c.canvas[canvas_x1: canvas_x2, canvas_y1: canvas_y2, 1] = block_g
        c.canvas[canvas_x1: canvas_x2, canvas_y1: canvas_y2, 2] = block_b

    def _blend_blocks(self):
        c = self._context

        info = str(
            "Started blending blocks\n"
            "-"
        )

        self.logln(info, 1)
        block_total = (c.y_frag_count - 1) * (c.x_frag_count - 1)
        cur_block = 0

        for iy in range(c.y_frag_count - 1):
            for ix in range(c.x_frag_count - 1):
                self._blend_block(iy, ix)

                needs_log = \
                    cur_block + 1 == 1 or \
                    (cur_block + 1) % 180 == 0 or \
                    cur_block + 1 == block_total

                if needs_log:
                    self.logln(f"Blended block {cur_block + 1} / {block_total}", 1)

                cur_block += 1
            # end for
        # end for

        self.logln(f"Canvas: {c.canvas}", 104)

        info = str(
            "-\n"
            "Completed blending blocks"
        )

        self.logln(info, 1)

    def _save_blended_blocks(self):
        c = self._context

        axis_order = [1, 0, 2]
        c.canvas = _nptranspose(c.canvas, axis_order)
        self.logln(f"Transposed the canvas with axis order {axis_order}", 101)
        canvas: _np_ndarray = c.canvas
        canvas = canvas.astype(_npubyte)
        image = _pil_image_fromarray(canvas, "RGB")
        now = _now()

        timestamp = str(
            f"{now.year:04}{now.month:02}{now.day:02}-{now.hour:02}{now.minute:02}{now.second:02}-"
            f"{now.microsecond:06}"
        )

        name = f"Blended-From-{c.frags_name}-Time-{timestamp}.jpg"
        loc = _join(self._proj_path, name)
        image.save(loc, quality=95)
        self.logln(f"Saved blended blocks at: {loc}", 1)

    def _render_frags_grid_block(self, block_y, block_x):
        c = self._context

        index = c.index_matrix[block_y][block_x]
        loc = c.frag_locs[index]
        image = _pil_image_open(loc)

        size = c.frag_width, c.frag_height
        resample = pil_image.BICUBIC
        image = image.resize(size, resample=resample)

        x_flip = pil_image.FLIP_TOP_BOTTOM
        y_flip = pil_image.FLIP_LEFT_RIGHT
        flip = c.flip_matrix[block_y][block_x]

        if "x" in flip:
            image = image.transpose(x_flip)

        if "y" in flip:
            image = image.transpose(y_flip)

        rot_180 = pil_image.ROTATE_180
        rot = c.rot_matrix[block_y][block_x]

        if rot == "180":
            image = image.transpose(rot_180)

        image_np = _nparray(image, dtype=_npsingle)
        axis_order = [1, 0, 2]
        image_np = _nptranspose(image_np, axis_order)
        self.logln(f"Transposed the image with axis order: {axis_order}", 103)

        info = str(
            f"image_np:\n"
            f"{image_np}\n"
        )

        self.logstr(info, 105)
        self.logln(f"image_np shape: {image_np.shape}", 103)

        x1 = c.frags_grid_pad + block_x * (c.frag_width + c.frags_grid_pad)
        y1 = c.frags_grid_pad + block_y * (c.frag_height + c.frags_grid_pad)
        x2 = x1 + c.frag_width
        y2 = y1 + c.frag_height

        c.frags_grid[x1: x2, y1: y2] = image_np

    def _render_frags_grid(self):
        c = self._context

        if c.save_frags_grid:
            info = str(
                "Started rendering fragments grid\n"
                "-"
            )

            self.logln(info, 1)
            frags_grid: _np_ndarray = c.frags_grid
            frags_grid.fill(c.frags_grid_pad_bright)
            block_total = c.y_frag_count * c.x_frag_count
            cur_block = 0

            for iy in range(c.y_frag_count):
                for ix in range(c.x_frag_count):
                    self._render_frags_grid_block(iy, ix)

                    needs_log = \
                        cur_block + 1 == 1 or \
                        (cur_block + 1) % 360 == 0 or \
                        cur_block + 1 == block_total

                    if needs_log:
                        self.logln(f"Rendered fragments grid block: {cur_block + 1} / {block_total}", 1)

                    cur_block += 1
                # end for
            # end for

            self.logln(f"Fragments grid: {frags_grid}", 104)

            info = str(
                "-\n"
                "Completed rendering fragments grid"
            )

            self.logln(info, 1)
        # end if

    def _save_frags_grid(self):
        c = self._context

        if c.save_frags_grid:
            axis_order = [1, 0, 2]
            c.frags_grid = _nptranspose(c.frags_grid, axis_order)
            self.logln(f"Transposed the fragments grid with axis order {axis_order}", 101)
            frags_grid: _np_ndarray = c.frags_grid
            frags_grid = frags_grid.astype(_npubyte)
            image = _pil_image_fromarray(frags_grid, "RGB")
            now = _now()

            timestamp = str(
                f"{now.year:04}{now.month:02}{now.day:02}-{now.hour:02}{now.minute:02}{now.second:02}-"
                f"{now.microsecond:06}"
            )

            name = f"Frags-From-{c.frags_name}-Time-{timestamp}.jpg"
            loc = _join(self._proj_path, name)
            image.save(loc, quality=95)
            self.logln(f"Saved fragments grid at: {loc}", 1)
        # end if

    def _record_frag_locs(self):
        c = self._context

        if c.save_frag_locs:
            info = str(
                "Started recording fragment locations\n"
                "-"
            )

            self.logln(info, 1)
            block_total = c.y_frag_count * c.x_frag_count
            frag_loc_blocks = []
            cur_block = 0

            for iy in range(c.y_frag_count):
                frag_loc_row = []

                for ix in range(c.x_frag_count):
                    index = c.index_matrix[iy][ix]
                    loc = c.frag_locs[index]
                    flip = c.flip_matrix[iy][ix]

                    block = str(
                        f"- Fragment\n"
                        f"\n"
                        f"(X, Y): ({ix}, {iy})\n"
                        f"Image: \"{repr(loc)[1: -1]}\"\n"
                        f"Flip: \"{repr(flip)[1: -1]}\"\n"
                        f"\n"
                        f"- End of fragment\n"
                    )

                    frag_loc_row.append(block)

                    needs_log = \
                        cur_block + 1 == 1 or \
                        (cur_block + 1) % 720 == 0 or \
                        cur_block + 1 == block_total

                    if needs_log:
                        self.logln(f"Recorded fragment locations block: {cur_block + 1} / {block_total}", 1)

                    cur_block += 1
                # end for

                frag_loc_blocks.append(frag_loc_row)
            # end for

            c.frag_locs_text = ""

            for ix in range(c.x_frag_count):
                for iy in range(c.y_frag_count):
                    c.frag_locs_text += frag_loc_blocks[iy][ix]
                # end for
            # end for

            self.logln(f"Fragment locations: {c.frag_locs_text}", 103)

            info = str(
                "-\n"
                "Completed recording fragment locations"
            )

            self.logln(info, 1)
        # end if

    def _save_frag_locs(self):
        c = self._context

        if c.save_frag_locs:
            now = _now()

            timestamp = str(
                f"{now.year:04}{now.month:02}{now.day:02}-{now.hour:02}{now.minute:02}{now.second:02}-"
                f"{now.microsecond:06}"
            )

            name = f"Frag-Locations-From-{c.frags_name}-Time-{timestamp}.txt"
            loc = _join(self._proj_path, name)
            _save_text(c.frag_locs_text, loc)
            self.logln(f"Saved fragment locations at {loc}", 1)
        # end if

    def prep(self):
        """Prepares for blending."""
        info = str(
            "Blender started preparation\n"
            "-"
        )

        self.logln(info)
        self._read_config()
        self._parse_config()
        self._prep_frags()
        self._prep_matrices()
        self._prep_canvas()
        self._prep_frags_grid()
        self._tweak_pil_safety()

        info = str(
            "-\n"
            "Blender completed preparation"
        )

        self.logln(info)

    def blend(self):
        """Blends the frags into a large picture.

        Blends the frags in self.frags_path into a large picture in self.project_path.
        """
        info = str(
            "Started blending\n"
            "-"
        )

        self.logln(info)
        self._blend_blocks()
        self._save_blended_blocks()
        self._render_frags_grid()
        self._save_frags_grid()
        self._record_frag_locs()
        self._save_frag_locs()

        info = str(
            "-\n"
            "Completed blending"
        )

        self.logln(info)
