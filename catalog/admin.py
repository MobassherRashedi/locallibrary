from django.contrib import admin
from .models import Author, Genre, Book, BookInstance,Language
# Register your models here.
#admin.site.register(Author)
admin.site.register(Genre)
#admin.site.register(Book)
#admin.site.register(BookInstance)
admin.site.register(Language)


#Inline editing of associated records
class BooksInline(admin.TabularInline):
    model = Book
    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra



class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BooksInline,]

admin.site.register(Author, AuthorAdmin)

#Inline editing of associated records
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra


# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline,]



# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('__str__','status','borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
            }),
            ('Availability', {
                'fields': ('status', 'due_back','borrower')
                }),
                )




