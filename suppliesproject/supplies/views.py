import pkgutil
from random import choice
from django.shortcuts import render, get_object_or_404
# ↓ reverse関数をインポートする記述を追記
from django.urls import reverse,reverse_lazy
# ↓ UpdateViewをインポートする記述を追記
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
# ↓ Reviewをインポートする記述を追記
from .models import Supplies,Review, Lendingsupplies
# ↓ PermissionDeniedをインポートする記述を追記
from django.core.exceptions import PermissionDenied

from django.contrib.auth.mixins import LoginRequiredMixin
from .models import RATE_CHOICES

from django.db.models import Avg,Q
from django.core.paginator import Paginator
from .consts import ITEM_PER_PAGE

from django import forms


# Create your views here.
class ListSuppliesView(LoginRequiredMixin,ListView):
    model = Lendingsupplies #Supplies
    template_name = 'supplies/list.html'

    #　ここから検索機能について記載
    def get_queryset(self):
        query = self.request.GET.get('query')

        #　対象が"query"を含んでいるものを表示する
        if query:
            supplies_list = Supplies.objects.filter(
                Q(title__icontains=query)|Q(title__icontains=normalize_kana(query))|Q(title__icontains=normalize_hira(query))|Q(tag__icontains=query)|Q(tag__icontains=normalize_kana(query))|Q(tag__icontains=normalize_hira(query)) # type: ignore
            )
        else:
            supplies_list = Supplies.objects.all()
        return supplies_list

    #　ここまで

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
    fields = ('title', 'description', 'category', 'thumbnail', 'tag', 'allsupplies')
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

#検索をかけた際に名前またはタグに含まれているもののみを表示
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

class Rentallist(LoginRequiredMixin,ListView):
    model = Lendingsupplies
    template_name = 'supplies/rental_list.html'

class Lendlist(LoginRequiredMixin,ListView):
    model = Lendingsupplies
    template_name = 'supplies/lend_list.html'

#　カタカナをひらがなへ変換
def normalize_kana(text):
        return ''.join([chr(ord(ch)- 0x60)if 'ア' <= ch <= 'ン' else ch for ch in text])

#　ひらがなをカタカナへ変換
def normalize_hira(text):
        return ''.join([chr(ord(ch)+ 0x60)if 'あ' <= ch <= 'ん' else ch for ch in text])

class ThrowRentalView(LoginRequiredMixin,UpdateView):
    template_name = 'supplies/throw.html'
    model = Lendingsupplies
    fields = ('destruction',)
    success_url = reverse_lazy('rental-list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        pk_value = int(self.kwargs['pk'])
        lend = Lendingsupplies.objects.get(id = pk_value).lend
        choices = [(i, str(i)) for i in range(1, lend + 1)]
        form.fields['destruction'].choices = choices
        return form

    def form_valid(self, form):
    # まずLendingSupplies本体を保存
        response = super().form_valid(form)

        # 保存された貸出情報を取得
        throw = self.object      # =保存後のLendingSuppliesインスタンス
        destruction = throw.destruction    # 新しい破棄数
        print(destruction)
        lend = throw.lend
        lend -= destruction
        throw.lend = lend

        throw.save()

        # 対応するStockモデルを更新
        pk = self.kwargs['pk']
        supplies_obj = get_object_or_404(Supplies, id=pk)
        supplies_obj.allsupplies -= destruction
        supplies_obj.lend -= destruction

        supplies_obj.save()

        return response

      