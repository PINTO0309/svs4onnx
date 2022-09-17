# svs4onnx
A very simple tool to swap connections between output and input variables in an ONNX graph. **S**imple **V**ariable **S**witch for **ONNX**.

https://github.com/PINTO0309/simple-onnx-processing-tools

[![Downloads](https://static.pepy.tech/personalized-badge/svs4onnx?period=total&units=none&left_color=grey&right_color=brightgreen&left_text=Downloads)](https://pepy.tech/project/svs4onnx) ![GitHub](https://img.shields.io/github/license/PINTO0309/svs4onnx?color=2BAF2B) [![PyPI](https://img.shields.io/pypi/v/svs4onnx?color=2BAF2B)](https://pypi.org/project/svs4onnx/) [![CodeQL](https://github.com/PINTO0309/svs4onnx/workflows/CodeQL/badge.svg)](https://github.com/PINTO0309/svs4onnx/actions?query=workflow%3ACodeQL)

<p align="center">
  <img src="https://user-images.githubusercontent.com/33194443/190839161-dcea1864-e369-43cf-87ee-7bd3da96b615.png" />
</p>

## 1. Setup
### 1-1. HostPC
```bash
### option
$ echo export PATH="~/.local/bin:$PATH" >> ~/.bashrc \
&& source ~/.bashrc

### run
$ pip install -U onnx \
&& python3 -m pip install -U onnx_graphsurgeon --index-url https://pypi.ngc.nvidia.com \
&& pip install -U svs4onnx
```
### 1-2. Docker
https://github.com/PINTO0309/simple-onnx-processing-tools#docker

## 2. CLI Usage
```
$ svs4onnx -h

usage:
    svs4onnx [-h]
    -if INPUT_ONNX_FILE_PATH
    -fovn FROM_OUTPUT_VARIABLE_NAME
    -tivn TO_INPUT_VARIABLE_NAME
    -of OUTPUT_ONNX_FILE_PATH
    [-n]

optional arguments:
  -h, --help
        show this help message and exit.

  -if INPUT_ONNX_FILE_PATH, --input_onnx_file_path INPUT_ONNX_FILE_PATH
        Input onnx file path.

  -fovn FROM_OUTPUT_VARIABLE_NAME, --from_output_variable_name FROM_OUTPUT_VARIABLE_NAME
        Output variable name of the connection change source.
        e.g.
        --from_output_variable_name "output1"

  -tivn TO_INPUT_VARIABLE_NAME, --to_input_variable_name TO_INPUT_VARIABLE_NAME
        Input variable name of connection change destination.
        e.g.
        --to_input_variable_name "input1"

  -of OUTPUT_ONNX_FILE_PATH, --output_onnx_file_path OUTPUT_ONNX_FILE_PATH
        Output onnx file path.

  -n, --non_verbose
        Do not show all information logs. Only error logs are displayed.
```

## 3. In-script Usage
```python
>>> from svs4onnx import variable_switch
>>> help(variable_switch)

Help on function variable_switch in module svs4onnx.onnx_model_variable_switch:

variable_switch(
    from_output_variable_name: str,
    to_input_variable_name: str,
    input_onnx_file_path: Union[str, NoneType] = '',
    onnx_graph: Union[onnx.onnx_ml_pb2.ModelProto, NoneType] = None,
    output_onnx_file_path: Union[str, NoneType] = '',
    non_verbose: Union[bool, NoneType] = False,
) -> onnx.onnx_ml_pb2.ModelProto

    Parameters
    ----------
    from_output_variable_name: str
        Output variable name of the connection change source.
        e.g.
        output_op_names = "output1"

    to_input_variable_name: str
        Input variable name of connection change destination.
        e.g.
        output_op_names = "input1"

    input_onnx_file_path: Optional[str]
        Input onnx file path.
        Either input_onnx_file_path or onnx_graph must be specified.
        Default: ''

    onnx_graph: Optional[onnx.ModelProto]
        onnx.ModelProto.
        Either input_onnx_file_path or onnx_graph must be specified.
        onnx_graph If specified, ignore input_onnx_file_path and process onnx_graph.

    output_onnx_file_path: Optional[str]
        Output onnx file path. If not specified, no ONNX file is output.
        Default: ''

    non_verbose: Optional[bool]
        Do not show all information logs. Only error logs are displayed.
        Default: False

    Returns
    -------
    variable_switched_graph: onnx.ModelProto
        onnx.ModelProto with variable switched
```

## 4. CLI Execution
```bash
$ svs4onnx \
--input_onnx_file_path movenet_multipose_lightning_192x256_nopost_tmp1.onnx \
--from_output_variable_name "cast1_output" \
--to_input_variable_name "StatefulPartitionedCall/strided_slice_21" \
--output_onnx_file_path movenet_multipose_lightning_192x256_nopost_tmp2.onnx
```

## 5. In-script Execution
```python
from svs4onnx import variable_switch

onnx_graph = variable_switch(
    from_output_variable_name="cast1_output",
    to_input_variable_name="StatefulPartitionedCall/strided_slice_21",
    input_onnx_file_path="movenet_multipose_lightning_192x256_nopost_tmp1.onnx",
    output_onnx_file_path="movenet_multipose_lightning_192x256_nopost_tmp2.onnx",
)
```

## 6. Sample
```bash
$ svs4onnx \
--input_onnx_file_path movenet_multipose_lightning_192x256_nopost_tmp1.onnx \
--from_output_variable_name "cast1_output" \
--to_input_variable_name "StatefulPartitionedCall/strided_slice_21" \
--output_onnx_file_path movenet_multipose_lightning_192x256_nopost_tmp2.onnx
```
### Before
![image](https://user-images.githubusercontent.com/33194443/190838853-fe38c4af-0666-43c5-bae5-4c12fa3838b7.png)

### After
![image](https://user-images.githubusercontent.com/33194443/190838904-ce867f2d-2de5-45a4-b80a-334c80c5b24f.png)

## 7. Reference
1. https://github.com/onnx/onnx/blob/main/docs/Operators.md
2. https://docs.nvidia.com/deeplearning/tensorrt/onnx-graphsurgeon/docs/index.html
3. https://github.com/NVIDIA/TensorRT/tree/main/tools/onnx-graphsurgeon
4. https://github.com/PINTO0309/simple-onnx-processing-tools
5. https://github.com/PINTO0309/PINTO_model_zoo

## 8. Issues
https://github.com/PINTO0309/simple-onnx-processing-tools/issues
