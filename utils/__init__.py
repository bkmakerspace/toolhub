import collections


def deep_update(orig_dict, new_dict):
    for key, val in new_dict.items():
        if isinstance(val, collections.Mapping):
            tmp = deep_update(orig_dict.get(key, {}), val)
            orig_dict[key] = tmp
        elif isinstance(val, list):
            orig_dict[key] = orig_dict.get(key, []) + val
        else:
            orig_dict[key] = new_dict[key]
    return orig_dict
