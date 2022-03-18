# saleor-plugin-auth0

A simple plugin to use auth0 authentication.
It's only supporting the ["Saleor as a resource server"](https://docs.saleor.io/docs/3.x/developer/available-plugins/openid-connect#saleor-as-a-resource-server) Use Case. This is not considered a production ready plugin.

_Disclaimer:_ This project is not connected/endorsed by saleor's community

## Install

I do not provide a proper pip package as you should not consider this a production ready plugin. You can still add this plugin using pip package manager

```sh
pip install git+https://github.com/onkelfiets/saleor-plugin-auth0.git
```

## Notes

### Access Token

The Plugin expects an `access_token` in the Authentication Header.

```sh
Authentication: Bearer ${access_token}
```

### Custom Claims

You can use Auth0 actions to enhance the JWT with user details including the email which is required to get or create the user in saleor. More details about actions can be found in the [Auth0 docs](https://auth0.com/docs/customize/actions).

```js
exports.onExecutePostLogin = async (event, api) => {
  const namespace = "https://unverpackt-riedberg.de";
  if (event.authorization) {
    api.accessToken.setCustomClaim(`${namespace}/email`, event.user.email);
    api.accessToken.setCustomClaim(
      `${namespace}/firstname`,
      event.user.given_name
    );
    api.accessToken.setCustomClaim(
      `${namespace}/lastname`,
      event.user.family_name
    );
  }
};
```

This is not available in the free plan of Auth0.
If the user details are not included in the token, the plugin fetches this information using the Auth0 API which is time expensive and should be avoided.
