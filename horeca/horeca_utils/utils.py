from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 500


def enum_choices_factory(enum_cls):
    return tuple([(member.value, member.value) for name, member in enum_cls.__members__.items()])
