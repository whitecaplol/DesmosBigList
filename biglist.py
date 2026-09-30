def format_desmos_list(var_name: str, plain_list: list[Any] | tuple[list[Any], list[Any], list[Any]], max_fragments: int | None = None, max_list_size: int = 10000) -> str:
    output = ''
    true_length = len(plain_list) if type(plain_list) == list else len(plain_list[0])

    est_fragments, remainder = divmod(true_length, max_list_size)
    fragment_count = est_fragments + int(remainder > 0)
    max_fragments = min(fragment_count, max_fragments) if max_fragments is not None else fragment_count
    est_lines, remainder = divmod(fragment_count, max_fragments)
    lines = est_lines + int(remainder > 0)

    for j in range(lines):
        output += rf"{var_name[0]}_{{{var_name[1:]}{f'fragment{j}' if lines > 1 else ''}}}\left(l_{{o}},h_{{i}}\right)="
        has_join_prefix = False
        for i in range(max_fragments):
            offset = max_list_size * (j * max_fragments + i)
            lo = offset + 1
            hi = min(offset + max_list_size, true_length)
            fragment_length = hi - lo + 1
            if i == 0 and (max_fragments > 1 and fragment_length == max_list_size and hi < true_length):
                has_join_prefix = True
                output += r'\operatorname{join}\left('
            if fragment_length <= 0:
                output = output.removesuffix(',')
                break

            if type(plain_list) == list:
                l_str = rf'\left[{','.join(map(str, plain_list[lo-1:hi]))}\right]'
            elif type(plain_list) == tuple:
                l_str = fr'\left(\left[{','.join(map(str, plain_list[0][lo-1:hi]))}\right],\left[{','.join(map(str, plain_list[1][lo-1:hi]))}\right],\left[{','.join(map(str, plain_list[2][lo-1:hi]))}\right]\right)'
            else:
                raise TypeError("plain_list is not of expected type")

            output += rf'\left\{{\left\{{{lo}\le l_{{o}}\le{hi},0\right\}}+\left\{{{lo}\le h_{{i}}\le{hi},0\right\}}+\left\{{l_{{o}}<{lo},0\right\}}\left\{{h_{{i}}>{hi},0\right\}}\ge1:{l_str}\left[\max\left(1,\min\left({fragment_length},l_{{o}}-{offset}\right)\right)...\min\left({fragment_length},\max\left(1,h_{{i}}-{offset}\right)\right)\right],\left[\right]\right\}}{',' if i + 1 < max_fragments else ''}'
        output += '\\right)\n' if has_join_prefix else '\n'

    if lines > 1:
        output += rf'{var_name[0]}_{{{var_name[1:]}}}\left(l_{{o}},h_{{i}}\right)=\operatorname{{join}}\left({','.join([rf'{var_name[0]}_{{{var_name[1:]}{f'fragment{i}'}}}\left(l_{{o}},h_{{i}}\right)' for i in range(lines)])}\right)''\n'

    return output
