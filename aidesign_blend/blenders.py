"""Blenders."""

# Initially added by: liu-yucheng
# Last updated by: liu-yucheng

import datetime
import imghdr
import numpy
import os
import pathlib
import random
import typing

from PIL import Image as pil_image

from aidesign_blend import defaults
from aidesign_blend import grads
from aidesign_blend import utils

_Callable = typing.Callable
_join = os.path.join
_listdir = os.listdir
_Path = pathlib.Path
_randint = random.randint


class Blender:
    """Blender."""

    class Context(utils.DotDict):
        """Context."""
        rand_mode = None
        """Random mode."""
        rand_seed = None
        """Random seed."""
        rand_frags = None
        """Random fragments."""
        rand_flip = None
        """Random flipping."""
        save_fgrid = None
        """Save fragments grid."""
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
            utils.logstr(self.logs, string)

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
        self.logln("Blenders config location: {}".format(config_loc), 1)
        self.config = utils.load_json(config_loc)
        self.logln("Completed reading blenders config", 1)

    def _pad_coefs_exps(self, coefs, exps):
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

        manual_seed = self.config["manual_seed"]
        self.logln("manual_seed: {}".format(manual_seed), 101)
        if manual_seed is not None:
            manual_seed = int(manual_seed)
            manual_seed = manual_seed % (2 ** 32 - 1)

        if manual_seed is None:
            rand_mode = "Auto"
            random.seed(None)
            rand_seed = _randint(0, 2 ** 32 - 1)
        else:  # elif manual_seed is not None:
            rand_mode = "Manual"
            rand_seed = manual_seed
        random.seed(rand_seed)
        numpy.random.seed(rand_seed)

        c.rand_mode = rand_mode
        c.rand_seed = rand_seed
        self.logln("Random:  Mode: {}  Seed: {}".format(rand_mode, rand_seed), 1)

        rand_frags = self.config["random_frags"]
        self.logln("random_frags: {}".format(rand_frags), 101)
        rand_frags = bool(rand_frags)
        c.rand_frags = rand_frags
        self.logln("Random fragments: {}".format(rand_frags), 1)

        rand_flip = self.config["random_flipping"]
        self.logln("random_flipping: {}".format(rand_flip), 101)
        rand_flip = bool(rand_flip)
        c.rand_flip = rand_flip
        self.logln("Random flipping: {}".format(rand_flip), 1)

        frag_res = self.config["frag_resolution"]
        self.logln("frag_res: {}".format(frag_res), 101)
        frag_res = int(frag_res)
        if frag_res < 0:
            frag_res *= -1
        if frag_res < 2:
            frag_res = 2
        if not frag_res % 2 == 0:
            frag_res += 1
        c.frag_width = frag_res
        c.frag_height = frag_res
        self.logln("Fragment:  Width: {}  Height: {}".format(frag_res, frag_res), 1)

        x_frag_count = self.config["x_frag_count"]
        self.logln("x_frag_count: {}".format(x_frag_count), 101)
        x_frag_count = int(x_frag_count)
        if x_frag_count < 0:
            x_frag_count *= -1
        if x_frag_count < 2:
            x_frag_count = 2
        c.x_frag_count = x_frag_count

        y_frag_count = self.config["y_frag_count"]
        self.logln("y_frag_count: {}".format(y_frag_count), 101)
        y_frag_count = int(y_frag_count)
        if y_frag_count < 0:
            y_frag_count *= -1
        if y_frag_count < 2:
            y_frag_count = 2
        c.y_frag_count = y_frag_count

        self.logln("Fragment count:  X: {}  Y: {}".format(x_frag_count, y_frag_count), 1)

        fgrid_key = "frags_grid"
        save_key = "save"
        save_fgrid = False
        if fgrid_key in self.config:
            fgrid_config = self.config[fgrid_key]
        if save_key in fgrid_config:
            save_fgrid = fgrid_config[save_key]
            save_fgrid = bool(save_fgrid)

        self.logln("save_fgrid: {}".format(save_fgrid), 101)

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
            self.logstr(
                str(
                    "fgrid_padding: {}\n"
                    "fgrid_padding_bri: {}\n"
                ).format(
                    fgrid_padding,
                    fgrid_padding_bright
                ),
                101
            )
        # end if

        c.save_fgrid = save_fgrid
        c.fgrid_padding = fgrid_padding
        c.fgrid_padding_bright = fgrid_padding_bright

        self.logln("Save fragments grid: {}".format(save_fgrid), 1)

        if save_fgrid:
            self.logln(
                "Fragments grid:  Padding: {}  Padding brightness: {}".format(fgrid_padding, fgrid_padding_bright), 1
            )
        # end if

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

            grad_func = grads.Poly1V(coefs, exps)
        else:  # elif not cust_grad_enabled:
            grad_func = grads.LU()

        c.cust_grad_enabled = cust_grad_enabled
        c.grad_func = grad_func

        if cust_grad_enabled:
            grad_name = "custom"
        else:  # elif not cust_grad_enabled:
            grad_name = "default"
        self.logln("Prepared gradient function: {}".format(grad_name), 1)
        self.logln("Gradient function: \" {} \"".format(grad_func.fnstr()), 1)

        self.logln("Completed parsing blenders config", 1)

    def _read_frags_path(self, frags_path):
        frag_names = _listdir(frags_path)
        frag_names.sort()
        self.logln("frag_names: {}".format(frag_names), 102)
        frag_locs = []
        for name in frag_names:
            loc = _join(frags_path, name)
            frag_locs.append(loc)

        orig_frag_locs = frag_locs
        frag_locs = []
        for loc in orig_frag_locs:
            is_file = os.path.isfile(loc)
            is_img = is_file and imghdr.what(loc) is not None
            if is_img:
                frag_locs.append(loc)
        self.logln("frag_locs: {}".format(frag_locs), 102)
        frag_count = len(frag_locs)
        self.logln("frag_count: {}".format(frag_count), 101)

        return frag_locs

    def _prep_frags(self):
        c = self.context

        frags_path = self.frags_path
        frag_locs = self._read_frags_path(frags_path)
        frag_count = len(frag_locs)
        if frag_count <= 0:
            frags_path = defaults.default_frags_path
            self.logln("Found no fragments in frags_path, defaulting frags_path to: {}".format(frags_path), 1)
            frag_locs = self._read_frags_path(frags_path)
            frag_count = len(frag_locs)
        frags_name = _Path(frags_path).name

        c.frags_path = frags_path
        self.logln("Fragments path: {}".format(frags_path), 1)
        c.frags_name = frags_name
        self.logln("Fragments name: {}".format(frags_name), 1)
        c.frag_count = frag_count
        self.logln("Fragment count: {}".format(frag_count), 1)
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
        matrix = numpy.ndarray((x_size, y_size), dtype=numpy.single)
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

    def _prep_matrices(self):
        c = self.context

        idx_mtx = self._make_2d_matrix(c.y_frag_count, c.x_frag_count)
        if c.rand_frags:
            for iy in range(c.y_frag_count):
                for ix in range(c.x_frag_count):
                    idx_mtx[iy][ix] = _randint(0, c.frag_count - 1)
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
        self.logln("idx_mtx: {}".format(idx_mtx), 103)

        flip_mtx = self._make_2d_matrix(c.y_frag_count, c.x_frag_count)
        if c.rand_flip:
            for iy in range(c.y_frag_count):
                for ix in range(c.x_frag_count):
                    flip_x = utils.rand_bool()
                    flip_y = utils.rand_bool()
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
        self.logln("flip_mtx: {}".format(flip_mtx), 103)

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

                # Use normalized 2-d distances as blend factors
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

                ul_remain = utils.clamp(ul_remain, 0, 1)
                ur_remain = utils.clamp(ur_remain, 0, 1)
                ll_remain = utils.clamp(ll_remain, 0, 1)
                lr_remain = utils.clamp(lr_remain, 0, 1)

                remain_sum = ul_remain + ur_remain + ll_remain + lr_remain

                ul_fac = ul_remain / remain_sum
                ur_fac = ur_remain / remain_sum
                ll_fac = ll_remain / remain_sum
                lr_fac = lr_remain / remain_sum

                ul_bmtx[ix, iy] = ul_fac
                ur_bmtx[ix, iy] = ur_fac
                ll_bmtx[ix, iy] = ll_fac
                lr_bmtx[ix, iy] = lr_fac
            # end for
        # end for
        self.logstr(
            str(
                "bmtx:\n"
                "  ul:\n"
                "{}\n"
                "  ur:\n"
                "{}\n"
                "  ll:\n"
                "{}\n"
                "  lr:\n"
                "{}\n"
            ).format(
                ul_bmtx,
                ur_bmtx,
                ll_bmtx,
                lr_bmtx
            ),
            103
        )

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
        self.logln("Blend matrices:  Width: {}  Height: {}".format(width, height), 1)

    def _make_numpy_3d_matrix(self, x_size, y_size, z_size):
        matrix = numpy.ndarray((x_size, y_size, z_size), dtype=numpy.single)
        return matrix

    def _prep_canvas(self):
        c = self.context

        width = c.bmtx_width * (c.x_frag_count - 1)
        height = c.bmtx_height * (c.y_frag_count - 1)
        canvas = self._make_numpy_3d_matrix(width, height, 3)

        c.canvas_width = width
        c.canvas_height = height
        c.canvas = canvas

        self.logln("Prepared the canvas:  Width: {}  Height: {}".format(width, height), 1)

    def _prep_fgrid(self):
        c = self.context

        if c.save_fgrid:
            width = c.fgrid_padding + c.x_frag_count * (c.frag_width + c.fgrid_padding)
            height = c.fgrid_padding + c.y_frag_count * (c.frag_height + c.fgrid_padding)
            fgrid = self._make_numpy_3d_matrix(width, height, 3)
            self.logstr(
                str(
                    "width: {}\n"
                    "height: {}\n"
                ).format(
                    width,
                    height
                ),
                101
            )
            self.logstr(
                str(
                    "fgrid:\n"
                    "{}\n"
                ).format(fgrid),
                104
            )
            c.fgrid_width = width
            c.fgrid_height = height
            c.fgrid = fgrid
            self.logln("Prepared the fragments grid:  Width: {}  Height: {}".format(width, height), 1)
        # end if

    def _tweak_pil_safety(self):
        max_width = 65535
        max_height = 65535
        max_pixs = max_width * max_height
        pil_image.MAX_IMAGE_PIXELS = max_pixs
        self.logln("Tweaked PIL safety max pixels:  Width: {}  Height: {}".format(max_width, max_height), 1)

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

        ul_img = pil_image.open(ul_loc)
        ur_img = pil_image.open(ur_loc)
        ll_img = pil_image.open(ll_loc)
        lr_img = pil_image.open(lr_loc)

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

        ul_np = numpy.array(ul_img, dtype=numpy.single)
        ur_np = numpy.array(ur_img, dtype=numpy.single)
        ll_np = numpy.array(ll_img, dtype=numpy.single)
        lr_np = numpy.array(lr_img, dtype=numpy.single)

        axis_ord = [1, 0, 2]
        ul_np = numpy.transpose(ul_np, axis_ord)
        ur_np = numpy.transpose(ur_np, axis_ord)
        ll_np = numpy.transpose(ll_np, axis_ord)
        lr_np = numpy.transpose(lr_np, axis_ord)
        self.logln("Transposed the UL, UR, LL, LR images with axis order: {}".format(axis_ord), 103)

        self.logstr(
            str(
                "ul_np:\n"
                "{}\n"
                "ur_np:\n"
                "{}\n"
                "ll_np:\n"
                "{}\n"
                "lr_np:\n"
                "{}\n"
            ).format(
                ul_np,
                ur_np,
                ll_np,
                lr_np
            ),
            105
        )
        self.logstr(
            str(
                "ul_np shape: {}\n"
                "ur_np shape: {}\n"
                "ll_np shape: {}\n"
                "lr_np shape: {}\n"
            ).format(
                ul_np.shape,
                ur_np.shape,
                ll_np.shape,
                lr_np.shape
            ),
            103
        )

        block_r = numpy.multiply(c.ul_bmtx, ul_np[:, :, 0]) + \
            numpy.multiply(c.ur_bmtx, ur_np[:, :, 0]) + \
            numpy.multiply(c.ll_bmtx, ll_np[:, :, 0]) + \
            numpy.multiply(c.lr_bmtx, lr_np[:, :, 0])
        block_g = numpy.multiply(c.ul_bmtx, ul_np[:, :, 1]) + \
            numpy.multiply(c.ur_bmtx, ur_np[:, :, 1]) + \
            numpy.multiply(c.ll_bmtx, ll_np[:, :, 1]) + \
            numpy.multiply(c.lr_bmtx, lr_np[:, :, 1])
        block_b = numpy.multiply(c.ul_bmtx, ul_np[:, :, 2]) + \
            numpy.multiply(c.ur_bmtx, ur_np[:, :, 2]) + \
            numpy.multiply(c.ll_bmtx, ll_np[:, :, 2]) + \
            numpy.multiply(c.lr_bmtx, lr_np[:, :, 2])

        numpy.clip(block_r, 0, 255, block_r)
        numpy.clip(block_g, 0, 255, block_g)
        numpy.clip(block_b, 0, 255, block_b)

        self.logstr(
            str(
                "block_r: \n"
                "{}\n"
                "block_g: \n"
                "{}\n"
                "block_b: \n"
                "{}\n"
            ).format(
                block_r,
                block_g,
                block_b
            ),
            104
        )

        c.canvas[canvas_x1: canvas_x2, canvas_y1: canvas_y2, 0] = block_r
        c.canvas[canvas_x1: canvas_x2, canvas_y1: canvas_y2, 1] = block_g
        c.canvas[canvas_x1: canvas_x2, canvas_y1: canvas_y2, 2] = block_b

    def _blend(self):
        c = self.context

        total_block_count = (c.y_frag_count - 1) * (c.x_frag_count - 1)
        curr_block = 0

        for iy in range(c.y_frag_count - 1):
            for ix in range(c.x_frag_count - 1):
                self._blend_block(iy, ix)

                needs_log = curr_block + 1 == 1
                needs_log = needs_log or (curr_block + 1) % 180 == 0
                needs_log = needs_log or curr_block + 1 == total_block_count
                if needs_log:
                    self.logln("Blended block {} / {}".format(curr_block + 1, total_block_count), 1)
                curr_block += 1
            # end for
        # end for

        self.logln("Canvas: {}".format(c.canvas), 104)

    def _save_blended(self):
        c = self.context

        axis_ord = [1, 0, 2]
        c.canvas = numpy.transpose(c.canvas, axis_ord)
        self.logln("Transposed the canvas with axis order {}".format(axis_ord), 101)

        canvas: numpy.ndarray = c.canvas
        canvas = canvas.astype(numpy.ubyte)
        img = pil_image.fromarray(canvas, "RGB")
        now = datetime.datetime.now()
        timestamp = str(
            f"{now.year:04}{now.month:02}{now.day:02}-{now.hour:02}{now.minute:02}{now.second:02}-"
            f"{now.microsecond:06}"
        )
        img_name = "Blended-From-{}-Time-{}.jpg".format(c.frags_name, timestamp)
        img_loc = _join(self.proj_path, img_name)
        img.save(img_loc, quality=95)
        self.logln("Saved the blended image to: {}".format(img_loc), 1)

    def _render_fgrid_block(self, block_y, block_x):
        c = self.context

        idx = c.idx_mtx[block_y][block_x]
        loc = c.frag_locs[idx]

        img = pil_image.open(loc)

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

        img_np = numpy.array(img, dtype=numpy.single)
        axis_ord = [1, 0, 2]
        img_np = numpy.transpose(img_np, axis_ord)
        self.logln("Transposed the image with axis order: {}".format(axis_ord), 103)

        self.logstr(
            str(
                "img_np:\n"
                "{}\n"
            ).format(img_np),
            105
        )

        self.logln("img_np shape: {}".format(img_np.shape), 103)

        fgrid_x1 = c.fgrid_padding + block_x * (c.frag_width + c.fgrid_padding)
        fgrid_y1 = c.fgrid_padding + block_y * (c.frag_height + c.fgrid_padding)
        fgrid_x2 = fgrid_x1 + c.frag_width
        fgrid_y2 = fgrid_y1 + c.frag_height

        c.fgrid[fgrid_x1: fgrid_x2, fgrid_y1: fgrid_y2] = img_np

    def _render_fgrid(self):
        c = self.context

        if c.save_fgrid:
            total_block_count = c.y_frag_count * c.x_frag_count
            curr_block = 0
            c.fgrid.fill(c.fgrid_padding_bright)

            for iy in range(c.y_frag_count):
                for ix in range(c.x_frag_count):
                    self._render_fgrid_block(iy, ix)

                    needs_log = curr_block + 1 == 1
                    needs_log = needs_log or (curr_block + 1) % 360 == 0
                    needs_log = needs_log or curr_block + 1 == total_block_count
                    if needs_log:
                        self.logln(
                            "Rendered fragments grid block: {} / {}".format(curr_block + 1, total_block_count), 1
                        )
                    # end if
                    curr_block += 1
                # end for
            # end for

            self.logln("Fragments grid: {}".format(c.fgrid), 104)
        # end if

    def _save_fgrid(self):
        c = self.context

        if c.save_fgrid:
            axis_ord = [1, 0, 2]
            c.fgrid = numpy.transpose(c.fgrid, axis_ord)
            self.logln("Transposed the fragments grid with axis order {}".format(axis_ord), 101)

            fgrid: numpy.ndarray = c.fgrid
            fgrid = fgrid.astype(numpy.ubyte)
            img = pil_image.fromarray(fgrid, "RGB")
            now = datetime.datetime.now()
            timestamp = str(
                f"{now.year:04}{now.month:02}{now.day:02}-{now.hour:02}{now.minute:02}{now.second:02}-"
                f"{now.microsecond:06}"
            )
            img_name = "Frags-From-{}-Time-{}.jpg".format(c.frags_name, timestamp)
            img_loc = _join(self.proj_path, img_name)
            img.save(img_loc, quality=95)
            self.logln("Saved the frags grid to: {}".format(img_loc), 1)
        # end if

    def prep(self):
        """Prepares for blending."""
        self._read_config()
        self._parse_config()
        self._prep_frags()
        self._prep_matrices()
        self._prep_canvas()
        self._prep_fgrid()
        self._tweak_pil_safety()
        self.logln("Completed preparing the blender")

    def blend(self):
        """Blends the frags into a large picture.

        Blends the frags in self.frags_path into a large picture in self.project_path.
        """
        self._blend()
        self._save_blended()
        self._render_fgrid()
        self._save_fgrid()
        self.logln("Completed blending")
