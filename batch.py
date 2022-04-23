from sagemaker import AutoML


def marco(name):
    if name == "Marco":
        return "Polo"
    return "No!"


print(marco("Marco"))
