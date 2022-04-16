from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
import datetime
from django.urls import reverse
from catalog.models import Book, Author, BookInstance, Genre
from catalog.forms import RenewBookForm
# Create your views here.


@csrf_protect
def index(request):
    """View function for home page of site."""
    #have to adjust this later 
    search_book_title ='Habit'
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_genre = Genre.objects.all().count()
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__iexact='a').count()
    #have to fix this later **make dynamic filter option ..e.g. habit> variable
    num_book_available = Book.objects.filter(title__contains=search_book_title).count()
    # The 'all()' is implied by default.
    num_authors = Author.objects.count()
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genre' : num_genre,
        'num_book_available': num_book_available,
        'book_title_for_search': search_book_title,
        'num_visits':num_visits,
    }
    return render(request, 'index.html', context=context)


class BookListView(LoginRequiredMixin,ListView):
    model = Book
    context_object_name = 'book_list'  
    template_name = 'books/books.html'
    # to add context use this method 
    """def get_context_data(self, **kwargs):
        pass"""
    # to override query
    """def get_queryset(self):
        queryset = super(Book, self).get_queryset()
        queryset = Book.objects.filter(title__icontains='war')[:5] # TODO
        return queryset"""

    
class BookDetailView(LoginRequiredMixin,DetailView):
    model = Book
    context_object_name = 'book'  
    template_name = 'books/book_detail.html'

class AuthorListlView(LoginRequiredMixin,ListView):
    model = Author
    context_object_name = 'authors'
    template_name = 'author/author_list.html'
    

class AuthorDetailView(LoginRequiredMixin,DetailView):
    model = Author
    context_object_name = 'author'
    template_name = 'author/author_detail.html'

    # have to fix it ===============Dynamic It===================================
    def get_context_data(self, **kwargs):
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        context['author_books'] = Book.objects.filter(author__id=1)#dynamic it
        return context




@csrf_protect    
@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk = pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('all-borrowed') )


    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form' : form,
        'book_instance' : book_instance,
    }

    return render(request, 'books/book_renew_librarian.html', context)


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.models import Author

class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

# Added as part of challenge!
from django.contrib.auth.mixins import PermissionRequiredMixin


class LoanedBooksAllListView(PermissionRequiredMixin, ListView):
    """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')