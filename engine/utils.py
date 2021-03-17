def change_val_and_key(in_dict):
    """Changes value and key.

    Example
        >> in_dict = {'a': 1}
        >> change_val_and_key(in_dict)
            {1: 'a'}
    """
    return {val: key for key, val in in_dict.items()}