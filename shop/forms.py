from django import forms

class AddToCartForm(forms.Form):
    product_id = forms.IntegerField()
    options = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    quantity = forms.IntegerField(min_value=1, initial=1)

    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', None)
        super(AddToCartForm, self).__init__(*args, **kwargs)
        if product:
            self.fields['options'].choices = [
                (option.id, option.name) for option in product.options.all()
            ]
