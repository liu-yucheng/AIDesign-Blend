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

from aidesign_blend.libs import defaults
from aidesign_blend.libs import grads
from aidesign_blend.libs import utils

_Callable = typing.Callable
_clamp = utils.clamp_float
_DotDict = utils.DotDict
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


class Blender:
    """Blender."""

    class Context(_DotDict):
        """Context."""

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
        save_fgrid = None
        """Save fragments grid."""
        save_flocs = None
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

        idx_mtx = None
        """Index matrix. Subscripts [y][x]."""
        flip_mtx = None
        """Flipping matrix. Subscripts [y][x]."""
        bmtx_width = None
        """Blend matrix width."""
        bmtx_height = None
        """Blend matrix height."""
        ul_bmtx = None
        """Upper left blend matrix. Numpy array. Subscript [x, y]."""
        ur_bmtx = None
        """Upper right blend matrix. Numpy array. Subscript [x, y]."""
        ll_bmtx = None
        """Lower left blend matrix.Numpy array. Subscript [x, y]."""
        lr_bmtx = None
        """Lower right blend matrix. Numpy array. Subscript [x, y]."""

        canvas_width = None
        """Canvas width."""
        canvas_height = None
        """Canvas height."""
        canvas = None
        """Canvas. Numpy array. Subscript [x, y]."""

        fgrid_padding = None
        """Fragments grid padding."""
        fgrid_padding_bright = None
        """Fragments grid padding brightness."""
        fgrid_width = None
        """Fragments grid width."""
        fgrid_height = None
        """Fragments grid height."""
        fgrid = None
        """Fragments grid. Numpy array. Subscript [x, y]."""

        cust_grad_enabled = None
        """Custom gradient function enabled."""
        grad_func = None
        """Gradient function. Used to calculate the gradient progress. Input and output range [0, 1]."""

        flocs_text = None
        """Fragment locations text."""
    # end class

    def __init__(self, frags_path, proj_path, logs, debug_level=0):
        """Inits self with the given args."""
        self.frags_path = frags_path
        """Fragments path"""
        self.proj_path = proj_path
        """Project path"""
        self.logs = logs
        """Logs."""
        self.debug_level = debug_level
        """Debug level."""
        self.config = {}
        """Configuration."""
        self.context = type(self).Context()
        """Context."""

    def logstr(self, string="", debug_level=0):
        """Logs a string.

        Args:
            string: the string
            debug_level: the debug level
        """
        if debug_level <= self.debug_level:
            _logstr(self.logs, string)

    def logln(self, line="", debug_level=0):
        """Logs a line.

        Args:
            line: the line
            debug_level: the debug level
        """
        line += "\n"
        self.logstr(line, debug_level)

    def _read_config(self):
        config_loc = _join(self.proj_path, defaults.blenders_config_name)
        self.logln(f"Blenders config location: {config_loc}", 1)
        self.config = _load_json(config_loc)
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
        c = self.context

        # Parse manual_seed

        manual_seed = self.config["manual_seed"]
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

        rand_frags = self.config["random_frags"]
        self.logln(f"random_frags: {rand_frags}", 101)
        rand_frags = bool(rand_frags)
        c.rand_frags = rand_frags
        self.logln(f"Random fragments: {rand_frags}", 1)

        # End parse random_frags
        # Parse avoid_random_duplicates

        avoid_rand_dups_key = "avoid_random_duplicates"
        avoid_rand_dups = False

        if avoid_rand_dups_key in self.config:
            avoid_rand_dups = self.config[avoid_rand_dups_key]
            self.logln(f"avoid_rand_dups: {avoid_rand_dups}", 101)

        avoid_rand_dups = bool(avoid_rand_dups)
        c.avoid_rand_dups = avoid_rand_dups
        self.logln(f"Avoid random fragment duplicates: {avoid_rand_dups}", 1)

        # End parse avoid_random_duplicates
        # Parse random_flipping

        rand_flip = self.config["random_flipping"]
        self.logln(f"random_flipping: {rand_flip}", 101)
        rand_flip = bool(rand_flip)
        c.rand_flip = rand_flip
        self.logln(f"Random flipping: {rand_flip}", 1)

        # End parse random_flipping
        # Parse frag_resolution

        frag_res = self.config["frag_resolution"]
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

        x_frag_count = self.config["x_frag_count"]
        self.logln(f"x_frag_count: {x_frag_count}", 101)
        x_frag_count = int(x_frag_count)

        if x_frag_count < 0:
            x_frag_count *= -1

        if x_frag_count < 2:
            x_frag_count = 2

        c.x_frag_count = x_frag_count

        # End parse x_frag_count
        # Parse y_frag_count

        y_frag_count = self.config["y_frag_count"]
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

        save_flocs_key = "save_frag_locations"

        if save_flocs_key in self.config:
            save_flocs = bool(self.config[save_flocs_key])
        else:
            save_flocs = False

        self.logln(f"save_flocs: {save_flocs}", 101)
        c.save_flocs = save_flocs
        self.logln(f"Save fragment locations: {save_flocs}", 1)

        # End parse save_frag_locations
        # Parse frags_grid

        fgrid_key = "frags_grid"
        save_key = "save"
        save_fgrid = False

        if fgrid_key in self.config:
            fgrid_config = self.config[fgrid_key]

        if save_key in fgrid_config:
            save_fgrid = fgrid_config[save_key]
            save_fgrid = bool(save_fgrid)

        self.logln(f"save_fgrid: {save_fgrid}", 101)

        if save_fgrid:
            fgrid_padding = fgrid_config["padding"]
            fgrid_padding = int(fgrid_padding)

            if fgrid_padding < 0:
                fgrid_padding *= -1

            fgrid_padding_bright = fgrid_config["padding_brightness"]
            fgrid_padding_bright = int(fgrid_padding_bright)

            if fgrid_padding_bright < 0:
                fgrid_padding_bright *= -1

            if fgrid_padding_bright > 255:
                fgrid_padding_bright = 255

        else:  # elif not save_fgrid:
            fgrid_padding = None
            fgrid_padding_bright = None
        # end if

        if save_fgrid:
            info = str(
                f"fgrid_padding: {fgrid_padding}\n"
                f"fgrid_padding_bright: {fgrid_padding_bright}\n"
            )

            self.logstr(info, 101)
        # end if

        c.save_fgrid = save_fgrid
        c.fgrid_padding = fgrid_padding
        c.fgrid_padding_bright = fgrid_padding_bright
        self.logln(f"Save fragments grid: {save_fgrid}", 1)

        if save_fgrid:
            self.logln(f"Fragments grid:  Padding: {fgrid_padding}  Padding brightness: {fgrid_padding_bright}", 1)

        # End parse frags_grid
        # Parse custom_gradient

        cust_grad_enabled = False
        cust_grad_key = "custom_gradient"

        if cust_grad_key in self.config:
            cust_grad_enabled = self.config[cust_grad_key]["enabled"]
            cust_grad_enabled = bool(cust_grad_enabled)

        if cust_grad_enabled:
            cgrad_config = self.config[cust_grad_key]
            coefs = cgrad_config["coefficients"]
            exps = cgrad_config["exponents"]
            coefs, exps = self._pad_coefs_exps(coefs, exps)
            grad_func = _Poly1V(coefs, exps)
        else:  # elif not cust_grad_enabled:
            grad_func = _LU()
        # end if

        c.cust_grad_enabled = cust_grad_enabled
        c.grad_func = grad_func

        if cust_grad_enabled:
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
        c = self.context

        frags_path = self.frags_path
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

    def _grad_prog(self, idx, count):
        idx = int(idx)
        count = int(count)
        c = self.context

        last_idx = count - 1
        float_idx = float(idx)
        float_last_idx = float(last_idx)
        line_prog = float_idx / float_last_idx

        grad_func: _Callable[..., float] = c.grad_func
        prog = grad_func(line_prog)
        return prog

    def _gen_rand_frag_idxs(self):
        c = self.context

        idxs = [idx for idx in range(c.frag_count)]
        _shuffle(idxs)

        result = idxs
        return result

    def _prep_matrices(self):
        c = self.context

        # Make index matrix

        idx_mtx = self._make_2d_matrix(c.y_frag_count, c.x_frag_count)

        if c.avoid_rand_dups:
            remain_idxs = self._gen_rand_frag_idxs()
        else:  # elif not c.avoid_rand_dups:
            remain_idxs = None
        # end if

        if c.rand_frags:
            for iy in range(c.y_frag_count):
                for ix in range(c.x_frag_count):
                    if c.avoid_rand_dups:
                        remain_idxs_len = len(remain_idxs)

                        if remain_idxs_len <= 0:
                            remain_idxs = self._gen_rand_frag_idxs()

                        idx_mtx[iy][ix] = remain_idxs.pop(0)
                    else:  # elif not c.avoid_rand_dups:
                        idx_mtx[iy][ix] = _randint(0, c.frag_count - 1)
                    # end if
                # end for
            # end for
        else:  # elif not c.rand_frags:
            idx = 0

            for iy in range(c.y_frag_count):
                for ix in range(c.x_frag_count):
                    idx_mtx[iy][ix] = idx
                    idx = (idx + 1) % c.frag_count
                # end for
            # end for
        # end if

        self.logln(f"idx_mtx: {idx_mtx}", 103)

        # End make index matrix
        # Make flip matrix

        flip_mtx = self._make_2d_matrix(c.y_frag_count, c.x_frag_count)

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

                    flip_mtx[iy][ix] = flip
                # end for
            # end for
        else:  # elif not c.rand_flip:
            for iy in range(c.y_frag_count):
                for ix in range(c.x_frag_count):
                    flip_mtx[iy][ix] = ""
                # end for
            # end for
        # end if

        self.logln(f"flip_mtx: {flip_mtx}", 103)

        # End make flip matrix
        # Make blend matrices

        width = c.frag_width // 2
        height = c.frag_height // 2
        ul_bmtx = self._make_numpy_2d_matrix(width, height)
        ur_bmtx = self._make_numpy_2d_matrix(width, height)
        ll_bmtx = self._make_numpy_2d_matrix(width, height)
        lr_bmtx = self._make_numpy_2d_matrix(width, height)

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

                ul_bmtx[ix, iy] = ul_fac
                ur_bmtx[ix, iy] = ur_fac
                ll_bmtx[ix, iy] = ll_fac
                lr_bmtx[ix, iy] = lr_fac
            # end for
        # end for

        info = str(
            f"bmtx:\n"
            f"  ul:\n"
            f"{ul_bmtx}\n"
            f"  ur:\n"
            f"{ur_bmtx}\n"
            f"  ll:\n"
            f"{ll_bmtx}\n"
            f"  lr:\n"
            f"{lr_bmtx}\n"
        )

        self.logstr(info, 103)

        # End make blend matrices

        c.idx_mtx = idx_mtx
        self.logln("Prepared the index matrix", 1)
        c.flip_mtx = flip_mtx
        self.logln("Prepared the flipping matrix", 1)
        c.bmtx_width = width
        c.bmtx_height = height
        c.ul_bmtx = ul_bmtx
        c.ur_bmtx = ur_bmtx
        c.ll_bmtx = ll_bmtx
        c.lr_bmtx = lr_bmtx
        self.logln("Prepared 4 blend matrices:  Upper-left  Upper-right  Lower-left  Lower-right", 1)
        self.logln(f"Blend matrices:  Width: {width}  Height: {height}", 1)

    def _make_numpy_3d_matrix(self, x_size, y_size, z_size):
        matrix = _np_ndarray((x_size, y_size, z_size), dtype=_npsingle)
        return matrix

    def _prep_canvas(self):
        c = self.context

        width = c.bmtx_width * (c.x_frag_count - 1)
        height = c.bmtx_height * (c.y_frag_count - 1)
        canvas = self._make_numpy_3d_matrix(width, height, 3)

        c.canvas_width = width
        c.canvas_height = height
        c.canvas = canvas

        self.logln(f"Prepared the canvas:  Width: {width}  Height: {height}", 1)

    def _prep_fgrid(self):
        c = self.context

        if c.save_fgrid:
            width = c.fgrid_padding + c.x_frag_count * (c.frag_width + c.fgrid_padding)
            height = c.fgrid_padding + c.y_frag_count * (c.frag_height + c.fgrid_padding)
            fgrid = self._make_numpy_3d_matrix(width, height, 3)

            info = str(
                f"width: {width}\n"
                f"height: {height}\n"
            )

            self.logstr(info, 101)

            info = str(
                f"fgrid:\n"
                f"{fgrid}\n"
            )

            self.logstr(info, 104)
            c.fgrid_width = width
            c.fgrid_height = height
            c.fgrid = fgrid
            self.logln(f"Prepared the fragments grid:  Width: {width}  Height: {height}", 1)
        # end if

    def _tweak_pil_safety(self):
        max_width = 65535
        max_height = 65535
        max_pixs = max_width * max_height
        pil_image.MAX_IMAGE_PIXELS = max_pixs
        self.logln(f"Tweaked PIL safety max pixels:  Width: {max_width}  Height: {max_height}  Total: {max_pixs}", 1)

    def _blend_block(self, block_y, block_x):
        c = self.context

        canvas_x1 = block_x * c.bmtx_width
        canvas_y1 = block_y * c.bmtx_height
        canvas_x2 = canvas_x1 + c.bmtx_width
        canvas_y2 = canvas_y1 + c.bmtx_height

        ul_box = c.bmtx_width, c.bmtx_height, c.frag_width, c.frag_height
        ur_box = 0, c.bmtx_height, c.bmtx_width, c.frag_height
        ll_box = c.bmtx_width, 0, c.frag_width, c.bmtx_height
        lr_box = 0, 0, c.bmtx_width, c.bmtx_height

        uly, ulx = block_y, block_x
        ury, urx = uly, ulx + 1
        lly, llx = uly + 1, ulx
        lry, lrx = uly + 1, ulx + 1

        ul_idx = c.idx_mtx[uly][ulx]
        ur_idx = c.idx_mtx[ury][urx]
        ll_idx = c.idx_mtx[lly][llx]
        lr_idx = c.idx_mtx[lry][lrx]

        ul_flip = c.flip_mtx[uly][ulx]
        ur_flip = c.flip_mtx[ury][urx]
        ll_flip = c.flip_mtx[lly][llx]
        lr_flip = c.flip_mtx[lry][lrx]

        ul_loc = c.frag_locs[ul_idx]
        ur_loc = c.frag_locs[ur_idx]
        ll_loc = c.frag_locs[ll_idx]
        lr_loc = c.frag_locs[lr_idx]

        ul_img = _pil_image_open(ul_loc)
        ur_img = _pil_image_open(ur_loc)
        ll_img = _pil_image_open(ll_loc)
        lr_img = _pil_image_open(lr_loc)

        size = c.frag_width, c.frag_height
        resample = pil_image.BICUBIC
        ul_img = ul_img.resize(size=size, resample=resample)
        ur_img = ur_img.resize(size=size, resample=resample)
        ll_img = ll_img.resize(size=size, resample=resample)
        lr_img = lr_img.resize(size=size, resample=resample)

        xflip = pil_image.FLIP_TOP_BOTTOM
        yflip = pil_image.FLIP_LEFT_RIGHT

        if "x" in ul_flip:
            ul_img = ul_img.transpose(xflip)

        if "y" in ul_flip:
            ul_img = ul_img.transpose(yflip)

        if "x" in ur_flip:
            ur_img = ur_img.transpose(xflip)

        if "y" in ur_flip:
            ur_img = ur_img.transpose(yflip)

        if "x" in ll_flip:
            ll_img = ll_img.transpose(xflip)

        if "y" in ll_flip:
            ll_img = ll_img.transpose(yflip)

        if "x" in lr_flip:
            lr_img = lr_img.transpose(xflip)

        if "y" in lr_flip:
            lr_img = lr_img.transpose(yflip)

        ul_img = ul_img.crop(ul_box)
        ur_img = ur_img.crop(ur_box)
        ll_img = ll_img.crop(ll_box)
        lr_img = lr_img.crop(lr_box)

        ul_np = _nparray(ul_img, dtype=_npsingle)
        ur_np = _nparray(ur_img, dtype=_npsingle)
        ll_np = _nparray(ll_img, dtype=_npsingle)
        lr_np = _nparray(lr_img, dtype=_npsingle)

        axis_ord = [1, 0, 2]
        ul_np = _nptranspose(ul_np, axis_ord)
        ur_np = _nptranspose(ur_np, axis_ord)
        ll_np = _nptranspose(ll_np, axis_ord)
        lr_np = _nptranspose(lr_np, axis_ord)
        self.logln(f"Transposed the UL, UR, LL, LR images with axis order: {axis_ord}", 103)

        info = str(
            f"ul_np:\n"
            f"{ul_np}\n"
            f"ur_np:\n"
            f"{ur_np}\n"
            f"ll_np:\n"
            f"{ll_np}\n"
            f"lr_np:\n"
            f"{lr_np}\n"
        )

        self.logstr(info, 105)

        info = str(
            f"ul_np shape: {ul_np.shape}\n"
            f"ur_np shape: {ur_np.shape}\n"
            f"ll_np shape: {ll_np.shape}\n"
            f"lr_np shape: {lr_np.shape}\n"
        )

        self.logstr(info, 103)

        block_r = _npmultiply(c.ul_bmtx, ul_np[:, :, 0]) + \
            _npmultiply(c.ur_bmtx, ur_np[:, :, 0]) + \
            _npmultiply(c.ll_bmtx, ll_np[:, :, 0]) + \
            _npmultiply(c.lr_bmtx, lr_np[:, :, 0])

        block_g = _npmultiply(c.ul_bmtx, ul_np[:, :, 1]) + \
            _npmultiply(c.ur_bmtx, ur_np[:, :, 1]) + \
            _npmultiply(c.ll_bmtx, ll_np[:, :, 1]) + \
            _npmultiply(c.lr_bmtx, lr_np[:, :, 1])

        block_b = _npmultiply(c.ul_bmtx, ul_np[:, :, 2]) + \
            _npmultiply(c.ur_bmtx, ur_np[:, :, 2]) + \
            _npmultiply(c.ll_bmtx, ll_np[:, :, 2]) + \
            _npmultiply(c.lr_bmtx, lr_np[:, :, 2])

        _npclip(block_r, 0, 255, block_r)
        _npclip(block_g, 0, 255, block_g)
        _npclip(block_b, 0, 255, block_b)

        info = str(
            f"block_r: \n"
            f"{block_r}\n"
            f"block_g: \n"
            f"{block_g}\n"
            f"block_b: \n"
            f"{block_b}\n"
        )

        self.logstr(info, 104)
        c.canvas[canvas_x1: canvas_x2, canvas_y1: canvas_y2, 0] = block_r
        c.canvas[canvas_x1: canvas_x2, canvas_y1: canvas_y2, 1] = block_g
        c.canvas[canvas_x1: canvas_x2, canvas_y1: canvas_y2, 2] = block_b

    def _blend_blocks(self):
        c = self.context

        info = str(
            "Started blending blocks\n"
            "-"
        )

        self.logln(info)
        total_block_count = (c.y_frag_count - 1) * (c.x_frag_count - 1)
        curr_block = 0

        for iy in range(c.y_frag_count - 1):
            for ix in range(c.x_frag_count - 1):
                self._blend_block(iy, ix)

                needs_log = curr_block + 1 == 1
                needs_log = needs_log or (curr_block + 1) % 180 == 0
                needs_log = needs_log or curr_block + 1 == total_block_count

                if needs_log:
                    self.logln(f"Blended block {curr_block + 1} / {total_block_count}", 1)

                curr_block += 1
            # end for
        # end for

        self.logln(f"Canvas: {c.canvas}", 104)

        info = str(
            "-\n"
            "Completed blending blocks"
        )

        self.logln(info)

    def _save_blended_blocks(self):
        c = self.context

        axis_ord = [1, 0, 2]
        c.canvas = _nptranspose(c.canvas, axis_ord)
        self.logln(f"Transposed the canvas with axis order {axis_ord}", 101)
        canvas: _np_ndarray = c.canvas
        canvas = canvas.astype(_npubyte)
        img = _pil_image_fromarray(canvas, "RGB")
        now = _now()

        timestamp = str(
            f"{now.year:04}{now.month:02}{now.day:02}-{now.hour:02}{now.minute:02}{now.second:02}-"
            f"{now.microsecond:06}"
        )

        img_name = f"Blended-From-{c.frags_name}-Time-{timestamp}.jpg"
        img_loc = _join(self.proj_path, img_name)
        img.save(img_loc, quality=95)
        self.logln(f"Saved blended blocks at: {img_loc}", 1)

    def _render_fgrid_block(self, block_y, block_x):
        c = self.context

        idx = c.idx_mtx[block_y][block_x]
        loc = c.frag_locs[idx]
        img = _pil_image_open(loc)

        size = c.frag_width, c.frag_height
        resample = pil_image.BICUBIC
        img = img.resize(size, resample=resample)

        xflip = pil_image.FLIP_TOP_BOTTOM
        yflip = pil_image.FLIP_LEFT_RIGHT
        flip = c.flip_mtx[block_y][block_x]

        if "x" in flip:
            img = img.transpose(xflip)

        if "y" in flip:
            img = img.transpose(yflip)

        img_np = _nparray(img, dtype=_npsingle)
        axis_ord = [1, 0, 2]
        img_np = _nptranspose(img_np, axis_ord)
        self.logln(f"Transposed the image with axis order: {axis_ord}", 103)

        info = str(
            f"img_np:\n"
            f"{img_np}\n"
        )

        self.logstr(info, 105)
        self.logln(f"img_np shape: {img_np.shape}", 103)

        fgrid_x1 = c.fgrid_padding + block_x * (c.frag_width + c.fgrid_padding)
        fgrid_y1 = c.fgrid_padding + block_y * (c.frag_height + c.fgrid_padding)
        fgrid_x2 = fgrid_x1 + c.frag_width
        fgrid_y2 = fgrid_y1 + c.frag_height

        c.fgrid[fgrid_x1: fgrid_x2, fgrid_y1: fgrid_y2] = img_np

    def _render_fgrid(self):
        c = self.context

        if c.save_fgrid:
            info = str(
                "Started rendering fragments grid\n"
                "-"
            )

            self.logln(info)
            fgrid: _np_ndarray = c.fgrid
            fgrid.fill(c.fgrid_padding_bright)
            total_block_count = c.y_frag_count * c.x_frag_count
            curr_block = 0

            for iy in range(c.y_frag_count):
                for ix in range(c.x_frag_count):
                    self._render_fgrid_block(iy, ix)

                    needs_log = curr_block + 1 == 1
                    needs_log = needs_log or (curr_block + 1) % 360 == 0
                    needs_log = needs_log or curr_block + 1 == total_block_count

                    if needs_log:
                        self.logln(f"Rendered fragments grid block: {curr_block + 1} / {total_block_count}", 1)

                    curr_block += 1
                # end for
            # end for

            self.logln(f"Fragments grid: {fgrid}", 104)

            info = str(
                "-\n"
                "Completed rendering fragments grid"
            )

            self.logln(info)
        # end if

    def _save_fgrid(self):
        c = self.context

        if c.save_fgrid:
            axis_ord = [1, 0, 2]
            c.fgrid = _nptranspose(c.fgrid, axis_ord)
            self.logln(f"Transposed the fragments grid with axis order {axis_ord}", 101)
            fgrid: _np_ndarray = c.fgrid
            fgrid = fgrid.astype(_npubyte)
            img = _pil_image_fromarray(fgrid, "RGB")
            now = _now()

            timestamp = str(
                f"{now.year:04}{now.month:02}{now.day:02}-{now.hour:02}{now.minute:02}{now.second:02}-"
                f"{now.microsecond:06}"
            )

            img_name = f"Frags-From-{c.frags_name}-Time-{timestamp}.jpg"
            img_loc = _join(self.proj_path, img_name)
            img.save(img_loc, quality=95)
            self.logln(f"Saved fragments grid at: {img_loc}", 1)
        # end if

    def _record_flocs(self):
        c = self.context

        if c.save_flocs:
            info = str(
                "Started recording fragment locations\n"
                "-"
            )

            self.logln(info)
            total_block_count = c.y_frag_count * c.x_frag_count
            flocs_blocks = []
            curr_block = 0

            for iy in range(c.y_frag_count):
                flocs_row = []

                for ix in range(c.x_frag_count):
                    idx = c.idx_mtx[iy][ix]
                    loc = c.frag_locs[idx]
                    flip = c.flip_mtx[iy][ix]

                    block = str(
                        f"- Fragment\n"
                        f"\n"
                        f"(X, Y): ({ix}, {iy})\n"
                        f"Image: {loc}\n"
                        f"Flip: \"{flip}\"\n"
                        f"\n"
                        f"- End of fragment\n"
                    )

                    flocs_row.append(block)

                    needs_log = \
                        curr_block + 1 == 1 or \
                        (curr_block + 1) % 720 == 0 or \
                        curr_block + 1 == total_block_count

                    if needs_log:
                        self.logln(f"Recorded fragment locations block: {curr_block + 1} / {total_block_count}", 1)

                    curr_block += 1
                # end for

                flocs_blocks.append(flocs_row)
            # end for

            c.flocs_text = ""

            for ix in range(c.x_frag_count):
                for iy in range(c.y_frag_count):
                    c.flocs_text += flocs_blocks[iy][ix]
                # end for
            # end for

            self.logln(f"Fragment locations: {c.flocs_text}", 103)

            info = str(
                "-\n"
                "Completed recording fragment locations"
            )

            self.logln(info)
        # end if

    def _save_flocs(self):
        c = self.context

        if c.save_flocs:
            now = _now()

            timestamp = str(
                f"{now.year:04}{now.month:02}{now.day:02}-{now.hour:02}{now.minute:02}{now.second:02}-"
                f"{now.microsecond:06}"
            )

            name = f"Frag-Locations-From-{c.frags_name}-Time-{timestamp}.txt"
            loc = _join(self.proj_path, name)
            _save_text(c.flocs_text, loc)
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
        self._prep_fgrid()
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
        self._render_fgrid()
        self._save_fgrid()
        self._record_flocs()
        self._save_flocs()

        info = str(
            "-\n"
            "Completed blending"
        )

        self.logln(info)
