"""Configurations."""

# Copyright 2022 Yucheng Liu. GNU GPL3 license.
# GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt
# First added by username: liu-yucheng
# Last updated by username: liu-yucheng

from os import path as ospath

from aidesign_blend.libs import defaults
from aidesign_blend.libs import utils

_join = ospath.join
_load_json = utils.load_json
_save_json = utils.save_json


class Config:
    """Config base class."""

    default_loc = None
    """Default location."""
    default_name = None
    """Default name."""

    @classmethod
    def load(cls, from_file):
        """Loads the config from a file to a dict.

        Args:
            from_file: a file location

        Returns:
            to_dict: the loaded dict
        """
        from_file = str(from_file)
        to_dict = _load_json(from_file)
        to_dict = dict(to_dict)
        return to_dict

    @classmethod
    def load_default(cls):
        """Loads the default config.

        Returns:
            result: the result
        """
        result = cls.load(cls.default_loc)
        return result

    @classmethod
    def load_from_path(cls, path):
        """Loads the config named cls.default_name from a path.

        Args:
            path: a path

        Returns:
            result: the result
        """
        path = str(path)
        loc = _join(path, cls.default_name)
        result = cls.load(loc)
        return result

    @classmethod
    def save(cls, from_dict, to_file):
        """Saves a config from a dict to a file.

        Args:
            from_dict: a status dict to save
            to_file: a file location
        """
        from_dict = dict(from_dict)
        to_file = str(to_file)
        _save_json(from_dict, to_file)

    @classmethod
    def save_to_path(cls, from_dict, path):
        """Saves the config from a dict to a file named cls.default_name in a path.

        Args:
            from_dict: a dict to save
            path: a path
        """
        from_dict: dict = from_dict
        path = str(path)
        loc = _join(path, cls.default_name)
        cls.save(from_dict, loc)

    @classmethod
    def verify(cls, from_dict):
        """Verifies a config from a dict.

        Args:
            from_dict: a status dictionary to verify

        Returns:
            result: the verified dict"""
        from_dict: dict = from_dict
        result = from_dict
        return result


class BlendersConfig(Config):
    """Blenders config."""

    default_loc = _join(defaults.default_blend_project_path, defaults.blenders_config_name)
    default_name = defaults.blenders_config_name

    @classmethod
    def _verify_int_nonable(cls, from_dict, key):
        val = from_dict[key]

        if val is not None:
            val = int(val)

        from_dict[key] = val

    @classmethod
    def _verify_bool(cls, from_dict, key):
        val = from_dict[key]
        val = bool(val)
        from_dict[key] = val

    @classmethod
    def _verify_int_ge_2_even(cls, from_dict, key):
        val = from_dict[key]
        val = int(val)

        if val < 0:
            val *= -1

        if val < 2:
            val = 2

        if not val % 2 == 0:
            val += 1

        from_dict[key] = val

    @classmethod
    def _verify_int_ge_2(cls, from_dict, key):
        val = from_dict[key]
        val = int(val)

        if val < 0:
            val *= -1

        if val < 2:
            val = 2

        from_dict[key] = val

    @classmethod
    def _verify_int_ge_0(cls, from_dict, key):
        val = from_dict[key]
        val = int(val)

        if val < 0:
            val *= -1

        from_dict[key] = val

    @classmethod
    def _verify_int_ge_0_le_255(cls, from_dict, key):
        val = from_dict[key]
        val = int(val)

        if val < 0:
            val *= -1

        if val > 255:
            val = 255

        from_dict[key] = val

    @classmethod
    def _verify_float_list(cls, from_dict, key):
        val = from_dict[key]
        val = [float(elem) for elem in val]
        from_dict[key] = val

    @classmethod
    def verify(cls, from_dict):
        from_dict: dict = from_dict
        from_dict = super().verify(from_dict)

        cls._verify_int_nonable(from_dict, "manual_seed")
        cls._verify_bool(from_dict, "random_frags")
        avoid_rand_dups_key = "avoid_random_duplicates"

        if avoid_rand_dups_key in from_dict:
            cls._verify_bool(from_dict, avoid_rand_dups_key)
        else:
            from_dict[avoid_rand_dups_key] = False
        # end if

        cls._verify_bool(from_dict, "random_flipping")
        rand_rot_key = "random_rotating"

        if rand_rot_key in from_dict:
            cls._verify_bool(from_dict, rand_rot_key)
        else:
            from_dict[rand_rot_key] = False
        # end if

        cls._verify_int_ge_2_even(from_dict, "frag_resolution")
        cls._verify_int_ge_2(from_dict, "x_frag_count")
        cls._verify_int_ge_2(from_dict, "y_frag_count")
        save_frag_locs_key = "save_frag_locations"

        if save_frag_locs_key in from_dict:
            cls._verify_bool(from_dict, "save_frag_locations")
        else:
            from_dict[save_frag_locs_key] = False
        # end if

        frag_res_overrides_key = "frag_resolution_overrides"
        apply_key = "apply"
        x_res_key = "x_resolution"
        y_res_key = "y_resolution"

        if frag_res_overrides_key in from_dict:
            subdict = from_dict[frag_res_overrides_key]
            cls._verify_bool(subdict, apply_key)
            cls._verify_int_ge_2_even(subdict, x_res_key)
            cls._verify_int_ge_2_even(subdict, y_res_key)
        else:
            from_dict[frag_res_overrides_key] = {}
            subdict = from_dict[frag_res_overrides_key]
            subdict[apply_key] = False
            subdict[x_res_key] = 64
            subdict[y_res_key] = 64
        # end if

        frags_grid_key = "frags_grid"
        save_key = "save"
        pad_key = "padding"
        pad_bright_key = "padding_brightness"

        if frags_grid_key in from_dict:
            subdict = from_dict[frags_grid_key]
            cls._verify_bool(subdict, save_key)
            cls._verify_int_ge_0(subdict, pad_key)
            cls._verify_int_ge_0_le_255(subdict, pad_bright_key)
        else:
            from_dict[frags_grid_key] = {}
            subdict = from_dict[frags_grid_key]
            subdict[save_key] = False
            subdict[pad_key] = 2
            subdict[pad_bright_key] = 16
        # end if

        cust_grad_key = "custom_gradient"
        enabled_key = "enabled"
        coefs_key = "coefficients"
        exps_key = "exponents"

        if cust_grad_key in from_dict:
            subdict = from_dict[cust_grad_key]
            cls._verify_bool(subdict, enabled_key)
            cls._verify_float_list(subdict, coefs_key)
            cls._verify_float_list(subdict, exps_key)
        else:
            from_dict[cust_grad_key] = {}
            subdict = from_dict[cust_grad_key]
            subdict[enabled_key] = False
            subdict[coefs_key] = [float(1)]
            subdict[exps_key] = [float(1)]
        # end if

        result: dict = from_dict
        return result
