# Copyright 2021 Andreas Steck (steck.andi@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List

from carebt.treeNode import TreeNode


class ExecutionContext():

    def __init__(self, parent: TreeNode, node: TreeNode, params: str):
        self.call_in_params: List[str] = []
        self.call_out_params: List[str] = []

        if(params is not None):
            params = params.replace('   ', ' ')
            params = params.replace('  ',  ' ')

            # extract call input params if available
            for p in filter(None, params.split('=>')[0].split(' ')):
                # param is a careBt variable (starts with ?)
                if(p[0] == '?'):
                    self.call_in_params.append(p)
                else:
                    try:
                        # param is a member variable of the parent
                        self.call_in_params.append(eval(f'parent.{p}'))
                    except SyntaxError:
                        # param is a value
                        self.call_in_params.append(eval(p))
            self.call_in_params = tuple(self.call_in_params)

            # extract call output params if available
            if(len(params.split('=>')) == 2):
                for p in filter(None, params.split('=>')[1].split(' ')):
                    self.call_out_params.append(p)
                self.call_out_params = tuple(self.call_out_params)

        # the node
        self.node = node

        # placeholder for the instance of the node
        self.instance = None
