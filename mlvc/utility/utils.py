def title_to_underscore(string: str):
    return string.lower().replace(' /', '').replace(' ', '_')

def get_element_index_from_list(lst: list, ele: str):
    try:
        idx = lst.index(ele)
        return idx
    except:
        return -1