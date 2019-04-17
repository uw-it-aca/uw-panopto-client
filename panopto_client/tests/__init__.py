def instance_args(call_args_list):
    args = []
    for call in call_args_list:
        args.append(call[0][0])
    return sorted(args)
