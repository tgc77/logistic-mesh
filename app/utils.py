

def input_is_string(input):
    try:
        # Convert it into integer
        val = int(input)
        return False
    except ValueError:
        try:
            # Convert it into float
            val = float(input)
            return False
        except ValueError:
            return True


def validate_map_inputs(log_map):
    for data in log_map:
        tmp = tuple(data)
        p1, p2, dist = tmp
        if not input_is_string(p1):
            return False
        if not input_is_string(p2):
            return False
        if not dist.isnumeric():
            return False
    return True
