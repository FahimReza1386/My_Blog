from django import forms
from .models import Post, Category
from comment.models import Comments


class CreatePostForm(forms.ModelForm):
    image = forms.ImageField(label="تصویر خود را انتخاب نمایید ...", required=False, help_text='', widget=forms.FileInput(attrs={'placeholder': "تصویر وبلاگ خود را بنویسید .."}))
    title = forms.CharField(label="" , help_text='', widget=forms.TextInput(attrs={'placeholder':"نام وبلاگ خود را بنویسید .."}))
    content = forms.CharField(label="" , max_length=200, help_text='', widget=forms.TextInput(attrs={'placeholder':"متن وبلاگ خود را بنویسید .."}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label="" , help_text='', widget=forms.Select(attrs={'placeholder':"دسته بندی وبلاگ خود را انتخاب کنید .."}))
    published_date = forms.DateTimeField(label="" , help_text='', widget=forms.DateInput(attrs={'placeholder':"زمان انتشار وبلاگ خود را بنویسید ..",'type':'date'}))

    class Meta:
        model=Post
        fields=["image","title","content","category","published_date"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'margin-top: 2rem;'

        self.fields['category'].empty_label = 'لطفاً دسته‌بندی را انتخاب کنید ...'
        self.fields['image'].empty_label = 'لطفاً دسته‌بندی را انتخاب کنید ...'



class EditView(forms.ModelForm):
    image = forms.ImageField(label="تصویر خود را انتخاب نمایید ...", required=False, help_text='', widget=forms.FileInput(attrs={'placeholder': "تصویر وبلاگ خود را بنویسید .."}))
    title = forms.CharField(label="" , help_text='', widget=forms.TextInput(attrs={'placeholder':"نام وبلاگ خود را بنویسید .."}))
    content = forms.CharField(label="" , max_length=200, help_text='', widget=forms.TextInput(attrs={'placeholder':"متن وبلاگ خود را بنویسید .."}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label="" , help_text='', widget=forms.Select(attrs={'placeholder':"دسته بندی وبلاگ خود را انتخاب کنید .."}))
    published_date = forms.DateTimeField(label="" , help_text='', widget=forms.DateInput(attrs={'placeholder':"زمان انتشار وبلاگ خود را بنویسید ..",'type':'date'}))

    class Meta:
        model=Post
        fields=["image","title","content","category","published_date"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'margin-top: 2rem;text-align: center;'

        self.fields['category'].empty_label = 'لطفاً دسته‌بندی را انتخاب کنید ...'
        self.fields['image'].empty_label = 'لطفاً دسته‌بندی را انتخاب کنید ...'

