# saleor-plugin-auth0

A simple plugin to use auth0 authentication.
It's only supporting the ["Saleor as a resource server"](https://docs.saleor.io/docs/3.x/developer/available-plugins/openid-connect#saleor-as-a-resource-server) Use Case.

The Plugin expects an `access_token` in the Authentication Header.

```
Authentication: Bearer ${access_token}
```

You can use Auth0 actions to enhance the JWT with user details including the email which is required to get or create the user in saleor.

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

This is not available in the free plan. In that case the plugin fetches this information using the Auth0 API which is time expensive and should be avoided.
