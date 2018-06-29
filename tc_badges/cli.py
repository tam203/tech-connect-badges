import sys
from tc_badges.create import main as create
from tc_badges.award import main as award
from tc_badges.list import main as lst

methods = {
    'create': create,
    'award': award,
    'list': lst
}


def help(msg):
    print(msg + """\n
        tc_badge <method> [args...]

        <method> one of %s
    
    """ % ', '.join(methods.keys()))


args = sys.argv[1:]

if(len(args)) == 0:
    help("not enough args")
    sys.exit(1)

method, args = args[0], args[1:]
if not method in methods.keys():
    help("%s not in allowed methods" % method)

methods[method](args)
