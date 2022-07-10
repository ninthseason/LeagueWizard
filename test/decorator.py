def register():
    def dec(func):
        print(2)

    return dec


def deco(func):
    print(1)

    def wrapper():
        print("ok")
        pass

    return wrapper


@register()
def foo():
    print(1)
