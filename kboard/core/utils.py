

def get_pages_nav_info(objs, nav_chunk_size=10):
    """ this function return navigation bar info of paginated objects """
    # page list
    first_page_in_list = (
        int((objs.number - 1) / nav_chunk_size)) * nav_chunk_size + 1
    end_page_in_list = (
        int((objs.number - 1) / nav_chunk_size) + 1) * nav_chunk_size
    page_list = []
    for page_num in range(first_page_in_list, end_page_in_list + 1):
        if page_num > objs.paginator.num_pages:
            break
        page_list.append(page_num)

    pre_page = -1
    next_page = -1

    if objs.number > nav_chunk_size:
        pre_page = first_page_in_list - 1

    if end_page_in_list < objs.paginator.num_pages:
        next_page = end_page_in_list + 1

    pages_info = {
        'pre_page': pre_page,
        'page_list': page_list,
        'current_num': objs.number,
        'next_page': next_page}
    return pages_info
