#! /usr/bin/env python

import sys
import onnx
import onnx_graphsurgeon as gs
from typing import Optional
from argparse import ArgumentParser

class Color:
    BLACK          = '\033[30m'
    RED            = '\033[31m'
    GREEN          = '\033[32m'
    YELLOW         = '\033[33m'
    BLUE           = '\033[34m'
    MAGENTA        = '\033[35m'
    CYAN           = '\033[36m'
    WHITE          = '\033[37m'
    COLOR_DEFAULT  = '\033[39m'
    BOLD           = '\033[1m'
    UNDERLINE      = '\033[4m'
    INVISIBLE      = '\033[08m'
    REVERCE        = '\033[07m'
    BG_BLACK       = '\033[40m'
    BG_RED         = '\033[41m'
    BG_GREEN       = '\033[42m'
    BG_YELLOW      = '\033[43m'
    BG_BLUE        = '\033[44m'
    BG_MAGENTA     = '\033[45m'
    BG_CYAN        = '\033[46m'
    BG_WHITE       = '\033[47m'
    BG_DEFAULT     = '\033[49m'
    RESET          = '\033[0m'


def variable_switch(
    from_output_variable_name: str,
    to_input_variable_name: str,
    input_onnx_file_path: Optional[str] = '',
    onnx_graph: Optional[onnx.ModelProto] = None,
    output_onnx_file_path: Optional[str] = '',
    non_verbose: Optional[bool] = False,
) -> onnx.ModelProto:
    """
    Parameters
    ----------
    from_output_variable_name: str
        Output variable name of the connection change source. \n\
        e.g.\n\
        output_op_names = "output1"

    to_input_variable_name: str
        Input variable name of connection change destination. \n\
        e.g.\n\
        output_op_names = "input1"

    input_onnx_file_path: Optional[str]
        Input onnx file path.\n\
        Either input_onnx_file_path or onnx_graph must be specified.\n\
        Default: ''

    onnx_graph: Optional[onnx.ModelProto]
        onnx.ModelProto.\n\
        Either input_onnx_file_path or onnx_graph must be specified.\n\
        onnx_graph If specified, ignore input_onnx_file_path and process onnx_graph.

    output_onnx_file_path: Optional[str]
        Output onnx file path. If not specified, no ONNX file is output.\n\
        Default: ''

    non_verbose: Optional[bool]
        Do not show all information logs. Only error logs are displayed.\n\
        Default: False

    Returns
    -------
    variable_switched_graph: onnx.ModelProto
        onnx.ModelProto with variable switched
    """

    # Unspecified check for input_onnx_file_path and onnx_graph
    if not input_onnx_file_path and not onnx_graph:
        print(
            f'{Color.RED}ERROR:{Color.RESET} '+
            f'One of input_onnx_file_path or onnx_graph must be specified.'
        )
        sys.exit(1)

    if not from_output_variable_name:
        print(
            f'{Color.RED}ERROR:{Color.RESET} '+
            f'from_output_variable_name must be specified.'
        )
        sys.exit(1)

    if not to_input_variable_name:
        print(
            f'{Color.RED}ERROR:{Color.RESET} '+
            f'to_input_variable_name must be specified.'
        )
        sys.exit(1)

    # Loading Graphs
    # onnx_graph If specified, onnx_graph is processed first
    if not onnx_graph:
        onnx_graph = onnx.load(input_onnx_file_path)
    graph = gs.import_onnx(onnx_graph)
    graph.cleanup().toposort()

    switch_target_output_var = None
    switch_target_input_node = None
    switch_target_input_var = None
    for graph_node in graph.nodes:
        if switch_target_output_var is None:
            for graph_node_output in graph_node.outputs:
                if graph_node_output.name == from_output_variable_name:
                    switch_target_output_var = graph_node_output
                    break
        if switch_target_input_var is None:
            for graph_node_input in graph_node.inputs:
                if graph_node_input.name == to_input_variable_name:
                    switch_target_input_node = graph_node
                    switch_target_input_var = graph_node_output
                    break
        if switch_target_output_var is not None and switch_target_input_var is not None:
            break

    if switch_target_output_var is None:
        print(
            f'{Color.RED}ERROR:{Color.RESET} '+
            f'from_output_variable_name must be an output variable name that exists in the model. '+
            f'from_output_variable_name: {from_output_variable_name}'
        )
        sys.exit(1)

    if switch_target_input_var is None:
        print(
            f'{Color.RED}ERROR:{Color.RESET} '+
            f'to_input_variable_name must be an output variable name that exists in the model. '+
            f'to_input_variable_name: {to_input_variable_name}'
        )
        sys.exit(1)

    for idx in range(len(switch_target_input_node.inputs)):
        if switch_target_input_node.inputs[idx].name == to_input_variable_name:
            switch_target_input_node.inputs[idx] = switch_target_output_var
            break

    graph.outputs = [
        graph_output for graph_output in graph.outputs if graph_output.name != from_output_variable_name
    ]

    graph.cleanup().toposort()

    # Shape Estimation
    variable_switched_graph = None
    try:
        variable_switched_graph = onnx.shape_inference.infer_shapes(gs.export_onnx(graph))
    except:
        variable_switched_graph = gs.export_onnx(graph)
        if not non_verbose:
            print(
                f'{Color.YELLOW}WARNING:{Color.RESET} '+
                'The input shape of the next OP does not match the output shape. '+
                'Be sure to open the .onnx file to verify the certainty of the geometry.'
            )

    # Save
    if output_onnx_file_path:
        onnx.save(variable_switched_graph, output_onnx_file_path)

    if not non_verbose:
        print(f'{Color.GREEN}INFO:{Color.RESET} Finish!')

    # Return
    return variable_switched_graph


def main():
    parser = ArgumentParser()
    parser.add_argument(
        '-if',
        '--input_onnx_file_path',
        type=str,
        required=True,
        help='Input onnx file path.'
    )
    parser.add_argument(
        '-fovn',
        '--from_output_variable_name',
        type=str,
        required=True,
        help=\
            'Output variable name of the connection change source. \n'+
            'e.g.\n'+
            '--from_output_variable_name "output1"'
    )
    parser.add_argument(
        '-tivn',
        '--to_input_variable_name',
        type=str,
        required=True,
        help=\
            'Input variable name of connection change destination. \n'+
            'e.g.\n'+
            '--to_input_variable_name "input1"'
    )
    parser.add_argument(
        '-of',
        '--output_onnx_file_path',
        type=str,
        required=True,
        help='Output onnx file path.'
    )
    parser.add_argument(
        '-n',
        '--non_verbose',
        action='store_true',
        help='Do not show all information logs. Only error logs are displayed.'
    )
    args = parser.parse_args()

    input_onnx_file_path = args.input_onnx_file_path
    from_output_variable_name = args.from_output_variable_name
    to_input_variable_name = args.to_input_variable_name
    output_onnx_file_path = args.output_onnx_file_path
    non_verbose = args.non_verbose

    # Load
    onnx_graph = onnx.load(input_onnx_file_path)

    # Output OP add
    variable_switched_graph = variable_switch(
        from_output_variable_name=from_output_variable_name,
        to_input_variable_name=to_input_variable_name,
        input_onnx_file_path=None,
        onnx_graph=onnx_graph,
        output_onnx_file_path=output_onnx_file_path,
        non_verbose=non_verbose,
    )


if __name__ == '__main__':
    main()
