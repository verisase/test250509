from django.shortcuts import render
# ↓ reverse関数をインポートする記述を追記
from django.urls import reverse,reverse_lazy
# ↓ UpdateViewをインポートする記述を追記
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
# ↓ Reviewをインポートする記述を追記
from .models import Supplies,Review
# ↓ PermissionDeniedをインポートする記述を追記
from django.core.exceptions import PermissionDenied

from django.contrib.auth.mixins import LoginRequiredMixin
from .models import RATE_CHOICES

from django.db.models import Avg
from django.core.paginator import Paginator
from .consts import ITEM_PER_PAGE


# Create your views here.
class ListSuppliesView(LoginRequiredMixin,ListView):
    model = Supplies
    template_name = 'supplies/list.html'

class DetailSuppliesView(LoginRequiredMixin,DetailView):
    model = Supplies
    template_name = 'supplies/detail.html'
    # ↓ここから追記
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rate_choices'] = RATE_CHOICES
        return context
    # ↑ここまで追記

class CreateSuppliesView(LoginRequiredMixin,CreateView):
    template_name = 'supplies/create.html'
    model = Supplies
    fields = ('title', 'description', 'category', 'thumbnail')
    success_url = reverse_lazy('list-supplies')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class UpdateSuppliesView(LoginRequiredMixin,UpdateView):
    template_name = 'supplies/update.html'
    model = Supplies
    fields = ('title', 'description', 'category', 'thumbnail')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user:
            raise PermissionDenied

        return obj
    
    def get_success_url(self):
        return reverse('detail-supplies', kwargs={'pk': self.object.id})

class DeleteSuppliesView(LoginRequiredMixin,DeleteView):
    template_name = 'supplies/delete_confirm.html'
    model = Supplies
    success_url = reverse_lazy('list-supplies')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user:
            raise PermissionDenied
        
        return obj

class CreateReviewView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ('title', 'description', 'rate', 'supplies')
    template_name = 'supplies/review/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['supplies'] = Supplies.objects.get(pk=self.kwargs['supplies_id'])
        context['rate_choices'] = RATE_CHOICES
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail-supplies', kwargs={'pk': self.object.supplies.id})

class DeleteReviewView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'supplies/review/delete_confirm.html'
    success_url = reverse_lazy('list-supplies')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied
        return obj

def index_view(request):
    object_list = Supplies.objects.order_by('-id')
    ranking_list = Supplies.objects.annotate(avg_rating=Avg('review__rate')).order_by('-avg_rating')

    paginator = Paginator(ranking_list, ITEM_PER_PAGE)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.page(page_number)

    return render(
        request,
        'supplies/index.html',
        {'object_list': object_list, 'ranking_list': ranking_list, 'page_obj': page_obj},
    )
