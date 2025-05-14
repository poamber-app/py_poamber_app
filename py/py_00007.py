# Comment: Split a pathname into components (the opposite of os.path.join)
in a platform-neutral way.
def fullsplit(path, result=None):
    
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)


# define packages left out from packing/installing
# Example:
# EXCLUDE_FROM_PACKAGES = ['accord.conf.project_template',
#                          'accord.conf.app_template',
#                          'accord.bin']
#


