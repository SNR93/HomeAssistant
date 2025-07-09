person_id = data.get('person_entity_id', 'person.name_person')
message = data.get('message', 'Тестовое уведомление')
title = data.get('title', 'Уведомление')

# Получение списка device_trackers
devices = hass.states.get(person_id).attributes.get('device_trackers', [])
notify_services = [f"mobile_app_{device.split('.')[-1]}" for device in devices if device.startswith('device_tracker.')]

# Отправка уведомления на каждую службу
for service in notify_services:
    hass.services.call('notify', service, {
        'message': message,
        'title': title,
        'data': {
            'ttl': 0,
            'priority': 'high',
            'push': {
                'sound': {
                    'name': 'default',
                    'critical': 1,
                    'volume': 1.0
                }
            },
            'channel': 'alarm_notifications',  # Для Android
            'notification_category': 'alarm_notifications'  # Для iOS
        }
    })