from django import forms


class SeatReservationForm(forms.Form):
    selected_seats = forms.CharField(widget=forms.HiddenInput())
