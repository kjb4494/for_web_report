
def combine_list(*args: list, sort=True, duplicates=False) -> list:
    combined_list = []
    for arg in args:
        combined_list.extend(arg)
    if not duplicates:
        combined_list = list(set(combined_list))
    if sort:
        combined_list.sort()
    return combined_list
