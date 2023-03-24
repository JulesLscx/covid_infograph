from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(
        label='Search', max_length=100, min_length=3, required=True)


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    date = forms.DateTimeField(show_hidden_initial=True, auto_now_add=True)

    def upload_path(self, filename):
        return '/covid_infograph/files/excels/%s_%s' % (self.date.strftime("%Y%m%d_%H%M%S"), filename)
    fichier = forms.FileField(upload_to=upload_path,
                              match='*.xlsx$', required=True)
