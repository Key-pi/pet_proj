from boards.models import Reader


def create_profile(strategy, details, response, user, *args, **kwargs):
    if Reader.objects.filter(user=user).exists():
        pass
    else:
        new_profile = Reader(user=user)
        new_profile.save()
    return kwargs
