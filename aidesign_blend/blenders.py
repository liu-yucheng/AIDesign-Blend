"""Blenders."""

# Initially added by: liu-yucheng
# Last updated by: liu-yucheng

import datetime
import imghdr
import numpy
import os
import pathlib
import random

from PIL import Image as pil_image

from aidesign_blend import defaults
from aidesign_blend import utils

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
        frag_res = None
        """Fragment resolution."""
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

    def _parse_config(self):
        c = self.context

        manual_seed = self.config["manual_seed"]
        self.logln("Parsed manual_seed: {}".format(manual_seed), 2)
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
        self.logln("random_frags: {}".format(rand_frags), 2)
        rand_frags = bool(rand_frags)
        c.rand_frags = rand_frags
        self.logln("Random fragments: {}".format(rand_frags), 1)

        rand_flip = self.config["random_flipping"]
        self.logln("random_flipping: {}".format(rand_flip), 2)
        rand_flip = bool(rand_flip)
        c.rand_flip = rand_flip
        self.logln("Random flipping: {}".format(rand_flip), 1)

        frag_res = self.config["frag_resolution"]
        self.logln("frag_resolution: {}".format(frag_res), 2)
        frag_res = int(frag_res)
        if frag_res < 0:
            frag_res *= -1
        if frag_res < 2:
            frag_res = 2
        if not frag_res % 2 == 0:
            frag_res += 1
        c.frag_res = frag_res
        c.frag_width = frag_res
        c.frag_height = frag_res
        self.logln("Fragment resolution: {}".format(frag_res), 1)

        x_frag_count = self.config["x_frag_count"]
        self.logln("x_frag_count: {}".format(x_frag_count), 2)
        x_frag_count = int(x_frag_count)
        if x_frag_count < 0:
            x_frag_count *= -1
        if x_frag_count < 2:
            x_frag_count = 2
        c.x_frag_count = x_frag_count
        self.logln("X fragment count: {}".format(x_frag_count), 1)

        y_frag_count = self.config["y_frag_count"]
        self.logln("y_frag_count: {}".format(y_frag_count), 2)
        y_frag_count = int(y_frag_count)
        if y_frag_count < 0:
            y_frag_count *= -1
        if y_frag_count < 2:
            y_frag_count = 2
        c.y_frag_count = y_frag_count
        self.logln("Y fragment count: {}".format(y_frag_count), 1)

        self.logln("Completed parsing blenders config", 1)

    def _read_frags_path(self, frags_path):
        frag_names = _listdir(frags_path)
        frag_names.sort()
        self.logln("frag_names: {}".format(frag_names), 3)
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
        self.logln("frag_locs: {}".format(frag_locs), 3)
        frag_count = len(frag_locs)
        self.logln("frag_count: {}".format(frag_count), 2)

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
        matrix = numpy.ndarray((x_size, y_size), dtype=numpy.float32)
        return matrix

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
        self.logln("idx_mtx: {}".format(idx_mtx), 4)

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
        self.logln("flip_mtx: {}".format(flip_mtx), 4)

        w = c.frag_width // 2  # Width
        h = c.frag_height // 2  # Height
        ul_bmtx = self._make_numpy_2d_matrix(w, h)
        ur_bmtx = self._make_numpy_2d_matrix(w, h)
        ll_bmtx = self._make_numpy_2d_matrix(w, h)
        lr_bmtx = self._make_numpy_2d_matrix(w, h)
        for iy in range(h):
            for ix in range(w):
                h2 = h - 1
                w2 = w - 1

                iy_over_h2 = iy / h2
                ix_over_w2 = ix / w2

                ul_fac = (1 - iy_over_h2) * (1 - ix_over_w2)
                ur_fac = (1 - iy_over_h2) * ix_over_w2
                ll_fac = iy_over_h2 * (1 - ix_over_w2)
                lr_fac = iy_over_h2 * ix_over_w2

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
            4
        )

        c.idx_mtx = idx_mtx
        self.logln("Prepared the index matrix", 1)
        c.flip_mtx = flip_mtx
        self.logln("Prepared the flipping matrix", 1)
        c.bmtx_width = w
        c.bmtx_height = h
        c.ul_bmtx = ul_bmtx
        c.ur_bmtx = ur_bmtx
        c.ll_bmtx = ll_bmtx
        c.lr_bmtx = lr_bmtx
        self.logln("Prepared 4 blend matrices:  Upper-left  Upper-right  Lower-left  Lower-right", 1)
        self.logln("Blend matrices:  Width: {}  Height: {}".format(w, h), 1)

    def _make_numpy_3d_matrix(self, x_size, y_size, z_size):
        matrix = numpy.ndarray((x_size, y_size, z_size), dtype=numpy.float32)
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

    def _tweak_pil_safety(self):
        max_width = 65535
        max_height = 65535
        max_pixs = max_width * max_height
        pil_image.MAX_IMAGE_PIXELS = max_pixs
        self.logln("Tweaked PIL max image pixels:  Width: {}  Height: {}".format(max_width, max_height), 1)

    def prep(self):
        """Prepares for blending."""
        self._read_config()
        self._parse_config()
        self._prep_frags()
        self._prep_matrices()
        self._prep_canvas()
        self._tweak_pil_safety()
        self.logln("Completed preparing the blender")

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

        ul_np = numpy.array(ul_img, dtype=numpy.float32)
        ur_np = numpy.array(ur_img, dtype=numpy.float32)
        ll_np = numpy.array(ll_img, dtype=numpy.float32)
        lr_np = numpy.array(lr_img, dtype=numpy.float32)

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
            6
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
            4
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
            5
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
                needs_log = needs_log or (curr_block + 1) % 15 == 0
                needs_log = needs_log or curr_block + 1 == total_block_count
                if needs_log:
                    self.logln("Blended: Block {} / {}".format(curr_block + 1, total_block_count))
                curr_block += 1
            # end for
        # end for

        self.logln("Canvas: {}".format(c.canvas), 4)

    def _save_blended(self):
        c = self.context

        canvas: numpy.ndarray = c.canvas
        canvas = canvas.astype("uint8")
        bimg = pil_image.fromarray(canvas, "RGB")
        now = datetime.datetime.now()
        timestamp = str(
            f"{now.year:04}{now.month:02}{now.day:02}-{now.hour:02}{now.minute:02}{now.second:02}-"
            f"{now.microsecond:06}"
        )
        bimg_name = "Blended-From-{}-Time-{}.jpg".format(c.frags_name, timestamp)
        bimg_loc = _join(self.proj_path, bimg_name)
        bimg.save(bimg_loc, quality=95)
        self.logln("Saved the blended image to: {}".format(bimg_loc))

    def blend(self):
        """Blends the frags into a large picture.

        Blends the frags in self.frags_path into a large picture in self.project_path.
        """
        self._blend()
        self._save_blended()
        self.logln("Completed blending")
