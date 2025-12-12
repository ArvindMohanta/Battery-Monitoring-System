from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Battery, BatteryAlert
from .serializers import BatterySerializer, BatteryAlertSerializer


def broadcast_to_dashboard(payload: dict):
    layer = get_channel_layer()
    async_to_sync(layer.group_send)('dashboard', {
        'type': 'dashboard.update',
        'data': payload,
    })


@receiver(post_save, sender=Battery)
def battery_saved(sender, instance: Battery, created, **kwargs):
    data = BatterySerializer(instance).data
    payload = {'type': 'battery_update', 'battery': data, 'created': created}
    broadcast_to_dashboard(payload)


@receiver(post_save, sender=BatteryAlert)
def alert_saved(sender, instance: BatteryAlert, created, **kwargs):
    data = BatteryAlertSerializer(instance).data
    payload = {'type': 'alert_update', 'alert': data, 'created': created}
    broadcast_to_dashboard(payload)
