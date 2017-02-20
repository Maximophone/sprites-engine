import os

classes = {}

for module_name in os.listdir(os.path.dirname(__file__)):
    if module_name == '__init__.py' or module_name[-3:] != '.py':
        continue

    module = __import__(module_name[:-3], locals(), globals())
    classes[module_name[:-3]] = getattr(module,module_name[:-3])


del module_name
