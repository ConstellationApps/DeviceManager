from djano.forms import ModelForm

from .models import Device

class DeviceForm:
    class Meta:
        model = Device
