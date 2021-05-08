from rest_framework.response import Response

from game.models import Team

'''
    I used decorators to simply separating access among the different user types. This can be also done using 
    django user permissions. Because of there are only two user types, I choose this simple method to get this done
'''


# When we add this decorator to the api view, That view will be only accessed by admins
def admin():
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            # In here I get user object from session and check for is_admin property. Based on that give the access.
            if request.user.is_admin:
                return view_func(request, *args, **kwargs)
            else:
                return Response(data={"You not allowed to consume this API"}, status=403)

        return wrapper_func

    return decorator


# When we add this decorator to the api view, That view will be only accessed by coaches
def coach():
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            # In here I get user object from session and check for if coach is available for the account.
            # Based on that give the access.
            if request.user.coach:

                check_team(kwargs, args, request, view_func)

            else:
                return Response(data={"You not allowed to consume this API"})

        return wrapper_func

    return decorator


# When we add this decorator to the api view, That view can be accessed by both admins and coaches
def coach_and_admin():
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            if request.user.coach or request.user.is_admin:

                if request.user.is_admin:
                    return view_func(request, *args, **kwargs)

                check_team(kwargs, args, request, view_func)

            else:
                return Response(data={"You not allowed to consume this API"})

        return wrapper_func

    return decorator


def check_team(kwargs, args, request, view_func):
    request_team_id = kwargs["team_id"] if "team_id" in kwargs else False

    # If there is no team_id in url params, Giving access
    if not request_team_id:
        return view_func(request, *args, **kwargs)

    # Some API endpoints require team id as url parameter. In that kind of situation, need to check
    # requesting team is belongs to the coach. Because coach is not allowed to see other teams data.
    # To get that done, checking actual coach team id and team id in request url param
    team_id = Team.objects.get(coach_id=request.user.coach.id)

    if team_id == request_team_id:
        return view_func(request, *args, **kwargs)
    else:
        return Response(data={"You can't access this teams data"})
