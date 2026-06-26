class UnwrapResourceMixin:
    resource_key = None

    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs and self.resource_key:
            kwargs["data"] = kwargs["data"].get(self.resource_key, kwargs["data"])
        return super().get_serializer(*args, **kwargs)
