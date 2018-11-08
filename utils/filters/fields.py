from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django_filters.filters import Filter
from django_filters.constants import EMPTY_VALUES


class SearchFilter(Filter):
    # maybe make it not a django-filter
    def __init__(self, vectors=None, *args, **kwargs):
        self.vectors = vectors
        super().__init__(*args, **kwargs)

    def get_query_config(self):
        return None

    def filter(self, qs, value):
        # TODO: maybe use weights
        if value in EMPTY_VALUES:
            return qs
        vector = SearchVector(config=self.get_query_config(), *self.vectors)
        query = SearchQuery(value, config=self.get_query_config())
        qs = qs.annotate(
            search=vector,
            rank=SearchRank(vector, query)
        ).order_by('-rank')
        qs = self.get_method(qs)(search=query)
        return qs.distinct() if self.distinct else qs
