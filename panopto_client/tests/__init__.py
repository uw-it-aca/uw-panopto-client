# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


def instance_args(call_args_list):
    args = []
    for call in call_args_list:
        args.append(call[0][0])
    return sorted(args)
