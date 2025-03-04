def user_profile_context(request):
    """
    Context processor to add 'user_profile' from the session to the template context.
    """
    return {'user_profile': request.session.get('user_profile', None)}
