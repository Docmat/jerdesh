from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.views.generic import View, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm
from .models import Category, City, Ad


class IndexPage(View):
    def get(self, request, *args, **kwargs):
        ads = Ad.objects.order_by('id')[:5]
        categories = Category.objects.all()
        cities = City.objects.all()
        context = {
            'ads': ads,
            'categories': categories,
            'cities': cities,
        }
        return render(request, 'jerdesh/index.html', context)


class AdList(View):
    def get(self, request):
        search_title = request.GET.get('search', '')
        search_city = request.GET.get('location', '')
        search_category = request.GET.get('category', '')

        if search_title or search_city or search_category:
            ads = Ad.objects.filter(Q(ad_title__icontains=search_title) | Q(city__city_text=search_city) | Q(
                category__category_text=search_category))
        else:
            ads = Ad.objects.all()

        cities = City.objects.all()
        categories = Category.objects.all()
        paginator = Paginator(ads, 10)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        is_paginated = page.has_other_pages()

        if page.has_previous():
            prev_url = f'?page={page.previous_page_number()}'
        else:
            prev_url = ''

        if page.has_next():
            next_url = f'?page={page.next_page_number()}'
        else:
            next_url = ''

        context = {
            'cities': cities,
            'categories': categories,
            'ads': page,
            'is_paginated': is_paginated,
            'next_url': next_url,
            'prev_url': prev_url
        }
        return render(request, 'jerdesh/ads_list.html', context)


# CRUD
class AdCreate(CreateView):
    model = Ad
    template_name = 'jerdesh/ad_create.html'
    fields = ['category', 'city', 'ad_title', 'ad_text', 'img']
    success_url = reverse_lazy('jerdesh:ads_list_url')

    def get_form(self, form_class=None):
        form = super(AdCreate, self).get_form(form_class)
        form.fields['ad_title'].widget.attrs['placeholder'] = 'Название объявления'
        form.fields['ad_text'].widget.attrs['placeholder'] = 'Описание объявления'
        form.fields['img'].widget.attrs['class'] = 'custom-file-input'
        return form

    def form_valid(self, form):
        new_ad = form.save()
        new_ad.slug = f'{new_ad.ad_title}-{new_ad.id}'
        new_ad.author = self.request.user
        new_ad.save()
        return super(AdCreate, self).form_valid(form)


class AdDetails(DetailView):
    model = Ad
    slug_field = 'slug'
    template_name = 'jerdesh/ad_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class AddComment(View):
    def post(self, request, pk):
        form = CommentForm(request.POST)
        post = Ad.objects.get(pk=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.post = post
            form.save()
        return redirect(post.get_absolute_url())


class AdUpdate(UpdateView, LoginRequiredMixin):
    model = Ad
    template_name = 'jerdesh/ad_update.html'
    fields = ('ad_title', 'ad_text', 'img', 'category')
    login_url = 'login'

    def get_context_data(self, *args, **kwargs):
        some_list = ["some", "list"]
        context = super().get_context_data()
        context['some_lists'] = some_list
        return context

# class AdDelete(DeleteView):
# 	model = Ad
# 	template_name = 'jerdesh/ad_delete.html'
# 	success_url = reverse_lazy('')
