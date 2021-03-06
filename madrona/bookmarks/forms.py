from madrona.features.forms import FeatureForm
from madrona.bookmarks.models import Bookmark
from django import forms

class BookmarkForm(FeatureForm):
    name = forms.CharField(label='Bookmark Name')
    latitude = forms.FloatField(widget=forms.HiddenInput())
    longitude = forms.FloatField(widget=forms.HiddenInput())
    altitude = forms.FloatField(widget=forms.HiddenInput())
    heading = forms.FloatField(widget=forms.HiddenInput())
    tilt = forms.FloatField(widget=forms.HiddenInput())
    roll = forms.FloatField(widget=forms.HiddenInput())
    altitudeMode = forms.FloatField(widget=forms.HiddenInput())
    publicstate = forms.CharField(widget=forms.HiddenInput())
    ip = forms.CharField(widget=forms.HiddenInput(), initial="0.0.0.0", required=False)

    class Meta(FeatureForm.Meta):
        model = Bookmark
