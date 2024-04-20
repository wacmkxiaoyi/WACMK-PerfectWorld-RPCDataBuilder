import re, json, sys

maps = {
    "std::string": "string",
    "std::vector": "vector",
    "std::map": "maps",
    "std::pair": "pair",
    "std::list": "vector",
    "std::deque": "vector",
    "std::set": "vector",
    "float": "float32",
    "unsigned long": "ulong",
    "unsigned int": "uint",
    "unsignedint": "uint",
    "unsigned short": "ushort",
    "unsignedshort": "ushort",
    "unsigned char": "uchar",
    "unsignedchar": "uchar",
    "bool": "ubool",
    "int64_t": "slong",
    "long long": "slong",
    "long": "slong",
    "int": "sint",
    "size_t": "sint",
    "time_t": "sint",
}


def get_calls(file="call.dat"):
    def extract_data_from_call(line):
        match = re.match(r"^call\s+(.+)$", line)
        if match:
            call_data = match.group(1)
            inner_data_match = re.findall(r"\(([^()]+)\)", call_data)
            if inner_data_match:
                return inner_data_match[-1]

        return None

    def clean_str(ss):
        def stack(type_str):
            def to_jsonstr(input_str):
                input_str = (
                    input_str.replace("&lt", "[")
                    .replace("&gt", "]")
                    .replace("<", "[")
                    .replace(">", "]")
                    .replace(";", "")
                )
                input_str = f'[{input_str.replace("[[","<<").replace("[",",[").replace("<<","[[")}]'.replace(
                    " ", ""
                )
                input_str = input_str.replace("[", '["').replace("]", '"]')
                input_str = input_str.replace(",", '","')
                input_str = input_str.replace('"[', "[").replace(']"', "]")
                return input_str

            def res_stack(stacks):
                nstacks = [stacks[0]]
                for i in stacks[1:]:
                    if type(i) in (list, tuple):
                        nstacks[-1] = [
                            nstacks[-1],
                            (
                                res_stack(i)[0]
                                if nstacks[-1] in ("std::vector",)
                                else res_stack(i)
                            ),
                        ]
                    else:
                        nstacks.append(i)
                return nstacks

            stacks = json.loads(to_jsonstr(type_str))
            return res_stack(stacks)[0]

        ss = ss.split(" ")[0]
        return stack(ss)

    def rep_str(ss):
        if type(ss) in (list, tuple):
            return [rep_str(i) for i in ss]
        elif "GNET::" == ss[: len("GNET::")]:
            return f"{ss[len('GNET::'):]}"
        elif ss in maps:
            return maps[ss]
        return ss

    lines = open(file).readlines()
    results = []
    for line in lines:
        result = extract_data_from_call(line)
        if result:
            result = f"{rep_str(clean_str(result))}".replace("'", "").replace('"', "")
            results.append(result)
    return results


def get_names(file="source.dat"):
    def extract_data_from_line(line):
        match = re.search(r"\(([^()]+)\)", line)
        if match:
            inner_data = match.group(1)
            arrow_index = inner_data.find("->")
            if arrow_index != -1:
                return inner_data[arrow_index + 2 :]
            return inner_data.split(",")[1].strip()
        return None

    lines = open(file).readlines()
    results = []
    for line in lines:
        result = extract_data_from_line(line)
        if result:
            results.append(result)
    return results


def output(
    clsname,
    isclass="True",
    filename="result.py",
    file_call="call.dat",
    file_name="source.dat",
):
    call = get_calls(file_call)
    name = get_names(file_name)
    if isclass.lower() != "false":
        strc = f"class {clsname}(RPCB.{clsname}):\n"
        strc += "\t@classmethod\n"
        strc += "\tdef map(cls,*obj): return {\n"
    else:
        strc = clsname + "={\n"
    for i in range(len(call)):
        strc += (
            "\t" if isclass.lower() != "false" else ""
        ) + f'\t"{name[i]}":{call[i]},\n'
    if strc[-2] == ",":
        strc = strc[:-2] + "\n" + ("\t" if isclass.lower() != "false" else "") + "\t}\n"
    else:
        strc = strc[:-1] + "}\n"
    with open(filename, "w") as file:
        file.writelines(strc)


if __name__ == "__main__":
    output(*sys.argv[1:])
