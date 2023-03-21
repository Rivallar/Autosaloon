def client_login(client, user_type, correct_user, wrong_user):

    """Authenticates correct or wrong cars_and_users for tests"""

    if user_type == 'correct':
        client.force_authenticate(user=correct_user)
    elif user_type == 'wrong':
        client.force_authenticate(user=wrong_user)
    return client


def make_endpoint(base_url, endpoint_type, corr_value, wrong_value=None, wrong_id_value=None):

    """Adds correct/wrong/non-existent ids to the end of url"""

    url = base_url
    if endpoint_type == "correct":
        url += f'{corr_value}/'
    elif endpoint_type == "wrong":
        url += f'{wrong_value}/'
    elif endpoint_type == "wrong_id":
        url += f'{wrong_id_value}/'
    return url
