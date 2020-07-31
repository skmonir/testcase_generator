# Introduction
**Testcase Generator** is a standalone desktop application to prepare the input and output dataset for programming problem. Input generator is implemented using [CodeForces](https://www.codeforces.com/) [testlib.h](https://codeforces.com/testlib) library in C++. This tool is specially helpful for the problem author and tester of a programming competition.

# Features
* ## Input Generator
    Most of the programming problems contain a large number of input dataset. Solver's source code runs against these input dataset and provides verdict accordingly. So it's important to prepare valid testcases. But it's not easy to generate a large number of handmade testcases. This is where Input Generator comes into the picture. It generates specified number of testcase files in just a few seconds.
* ## Output Generator
    For every programming problem there are some input dataset and corresponding output dataset. That means a solver's souce code will be considered correct if the source code runs against the input dataset and produces output exactly same as the judge output dataset. So judge output should be accurate. Output Generator runs the judge solution executable(.exe) against the input dataset and prepare output dataset accordingly in just a few seconds.

# Screenshots
Input Generator screen. The script in the CLI is for generating a tree of nodes 10 to 15.<br>

![](./appdata/screenshots/InputGeneratorScreen.JPG)

<br>
Successfully generated input folder. <br>

![](./appdata/screenshots/InputFolder.JPG)

<br>
Input Generator logs. <br>

![](./appdata/screenshots/InputLog.JPG)

<br>
Output Generator screen. <br>

![](./appdata/screenshots/OutputGenerator.JPG)

<br>
Successfully generated output folder. <br>

![](./appdata/screenshots/OutputFolder.JPG)

# Installation
**Testcase Generator** runs on WINDOWS. 

**Installation steps**:
* Download the installation setup file from [here](https://github.com/skmonir/testcase_generator/releases).
* Double click on the setup to start the installation.
* Select a directory where you want to install and click install.
* After the installation is successful, you will find Testcase Generator shortcut on the Desktop for quick access.
* Open the shortcut from Desktop and enjoy.

# Components
* ## Input Generator
    * ### `No. of File`
        The number of input files to generate. For example, if we select 10, then 10 input files will be generated.

    * ### `File Mode`
        There are two options for File Mode.<br>

        **Write**: If the file already exists then the contents in the file will be overwritten by the new contents. Otherwise, new file will be opened. <br>
        For example, if a file contains a line ```This is older line``` and we now want to write a new line ```This is new line```, then after Write operation the file will contain ```This is new line```. <br>

        **Append**: Applied when expected file already exists. In Append mode, new contents will be concatenated with the older contents in the file.<br>
        In the example in Write mode, if we do the same in Append mode, then the file will contain both lines after Append operation.

    * ### `Test/File`
        Defines the number of testcases for each input file. More formally, it is used for multitest input dataset. `N\A` means there is no multitest. Any other numeric value(Lets define as `T`) means the number of testcases for each input file. So the script/generator executable will run `T` times for a single input file.

        **Example**: Suppose we want to generate an array of 5 integers in range [1, 10].
        
        For `Test/File = N\A`, we will get a random array of size 5 like the following.<br>
        ```
        5
        4 6 7 2 1
        ```

        For `Test/File = 2`, we will get random array of size 5 twice like the following.
        ```
        2
        5
        4 6 7 2 1
        5
        2 10 8 9 5
        ```
    
    * ### `File Prefix`
        The prefix of the filename. More formally, file name will be started with the File Prefix. For example, if we use `input` as File Prefix, then every file name will start with `input`.

    * ### `File Suffix`
        It is basically the extension of the input files. So the suffix can be `txt`, `in` etc. and the filename would be something like `input.txt`, `input.in` respectively.

    * ### `Serial From`
        Every input file will contain a serial number assigned to the file name. First file will get the serial number from `Serial From` field and every subsequent file's serial number will be incresed by 1.<br>
        For example, if we choose 1 in `Serial From`, files will be generated as following:
        ```
        input1.txt
        input2.txt
        input3.txt
        .
        .
        .
        ```

    * ### `Run Generator Script Exe`
        This is one of the generating methods. If we have the executable(.exe) of our own generator script, we can simply use the executable to generate input dataset. After selecting `Run Generator Script Exe` option, a file selector field will be appeared from where we can select out exe file.
    
    * ### `Write TGen Script in CLI`
        This is the simplest method to write script for generator. Introducing a new command line script named `TGen Script` for generating input dataset. A Command Line Interface(CLI) is integrated with the application. Also for the quick access of the available commands, there is a dropdown menu from where we can select expected command and insert it to our CLI.<br>

        ```
        Note: All available commands will be described in the section "About TGen Commands"
        ```

    * ### `Input Directory`
        The directory where all the input files will be saved.

    * ### `Generate Input`
        Clicking **Generate Input** button will start the process of generating input dataset.

    * ### `View Log`
        Clicking **View Log** button will open an window with the logs of input generator. Successful operations will be logged in `green` color text and failed operations will be logged in `red` color text.
    
* ## Output Generator
    * ### `Input Directory`
        The directory from where the input files will be run.
        ```
        Note: Make sure that the directory doesn't contain anything other than the input dataset.
        ```

    * ### `Output Directory`
        The directory where all the output files will be saved.

    * ### `Executable File`
        The executable(.exe) of the solution.

# About TGen Commands
For the sake of simplicity, a new Command Line Script called `TGen Script` is introduced for the application, where to generate a Tree of 5 nodes, `<tree[5]>` is enough.<br>
## General Rules
* Each command is embraced with angular braces(`<>`) to separate from each other.
* Each command has two main parts, `component` and `parameter`. For some commands, `parameter` part is not needed.
* `component` defines the type of testcase. This part contains the component name specified by the application.<br>
E.G. In command `<tree[5]>`, `tree` is the name of the component. For command `<connected_graph[5:10]>`, `connected_graph` is the name of component.
* `parameter` defines the information needed for the specified `component`. `parameter` is embraced with square brackets(`[]`) and parameters inside the square brackets are separated by a single colon(`:`).<br>
E.G. In command `<tree[5]>`, `[5]` defines `parameter`. For command `<connected_graph[5:10]>`, `[5:10]` is the `parameter` part.

## Commands
## `<line>` <br>
Prints a newline. This command has no `parameter`.

## `<space>` <br>
Prints a space. This command has no `parameter`.

## `<$var_name[min_value:max_value]>`
We can generate **integer variable** with random value in range specified in `parameter` by this command. A random value will be printed and stored in the variable so that we use the variable for integer type parameter in any subsequent command. <br>

* Variable name is defined in the `component` part and must precede with dollar sign(`$`). Variable name should contain alphabets and/or only symbol `underscore` (`_`).

* `parameter` part defines the range in integer data type.
    * `min_value`: The minimum value of the variable.
    * `max_value`: The maximum value of the variable.

Note that, `min_value` shouldn't be greater than `max_value`.

**Command**<br>
```javascript
<$n[10:15]>
```
**Output**<br>
A random value in range [10:15]
```
13
```

## `<int_array[size:min_value:max_value:isDistinct:end_with]>`
Generates integer array.
* `size`: The size of the array. Accepts any `integer` type value or variable.
* `min_value`: The minimum `integer` type value of the elements of the array.
* `max_value`: The maximum `integer` type value of the elements of the array.
* `isDistinct`: Accepts `0` or `1`, where `1` means the array will be distinct, `0` means not.
* `end_with`: Array elements will be separated by the value of `end_with`. Accepts `space` or `line`.

Note that, `min_value` shouldn't be greater than `max_value`.

**Command**<br>
```javascript
<$n[5:10]>
<line>
<int_array[$n:1:10:1:space]>
```
**Output**<br>
A space separated distinct array of size $n[5-10]
```
8
5 9 10 1 4 3 7 6
```

## `<int_pair[size:min_value:max_value:isSecondGreaterEqual]>`
Generates integer pair each in one line.
* `size`: The number of pairs to generate. Accepts any `integer` type value or variable.
* `min_value`: The minimum `integer` type value of the pair element.
* `max_value`: The maximum `integer` type value of the pair element.
* `isSecondGreaterEqual`: Accepts `0` or `1`, where `1` means the first element of the pair **will not be greater** than the second element, `0` means otherwise.

Note that, `min_value` shouldn't be greater than `max_value`.

**Command**<br>
```javascript
<$n[5:10]>
<line>
<int_pair[$n:1:10:1]>
```
**Output**<br>
Generates $n[5-10] integer pair in each line.
```
5
4 6
2 3
2 6
5 10
3 8
```

## `<int_permutation[size:indexing]>`
Generates an integer permutation.
* `size`: The number of pairs to generate. Accepts any `integer` type value or variable.
* `indexing`: The base index of the permutation. Accepts `0` or `1`, where `0` means the permutation will be 0-indexed, `1` means 1-indexed.

**Command**<br>
```javascript
<$n[5:10]>
<line>
<int_permutation[$n:0]>
```
**Output**<br>
Generates 0-indexed permutation of size $n[5-10].
```
8
5 2 3 7 0 4 6 1
```

## `<string[number_of_string:min_size:max_size:max_total_size:charset]>`
Generates specified number of strings.
* `number_of_string`: The number of strings to generate. Accepts any `integer` type value or variable.
* `min_size`: The minimum size of each string.
* `max_size`: The maximum size of each string.
* `max_total_size`: The maximum total size of all strings.
* `charset`: Alpha-numeric character set notation. Three available notations are `a-z`, `A-Z` and `0-9`. One or more of them can be used in any order like `a-zA-Z0-9`, `a-z0-9`, `0-9A-Z` etc. But make sure not to put any extra character in charset notation.

Note that, `(number_of_string * max_size) <= max_total_size`.

**Command**<br>
```javascript
<string[5:3:5:30:A-Z0-9a-z]>
```
**Output**<br>
Generates 5 alpha-numeric strings each in one line.
```
QVf14
R4Q
rbLl
dr2M
tFC
```

## `<tree[vertices]>`
Generates a tree.
* `vertices`: The number of vertices of the tree. Accepts any `integer` type value or variable.

**Command**<br>
```javascript
<$n[5:10]>
<line>
<tree[$n]>
```
**Output**<br>
Generates a random Tree of $n[5-10] nodes.
```
9
2 9
6 1
7 9
1 9
6 8
5 2
4 3
4 7
```

## `<weighted_tree[vertices:min_value:max_value]>`
Generates an weighted tree.
* `vertices`: The number of vertices of the tree. Accepts any `integer` type value or variable.
* `min_value`: The minimum `integer` type value of an edge.
* `max_value`: The maximum `integer` type value of an edge.

**Command**<br>
```javascript
<$n[5:10]>
<line>
<weighted_tree[$n:10:15]>
```
**Output**<br>
Generates a random Tree of $n[5-10] nodes where each edge's weight is in between 10-15.
```
9
4 1 12
2 3 14
6 5 12
9 1 15
3 9 15
8 3 13
5 2 14
4 7 11
```

## `<rooted_tree[vertices]>`
Generates a tree rooted at node **1**.
* `vertices`: The number of vertices of the rooted tree. Accepts any `integer` type value or variable.

**Command**<br>
```javascript
<$n[5:10]>
<line>
<rooted_tree[$n]>
```
**Output**<br>
Generates a random Tree of $n[5-10] nodes rooted at node **1**.
```
10
8 6 7 4 8 1 7 3 8
```

## `<connected_graph[vertices:edges]>`
Generates a connected graph.
* `vertices`: The number of vertices of the graph. Accepts any `integer` type value or variable.
* `edges`: The number of edges of the graph. Accepts any `integer` type value or variable.

**Command**<br>
```javascript
<$n[5:5]><space><$m[4:10]>
<line>
<connected_graph[$n:$m]>
```
**Output**<br>
Generates a random connected graph of 5 nodes and 4-10 edges.
```
5 8
3 1
4 5
3 5
5 4
2 5
4 3
2 5
2 1
```


## `<weighted_connected_graph[vertices:edges:min_value:max_value]>`
Generates a connected weighted graph.
* `vertices`: The number of vertices of the graph. Accepts any `integer` type value or variable.
* `edges`: The number of edges of the graph. Accepts any `integer` type value or variable.
* `min_value`: The minimum `integer` type value of an edge.
* `max_value`: The maximum `integer` type value of an edge.

**Command**<br>
```javascript
<$n[5:5]><space><$m[4:10]>
<line>
<weighted_connected_graph[$n:$m:10:15]>
```
**Output**<br>
Generates a random connected graph of 5 nodes and 4-10 edges of weight in between 10-15.
```
5 9
1 5 13
2 5 15
4 3 12
4 2 12
2 3 11
2 1 15
5 4 14
3 5 15
5 4 12
```


## `<int_matrix[row:column:min_value:max_value]>`
Generates matrix where each element is an integer.
* `row`: The number of row of the matrix. Accepts any `integer` type value or variable.
* `column`: The number of column of the matrix. Accepts any `integer` type value or variable.
* `min_value`: The minimum `integer` type value of an element.
* `max_value`: The maximum `integer` type value of an element.

**Command**<br>
```javascript
<$n[4:6]><space><$m[4:6]>
<line>
<int_matrix[$n:$m:1:9]>
```
**Output**<br>
Generates a random integer matrix of $n[4-6] rows and $m[4-6] columns where each element is in between 1-10.
```
5 6
6 5 9 4 8 5
9 3 7 6 7 9
4 4 5 6 9 7
8 8 8 4 9 6
7 7 8 9 5 7
```


## `<char_matrix[row:column:charset]>`
Generates matrix where each element is a alpha-numeric character.
* `row`: The number of row of the matrix. Accepts any `integer` type value or variable.
* `column`: The number of column of the matrix. Accepts any `integer` type value or variable.
* `charset`: Alpha-numeric character set notation. Three available notations are `a-z`, `A-Z` and `0-9`. One or more of them can be used in any order like `a-zA-Z0-9`, `a-z0-9`, `0-9A-Z` etc. But make sure not to put any extra character in charset notation.

**Command**<br>
```javascript
<$n[4:6]><space><$m[4:6]>
<line>
<char_matrix[$n:$m:a-zA-Z]>
```
**Output**<br>
Generates a random character matrix of $n[4-6] rows and $m[4-6] columns where each element is an uppercase or lowercase latin letter.
```
4 5
RmbAI
WhmtP
CjmMy
QYNzo
```


# Examples
## Script to generate testcase for [D. Serval and Rooted Tree](https://codeforces.com/problemset/problem/1153/D).
```javascript
<$n[2:300000]>
<line>
<int_array[$n:0:1:0:space]>
<line>
<rooted_tree[$n]>
```


## Script to generate testcase for [F. TorCoder](https://codeforces.com/contest/240/problem/F).
```javascript
<$n[1:100000]><space><$m[1:100000]>
<line>
<string[1:$n:$n:$n:a-z]>
<line>
<int_pair[$m:1:$n:1]>
```

## Script to generate testcase for [D. Birthday](https://codeforces.com/contest/494/problem/D).
```javascript
<$n[1:100000]>
<line>
<weighted_tree[$n:1:1000000000]>
<line>
<$q[1:100000]>
<line>
<int_pair[$q:1:$n:0]>
```

# Bottleneck
The application is implemented using [Python Tkinter](https://docs.python.org/3/library/tkinter.html) GUI framework for developing light desktop application. Tkinter is single threaded framework and it doesn't allow any other thread on the application. Basically, when any other thread is spawned the framework prevents interaction with the UI. Input Generator and Output Generator both uses multiple thread creation for faster performance. So be careful not to put heavy load on the application. Otherwise the application will be crashed and you will end up blaming me. :grin: