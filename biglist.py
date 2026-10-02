def format_desmos_list(var_name: str, plain_list: Sequence, max_mega_fragments: int | None = None, max_fragments: int | None = None, max_list_size: int = 10000) -> str:
    output = ''

    current_matrix_position = 0
    current_mega_fragments = 0
    current_global_fragments = 0

    def getTrailingCharacter():
        if (current_matrix_position >= 1024): return ''
        return '&' if current_matrix_position % 32 > 0 else '\\\\'

    def close_matrix():
        nonlocal output, current_matrix_position
        while (0 < current_matrix_position < 1024):
            output += getTrailingCharacter()
            current_matrix_position += 1
        if (output[-14:] != r'\right)\right]'):
            output += r'\end{bmatrix}'
            output += fr'\left[1+\operatorname{{mod}}\left(\operatorname{{floor}}\left(\frac{{\operatorname{{ceil}}\left(\frac{{k}}{{{max_list_size}}}\right)-1}}{{32}}\right),32\right);1+\operatorname{{mod}}\left(\operatorname{{ceil}}\left(\frac{{k}}{{{max_list_size}}}\right)-1,32\right)\right]\left[1+\operatorname{{mod}}\left(k-1,{max_list_size}\right)\right]'

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
            output += rf'{min(1 + (total_num_fragments - 1) * 1024 * max_list_size, len(plain_list))}\le k \le{min((total_num_fragments) * 1024 * max_list_size, len(plain_list))}:\begin{{bmatrix}}'
        current_matrix_position += 1
        output += rf'\left[{','.join(map(str, plain_list[i:i+max_list_size]))}\right]{getTrailingCharacter()}'
        if (i+max_list_size >= len(plain_list)):
            current_matrix_position += 1
            break
        if (current_matrix_position < 1024 and (max_fragments is None or current_matrix_position < max_fragments)): continue
        close_matrix()
        current_matrix_position = 0
        current_mega_fragments += 1
        if (max_mega_fragments is None or current_mega_fragments < max_mega_fragments): continue
        output += r'\right\}''\n'

    close_matrix()
    if output[-1] != '\n':
        output += r'\right\}''\n'

    output += f'{get_sanitized_string(var_name)}\\left(l\\right)='

    if max_mega_fragments is not None and current_global_fragments > 1:
        output += '\\left{'
        for i in range(current_global_fragments):
            if i > 0:
                output += ','
            output += f'{min(1 + i * 10240000 * max_mega_fragments, len(plain_list))} \\le k \\le {min((1 + i) * 10240000 * max_mega_fragments, len(plain_list))}:{get_sanitized_string(f'{var_name}{i+1}')}\\left(k\\right)'
        output += '\\right}'
    else:
        output += f'{get_sanitized_string(f'{var_name}1')}\\left(k\\right)'
    output += r'\operatorname{for}k=l'

    return output
