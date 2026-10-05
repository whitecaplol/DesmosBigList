from collections.abc import Sequence
from math import ceil

def get_sanitized_string(string: str) -> str:
    return f'{string[0]}_{{{string[1:]}}}'

def factor32(n: int) -> tuple[int, int]:
    factor1 = 0
    factor2 = 0
    min_diff = float('inf')
    for i in range(1, 33, 1):
        diff = min(32, ceil(n / i)) * i - n
        if diff >= min_diff or diff < 0:
            continue
        min_diff = diff
        factor1 = i
        factor2 = ceil(n / i)
    return factor1, factor2

def format_desmos_list(var_name: str, plain_list: Sequence, max_mega_fragments: int | None = None, max_fragments: int | None = None, max_list_size: int = 10000, add_new_line: bool=True) -> str:
    if (max_mega_fragments is not None and max_mega_fragments < 1): max_mega_fragments = None
    if ((max_fragments is not None and max_fragments < 1) or max_fragments is None): max_fragments = 1024
    elif (max_fragments is not None):
        max_fragments = min(1024, max_fragments)
    output = ''

    current_matrix_position = 0
    current_mega_fragments = 0
    current_global_fragments = 0
    rows, columns = factor32(min(max_fragments, ceil(len(plain_list) / max_list_size)))

    def getTrailingCharacter():
        if (current_matrix_position >= rows * columns): return ''
        return '&' if current_matrix_position % columns > 0 else '\\\\'

    def close_matrix():
        nonlocal output, current_matrix_position
        while (0 < current_matrix_position < rows * columns):
            output += getTrailingCharacter()
            current_matrix_position += 1
        if (output[-14:] != r'\right)\right]'):
            output += r'\end{bmatrix}'
            output += fr'\left[1+\operatorname{{mod}}\left(\operatorname{{floor}}\left(\frac{{\operatorname{{ceil}}\left(\frac{{k}}{{{max_list_size}}}\right)-1}}{{{columns}}}\right),{rows}\right);1+\operatorname{{mod}}\left(\operatorname{{ceil}}\left(\frac{{k}}{{{max_list_size}}}\right)-1,{columns}\right)\right]\left[1+\operatorname{{mod}}\left(k-1,{max_list_size}\right)\right]'

    for i in range(0, len(plain_list), max_list_size):
        if (current_matrix_position == 0 == current_mega_fragments):
            current_global_fragments += 1
        if (current_mega_fragments == 0):
            current_mega_fragments += 1
            output += rf'{get_sanitized_string(f'{var_name}{current_global_fragments}')}\left(k\right)=\left\{{'
        if (current_matrix_position == 0):
            if (current_mega_fragments > 1):
                output += ','
            total_num_fragments = current_mega_fragments if max_mega_fragments is None else (current_global_fragments - 1) * max_mega_fragments + current_mega_fragments
            output += rf'{min(1 + (total_num_fragments - 1) * rows * columns * max_list_size, len(plain_list))}\le k \le{min((total_num_fragments) * rows * columns * max_list_size, len(plain_list))}:\begin{{bmatrix}}'
        output += rf'\left[{','.join(map(str, plain_list[i:i+max_list_size]))}\right]'
        current_matrix_position += 1
        if (i+max_list_size >= len(plain_list)):
            output += r'.\operatorname{join}\left(\operatorname{repeat}\left(0,k\right)\right)'.replace("k", str(i+max_list_size - len(plain_list)))
            break
        if (current_matrix_position < rows * columns and (max_fragments is None or current_matrix_position < max_fragments)):
            output += getTrailingCharacter()
            continue
        close_matrix()
        current_matrix_position = 0
        current_mega_fragments += 1
        if (max_mega_fragments is None or current_mega_fragments <= max_mega_fragments): continue
        current_mega_fragments = 0
        output += r'\right\}''\n'

    close_matrix()
    if output[-1] != '\n':
        output += r'\right\}''\n'

    output += f'{get_sanitized_string(var_name)}\\left(l\\right)='

    if max_mega_fragments is not None and current_global_fragments > 1:
        output += '\\left\\{'
        for i in range(current_global_fragments):
            if i > 0:
                output += ','
            output += f'{min(1 + i * max_list_size * (max_fragments if max_fragments is not None else rows * columns) * max_mega_fragments, len(plain_list))} \\le k \\le {min((1 + i) * max_list_size * (max_fragments if max_fragments is not None else rows * columns) * max_mega_fragments, len(plain_list))}:{get_sanitized_string(f'{var_name}{i+1}')}\\left(k\\right)'
        output += '\\right\\}'
    else:
        output += f'{get_sanitized_string(f'{var_name}1')}\\left(k\\right)'
    output += r'\operatorname{for}k=l'

    if add_new_line:
        output += '\n'

    return output
