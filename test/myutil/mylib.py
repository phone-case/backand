import pandas as pd
def Read_xlsx_Data(_file):
    _df = pd.read_excel(_file)
    _df = _df.fillna('')
    _fields = _df.columns.tolist()
    #print(_file)

    _array = []
    _array.append([])
    
    for _f in _fields:
        _array[0].append(_f)
    for _f in _fields:
        _index = 1
        for _a in _df[_f]:
            if _f in _fields[0]:
                _array.append([])
            _array[_index].append(_a)
            _index += 1
    return _array
