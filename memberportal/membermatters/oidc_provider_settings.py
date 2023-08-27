def userinfo(claims, user):
    # Populate claims dict.
    claims["name"] = "{0} {1}".format(user.profile.first_name, user.profile.last_name)
    claims["given_name"] = user.profile.first_name or "NO_FIRSTNAME"
    claims["family_name"] = user.profile.last_name or "NO_LASTNAME"
    claims["nickname"] = user.profile.screen_name or "NO_SCREENNAME"
    claims["email"] = user.email
    claims["phone_number"] = user.profile.phone or "NO_PHONENUMBER"

    return claims
