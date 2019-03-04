from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from django_filters.filters import Filter
from django_filters.constants import EMPTY_VALUES


class SearchFilter(Filter):
    # maybe make a filter backend
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


class TrigramSearchFilter(Filter):
    def __init__(self, vectors=None, similarity=0.3, *args, **kwargs):
        self.vectors = vectors
        self.similarity = similarity
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        # TODO: maybe use weights
        if value in EMPTY_VALUES:
            return qs

        qs = qs.annotate(
            similarity=TrigramSimilarity(self.vectors, value),
        ).order_by('-similarity')

        qs = self.get_method(qs)(similarity__gt=self.similarity)
        return qs.distinct() if self.distinct else qs
