

def get_pages_nav_info(page, nav_chunk_size=10):
    """ this function return navigation bar info of paginated objects """

    first_page_in_list = (
        int((page.number - 1) / nav_chunk_size)) * nav_chunk_size + 1
    end_page_in_list = (
        int((page.number - 1) / nav_chunk_size) + 1) * nav_chunk_size
    page_list = []
    for page_num in range(first_page_in_list, end_page_in_list + 1):
        if page_num > page.paginator.num_pages:
            break
        page_list.append(page_num)

    # if not exist nav_page, -1
    pre_nav_page = -1
    next_nav_page = -1

    if page.number > nav_chunk_size:
        pre_nav_page = first_page_in_list - 1

    if end_page_in_list < page.paginator.num_pages:
        next_nav_page = end_page_in_list + 1

    pages_nav_info = {
        'pre_nav_page': pre_nav_page,
        'page_list': page_list,
        'current_page_num': page.number,
        'next_nav_page': next_nav_page}
    return pages_nav_info


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', None)
    x_real_ip = request.META.get('HTTP_X_REAL_IP', None)
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[-1].strip()
    elif x_real_ip:
        ip_address = x_real_ip
    else:
        ip_address = request.META.get('REMOTE_ADDR', None)
    return ip_address


def hide_ip(ip_str):
    ip_arr = str(ip_str).split('.')
    ip_arr[2] = 'xxx'
    return '.'.join(ip_arr)
