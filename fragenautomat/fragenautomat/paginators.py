from django.core.paginator import Paginator, Page
from django.utils.functional import cached_property


class SingleItemPage(Page):
    @cached_property
    def item(self):
        return self[0]


class SingleItemPaginator(Paginator):
    def __init__(self, object_list, *args, **kwargs):
        super().__init__(object_list, 1, *args, **kwargs)

    def _get_page(self, *args, **kwargs):
        return SingleItemPage(*args, **kwargs)
