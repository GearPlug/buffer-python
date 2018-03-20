import requests
from urllib.parse import urlencode
from buffer import exceptions


class Client(object):
    AUTH_ENDPOINT = 'https://bufferapp.com/oauth2/authorize?'
    TOKEN_ENDPOINT = 'https://api.bufferapp.com/1/oauth2/token.json'
    RESOURCE = 'https://api.bufferapp.com'

    def __init__(self, client_id, client_secret, api_version='1'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_version = api_version

        self.base_url = self.RESOURCE + '/' + self.api_version + '/'
        self.token = None

    def get_authorization_url(self, redirect_uri):
        """
        Args:
            redirect_uri: The redirect_uri of your app, where authentication responses can be sent and received by
            your app.  It must exactly match one of the redirect_uris you registered in the app registration portal
        Returns:
            A string.
        """
        params = {
            'client_id': self.client_id,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
        }

        return self.AUTH_ENDPOINT + urlencode(params)

    def exchange_code(self, redirect_uri, code):
        """Exchanges a code for a Token.
        Args:
            redirect_uri: The redirect_uri of your app, where authentication responses can be sent and received by
            your app.  It must exactly match one of the redirect_uris you registered in the app registration portal
            code: The authorization_code that you acquired in the first leg of the flow.
        Returns:
            A dict.
        """
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": redirect_uri,
            "code": code,
            "grant_type": "authorization_code"
        }
        response = requests.post(self.TOKEN_ENDPOINT, data=data, headers=headers)
        response = response.json()
        return response

    def set_token(self, token):
        """Sets the Token for its use in this library.
        Args:
            token: A string with the Token.
        """
        self.token = token

    def get_user_info(self):
        """Return user info
        Returns: request for info
        """
        endpoint = 'user.json'
        return self._get(endpoint)

    def get_user_profiles(self):
        """Returns user profiles registered in Buffer
        Returns: request for info
        """
        endpoint = 'profiles.json'
        return self._get(endpoint)

    def get_specific_profile(self, profile_id):
        """Returns information about specific profile

        Args:
            profile_id: string or list of strings to be embeded
            in endpoint and requested url.

        Returns:
        """
        endpoint = 'profiles/{}.json'.format(str(profile_id))
        return self._get(endpoint)

    def get_posting_schedules(self, profile_id):
        """Returns details of the posting schedules associated with
        a social media profile.
        Args:
            profile_id: string or list of strings to be embeded
            in endpoint and requested url.
        Returns:
        """
        endpoint = 'profiles/{}/schedules.json'.format(str(profile_id))
        return self._get(endpoint)

    def get_specific_post(self, post_id):
        """Returns specific post or update from post_id
        Args:
            post_id: id post to get
        Returns:
        """
        endpoint = 'updates/{}.json'.format(str(post_id))
        return self._get(endpoint)

    def get_pending_posts(self, profile_id):
        """Returns pending posts given a profile_id
        Args:
            profile_id: id of profile to look for pending posts

        Returns:
        """
        endpoint = 'profiles/{}/updates/pending.json'.format(str(profile_id))
        return self._get(endpoint)

    def get_sent_post(self, profile_id):
        """Returns already sent posts
        Args:
            profile_id: profile_id: id of profile to look for
            pending posts
        Returns:
        """
        endpoint = 'profiles/{}/updates/sent.json'.format(str(profile_id))
        return self._get(endpoint)

    def set_queue_posts_new_order(self, profile_id, order):
        """ Reorder the queue of the buffer
        Args:
            profile_id: profile id
            order: update's order in the buffer
        Returns:
        """
        payload = order
        endpoint = 'profiles/{}/updates/reorder.json'.format(str(profile_id))
        return self._post(endpoint, data=payload)

    def set_posting_schedule(self, profile_id, days, times):
        """
        Set the posting schedules for the specified social media profile.
        Args:
            profile_id: string or list of strings to be embeded
            in endpoint and requested url.
            days: days of the week, mon, tue, wed, thu, fri, sat, sun in a
            python list
            times: 24 format hour of the day in a
            python list
        Returns:
        """
        payload = {
            "schedules":
                [{
                    "days": {}.format(days),
                    "times": {}.format(times)
                }]
        }
        endpoint = 'profiles/{}/schedules/update.json'.format(str(profile_id))
        return self._post(endpoint, data=payload)

    def new_post(self, profile_ids, text=None, shorten=None, now=None, top=None,
                 attachment=None, scheduled_at=None, retweet=None):
        """ Create new update or post on the profile or profiles in args.
        Args:
            profile_ids: list of social network profiles. Required
            text: string to be in the post or update. Optional
            shorten: shorten urls in the text. Optional. True or False
            now: if the post or update is going to be sent now. Optional. True or False
            top: if it is True the post/update it's going to be set on the top of the queue or buffer.
            attachment: if True any link in the text will be taken as attachment. Optional. True/False
            scheduled_at: timestamp or ISO 8601 formatted date-time, overrides any top or now parameter. Optional
            retweet: create a 'retweet' update. It will be silently ignored for any other profiles. Optional
        Returns:
        """
        payload = {
            "profile_ids": profile_ids,
            "text": text,
            "shorten": shorten,
            "now": now,
            "top": top,
            "attachment": attachment,
            "scheduled_at": scheduled_at,
            "retweet": retweet,
        }
        endpoint = 'updates/create.json'
        return self._post(endpoint, data=payload)

    def edit_posted(self, text, now, post_id):
        """ Edit already post content
        Args:
            post_id: post id to edit
            text: new text
            now: True or False
        Returns:
        """
        payload = {
            "text": text,
            "now": now
        }
        endpoint = 'updates/{}/update.json'.format(str(post_id))
        return self._post(endpoint, data=payload)

    def _get(self, endpoint, **kwargs):
        return self._request('GET', endpoint, **kwargs)

    def _post(self, endpoint, **kwargs):
        return self._request('POST', endpoint, **kwargs)

    def _put(self, endpoint, **kwargs):
        return self._request('PUT', endpoint, **kwargs)

    def _patch(self, endpoint, **kwargs):
        return self._request('PATCH', endpoint, **kwargs)

    def _delete(self, endpoint, **kwargs):
        return self._request('DELETE', endpoint, **kwargs)

    def _request(self, method, endpoint, headers=None, **kwargs):
        _headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        params = {
            'access_token': '{}'.format(self.token['access_token'])
        }
        if headers:
            _headers.update(headers)
        url = self.base_url+endpoint
        r = requests.request(method, url, headers=_headers, params=params, **kwargs)
        return self._parse(r)

    def _parse(self, response):
        status_code = response.status_code
        if 'application/json' in response.headers['Content-Type']:
            r = response.json()
        else:
            r = response.text
        if status_code in (200, 201, 202):
            return r
        elif status_code == 204:
            return None
        elif status_code == 400:
            raise exceptions.BadRequest(r)
        elif status_code == 401:
            raise exceptions.Unauthorized(r)
        elif status_code == 403:
            raise exceptions.Forbidden(r)
        elif status_code == 404:
            raise exceptions.NotFound(r)
        elif status_code == 405:
            raise exceptions.MethodNotAllowed(r)
        elif status_code == 406:
            raise exceptions.NotAcceptable(r)
        elif status_code == 409:
            raise exceptions.Conflict(r)
        elif status_code == 410:
            raise exceptions.Gone(r)
        elif status_code == 411:
            raise exceptions.LengthRequired(r)
        elif status_code == 412:
            raise exceptions.PreconditionFailed(r)
        elif status_code == 413:
            raise exceptions.RequestEntityTooLarge(r)
        elif status_code == 415:
            raise exceptions.UnsupportedMediaType(r)
        elif status_code == 416:
            raise exceptions.RequestedRangeNotSatisfiable(r)
        elif status_code == 422:
            raise exceptions.UnprocessableEntity(r)
        elif status_code == 429:
            raise exceptions.TooManyRequests(r)
        elif status_code == 500:
            raise exceptions.InternalServerError(r)
        elif status_code == 501:
            raise exceptions.NotImplemented(r)
        elif status_code == 503:
            raise exceptions.ServiceUnavailable(r)
        elif status_code == 504:
            raise exceptions.GatewayTimeout(r)
        elif status_code == 507:
            raise exceptions.InsufficientStorage(r)
        elif status_code == 509:
            raise exceptions.BandwidthLimitExceeded(r)
        else:
            raise exceptions.UnknownError(r)

