import requests
from django.http import JsonResponse
from django.conf import settings

def altcha_challenge(request):
    if request.method == 'GET':
        headers = {
            'Referer': settings.REFERER_HEADER,
        }
        response = requests.get(f'{settings.CAPTCHA_URL}?apiKey={settings.CAPTCHA_KEY}', headers=headers)
        if response.status_code == 200:
            challenge_data = response.json()
            return JsonResponse(challenge_data)
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to retrieve challenge'}, status=response.status_code)
