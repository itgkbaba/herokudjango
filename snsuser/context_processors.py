from utils import get_and_delete_sns_message

def snsuser(request):
    return {
        'snsuser_messages': get_and_delete_sns_message(request),
    }

