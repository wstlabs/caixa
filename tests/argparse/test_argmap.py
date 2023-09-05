from caixa.argparse import ArgSpec 

T = {}
T['trivial-1'] = dict(cmd="", mono="", pair="", index=0)
T['trivial-2'] = dict(cmd="foo bar", mono="", pair="", index=0)
T['simple-1'] = dict(cmd="-h --help foo", mono="-h,--help", pair="", index=2)
T['simple-2'] = dict(cmd="-h --help", mono="-h,--help", pair="", index=2)
T['simple-3'] = dict(cmd="foo --help", mono="-h,--help", pair="", index=0)
T['simple-4'] = dict(cmd="foo -h --help", mono="-h,--help", pair="", index=0)
T['simple-5'] = dict(cmd="-h foo --help", mono="-h,--help", pair="", index=1)
T['simple-6'] = dict(cmd="--limit=2 foo", mono="", pair="--limit", index=1)
T['simple-7'] = dict(cmd="--limit 2 foo", mono="", pair="--limit", index=2)
T['simple-8'] = dict(cmd="--limit 2", mono="", pair="--limit", index=2)
T['simple-9'] = dict(cmd="--help", mono="--help", pair="", index=1)
T['mixed-1'] = dict(cmd="--limit 2 --help foo", mono="--help", pair="--limit", index=3)
T['mixed-2'] = dict(cmd="--help --limit 2 foo", mono="--help", pair="--limit", index=3)
T['fail-1'] = dict(cmd="--limit", mono="--help", pair="--limit", index=-1, reason="value expected for keyword argument --limit")
T['fail-2'] = dict(cmd="--limit --help foo", mono="--help", pair="--limit", index=-1, reason="value expected for keyword argument --limit")
T['fail-3'] = dict(cmd="--help=bar --help foo", mono="--help", pair="--limit", index=-1, reason="unexpected value for soliton keyword --help")
T['fail-4'] = dict(cmd="--help", mono="", pair="--limit", index=-1, reason="unrecognized term '--help' at position 0")

def test_argmap():
    global T
    for (label, spec) in T.items(): 
        print("..")
        print(f"{label}: {spec}")
        command = spec['cmd'].split(" ")
        rawspec = {k: spec[k] for k in ('mono', 'pair')}
        argspec = ArgSpec(rawspec)
        print(f"{label}: rawcmd = |{spec['cmd']}|")
        print(f"{label}: argspec = {argspec}")
        print(f"{label}: _val = {argspec._val}")
        print(f"{label}: command = {command}")
        argmap = argspec.resolve(command)
        print(f"{label}: argmap = {argmap}")
        status = 'OK' if argmap.index == spec['index'] else 'BAD'
        print(f"{label}: {status}")
        assert argmap.index == spec['index']


def main():
    global T
    test_argmap()


if __name__ == '__main__':
    main()


