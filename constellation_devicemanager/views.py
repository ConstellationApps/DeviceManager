from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.contrib.auth.models import User
from django.core import serializers

import netaddr

from .models import Device

def api_v1_device_add(request):
    deviceForm = DeviceForm(request.POST or none)
    if (request.POST and
        deviceForm.is_valid() and (
            request.user == deviceForm.cleaned_data['owner'] or
            request.user.is_staff())):
        # only do things if the form checks out.  The 'owner' value
        # must either match that of the user that is submitting the
        # form, or the form must be submitted by a user that has the
        # staff designation.

        mac = None
        try:
            # We define this inline so that we get nice macs out
            class MACCustomFormat(netaddr.mac_unix):
                word_fmt = '%.2X'
            mac = netaddr.EUI(netdata.deviceForm.cleaned_data['mac'],
                              dialect=MACCustomFormat)
        except netaddr.core.AddrFormatError as e:
            return HttpResponseBadRequest("Bad address format")

        # At this point we have a mac address, and a user that is
        # authorized to add it, lets go ahead and construct the object
        newDevice = Device()
        newDevice.MAC = str(mac)
        if request.user == User.objects.get(username = deviceForm.cleaned_data['owner']):
            
            newDevice.owner = request.user
        else:
            newDevice.owner = User.objects.get(username = deviceForm.cleaned_data['owner'])

        newDevice.save()
        return HttpResponse("Device saved successfully")

def api_v1_device_delete(request, deviceMAC):
    device = get_object_or_404(Device, pk=deviceMAC)
    device.delete()
    return HttpResponse("{0} was deleted".format(deviceMAC))

def api_v1_device_show_user(request, owner):
    devices = Device.objects.filter(owner = User.objects.get(username = owner))
    devicesJSON = serializers.serialize("json", devices)
    return HttpResponse(devicesJSON)

def api_v1_device_show_all(request):
    devices = Device.objects.all()
    devicesJSON = serializers.serialize("json", devices)
    return HttpResponse(devicesJSON)
