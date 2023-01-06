def clear_file(filename):
    with open(filename, 'w'):
        pass


def my_sorted(array: list, key=None, reverse=False):
    list_to_work_with = array[:]
    for i in range(len(list_to_work_with) - 1):
        for j in range(i + 1, len(list_to_work_with)):
            if key is None:
                if list_to_work_with[i] > list_to_work_with[j]:
                    list_to_work_with[i], list_to_work_with[j] = \
                        list_to_work_with[j], list_to_work_with[i]
            else:
                if key(list_to_work_with[i]) > key(list_to_work_with[j]):
                    list_to_work_with[i], list_to_work_with[j] = \
                        list_to_work_with[j], list_to_work_with[i]

    if reverse is True:
        return list_to_work_with[::-1]
    return list_to_work_with
