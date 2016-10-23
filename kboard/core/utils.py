

def get_page_info(objs, page_size=10):
    # page list
    page_list_count = page_size
    first_page_in_list = (
        int((objs.number - 1) / page_list_count)) * page_list_count + 1
    end_page_in_list = (
        int((objs.number - 1) / page_list_count) + 1) * page_list_count
    page_list = []
    for page_num in range(first_page_in_list, end_page_in_list + 1):
        if page_num > objs.paginator.num_pages:
            break
        page_list.append(page_num)

    pre_page = -1
    next_page = -1

    if objs.number > page_list_count:
        pre_page = first_page_in_list - 1

    if end_page_in_list < objs.paginator.num_pages:
        next_page = end_page_in_list + 1

    pages_info = {
        'pre_page': pre_page,
        'page_list': page_list,
        'current_num': objs.number,
        'next_page': next_page}
    return pages_info
