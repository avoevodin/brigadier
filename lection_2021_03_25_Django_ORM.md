# Basic tools
```python
from django.db import connection as conn
conn.queries
>[]
print(conn.queries[-1]['sql'])
```

```python
Book.objects.all().filter(publisher_id__in=[2,3])
Book.objects.all().filter(name__startwith='война')
Book.objects.all().filter(name__startwith='война')
Book.objects.values()
Book.objects.values('id', 'name')
Book.objects.values('id', 'name', 'publisher__name')
Book.objects.values_list('id', 'name', 'publisher__name')
# filter and values may be in any order
Book.objects.values_list('id', 'name', 'publisher__name').filter(rating__gte=9)
Store.objects.first().books.all()
Store.objects.first().books.count()
```
* Agregate
```python
from django.db.models import Avg, Sum, Max, Min, Count

Book.objects.aggregate(Avg('price'))
Book.objects.aggregate(Avg('price'), Min('price'), Max('price'))
# Good practice:
Book.objects.aggregate(avg_price=Avg('price'), min_price=Min('price'), max_price=Max('price'))
# Aggregate is the last member of a chain, because aggregate returns dict instead of queryset
Book.objects.filter(rating__gte=9).aggregate(avg_price=Avg('price'), min_price=Min('price'), max_price=Max('price'))
Book.objects.aggregate(price_diff=Max('price') - Avg('price'))
```
* Annotate
```python
pubs = Publisher.objects.annotate(num_books=Count('book'))
pubs = Publisher.objects.annotate(num_books=Count('book'), avg_rating=Avg('book__rating'))
book = Book.objects.annotate(num_authors=Count('authors'), num_stores=Count('store'))
book.values('id', 'name', 'num_authors', 'num_stores') # multiple error
book = Book.objects.annotate(num_authors=Count('authors', distinct=True), num_stores=Count('store', distinct=True))
```

-----

* Join 
```python
stores_ex = Store.objects.annotate(
    min_price=Min('books__price'),
    max_price=Max('books__price')
)
stores_ex.values()
```
---- 
* F-expressions
```python
from django.db.models import F
book_diff = stores_ex.annotate(book_diff=F('max_price')-F('min_price'))
book_diff.values()
```
-----
* Type conversion
```python
stores_ex1 = store.objects.annotate(
    books_count=Count('books')
    books_sum_pr=Sum('books__price')
)
stores_ex1.annotate(
    books_avg_pr = F('books_sum_pr') / F('books_count')
)
# >>> Error with types
from django.db.models import DecimalField

stores_ex1 = store.objects.annotate(
    books_count=Count('books', output_field=DecimalField())
    books_sum_pr=Sum('books__price', output_field=DecimalField())
)
stores_ex1.annotate(
    books_avg_pr=F('books_sum_pr') / F('books_count')
```
-----
* Case
```python
from django.db.models import Case, When, F
stores_ex1 = store.objects.annotate(
    books_count=Count('books', output_field=DecimalField())
    books_sum_pr=Sum('books__price', output_field=DecimalField())
)
stores_ex1.annotate(
    books_avg_pr=Case(
        When(books_count=0, then=0.0),
        default=F('books_sum_pr') / F('books_count')
    )
```
----
* Filter and order annotations
```python
from django.db.models import Case, When, F
stores_ex1 = store.objects.annotate(
    books_count=Count('books', output_field=DecimalField())
    books_sum_pr=Sum('books__price', output_field=DecimalField())
)
stores_ex1.annotate(
    books_avg_pr=Case(
        When(books_count=0, then=0.0),
        default=F('books_sum_pr') / F('books_count')
    )).filter(books_avg_pr=0.0).values()
```
* Q-expressions and type casts error
```python
from django.db.models import Count, Q, F, FloatField
bestsellers = Store.objects.annotate(
    books_count = Count('books', output_field=FloatField()),
    books_high_rating_count = Count('books', filter=Q(books__rating__gte=10), output_field=FloatField())
)
rate = bestsellers.annotate(
    bestsellers=Case(
        When(books_count=0, then=0.0),
        default=F(books_high_rating_count)/F(books_count)
    )
)
rate.values()
# error because of types
```
* Q-expressions and type casts without error
```python
from django.db.models import Count, Q, F, Cast, FloatField
bestsellers = Store.objects.annotate(
    books_count = Cast(Count('books'), FloatField()),
    books_high_rating_count = Cast(Count('books', filter=Q(books__rating__gte=10)), FloatField())
)
rate = bestsellers.annotate(
    bestsellers=Case(
        When(books_count=0, then=0.0),
        default=F(books_high_rating_count)/F(books_count)
    )
)
rate.values()
# error because of types
```

---------------
* Hooks

```python
class ProjectListView(generic.ListView):
    ...
    
    def get_template_names(self):
        return 'project_list.html'
    
    
    def get_queryset(self):
        qs = Project.objects.all()
        if self.request.GET.get('closed') == 'True':
            qs = qs.filter(closed=True)
        if self.request.GET.get('q'):
            qs = qs.filter(project_name__contains=self.request.GET.get('q'))
        if self.request.GET.get('ordering'):
            qs = qs.order_by(self.request.GET.get('ordering'))
        else:
            qs = qs.order_by('deadline')
        return qs
```

```python
class ProjectDetailView(generic.DetailView):
    model = Project
    template_name = 'project_detail.html'

    def get_context_data(self, **kwargs):
        project = self.get_object()
        tasks = Task.objects.filter(project=project)
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['task_list'] = tasks
        return context
```
```python
class ProjectCreateView(generic.CreateView):
    ...
    
    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        else:
            return reverse('employees:list')
```