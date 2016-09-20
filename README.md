# Blog API media

Today we will expand our Blog API to support some of the advanced `django-rest-framework` features, like `versioning`, `throttling`, etc.

Aside from small changes, we will mostly keep the same data model as before. Previous endpoints, like `/users`, `/entries`, etc will also remain the same.

## API versioning

It's a very good practice to keep your APIs versioned. If at any point in the future you need to do significant changes to your API, changing the original code or endpoints would not allow backward compatibility for all the current clients of your API. Instead, we can create a new version and keep everything safe.

The API version must be specified in the URL like this: `/api/v1/`. You must make sure to configure `rest_framework` properly, so the version is available for every request under `request.version`.

In order to test that the API versioning is actually working, we created a pretty simple `StatusView` that only returns `{"version": "v1"}`.

![version](http://i.imgur.com/D7wJ5Cq.png)

## Multiple formatting

In our previous API, we only supported `JSON` response format. There was no way of specifying a different data format. Today we will need to support both `JSON` and `XML`.

By default, the API should always return `JSON` responses. But, if we send a custom `?format=xml` argument, the same output must be returned using `XML` formatting. The `?format=json` argument should work as well, in case we want to explicitly select `JSON` as output.

![xml](http://i.imgur.com/nVeUXO6.png)

## Throttling

For security reasons, it's always recommended to avoid a single user being able to perform huge amount of requests in a considerable small amount of time. While working with APIs, that's well known as `throttling`. In `django-rest-framework`, API `throttling` is available out of the box.

You will need to configure a rule in your API, to limit a maximal of `50 requests per minute` for the same user.

![throttling](http://i.imgur.com/iK7QXRT.png)

## Entry images

Finally, we will do a quick update to our `Entry` model adding a new `image` field. We should be able to POST an attached image while creating a new blog `Entry`. We already provide the Django `MEDIA_ROOT` and `MEDIA_URL` settings so you don't need to deal with them. Make sure POSTed images are uploaded under those directories.

As a small hint, when you read the tests note that the `format="multipart"` is used when POSTing the `Entry` data.

![image](http://i.imgur.com/JPPXMv1.png)
