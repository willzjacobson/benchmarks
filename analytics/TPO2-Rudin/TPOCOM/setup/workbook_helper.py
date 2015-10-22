'''
Point list workbook helper.
'''
import xlrd

def get_sheets(workbook, sheet_name_substr='TPO-input'):
    '''
    Returns a list of sheets from the workbook that contain 
    the sheet_name_substr substring in their names. For getting sheets that 
    have TPO input points use 'TPO-input', and for getting sheets
    with TPO-output points use 'TPO-output'. 
    '''
    book = xlrd.open_workbook(workbook)
    input_sheet_names = ([sheet_name for sheet_name in book.sheet_names() 
                            if sheet_name_substr in sheet_name])
    input_sheets = [book.sheet_by_name(sheet) for sheet in input_sheet_names]
    return input_sheets

def get_points(sheets, name_col = 3, sig_code_col = 4, sig_prog_col = 5, point_type_col = 6):
    '''
    Return a list of dictionaries, one for each point in the sheets.
    The other parameters refer to the column numbers for the point parts
    in the sheet.
    '''
    points = []
    for sheet in sheets:
        for row in range(sheet.nrows):
            point_cells = ({'name':sheet.cell(row, name_col), 
                'sig_code':sheet.cell(row, sig_code_col),
                'sig_prog':sheet.cell(row, sig_prog_col), 
                'point_type':sheet.cell(row, point_type_col)})
            if check_point_cells(point_cells):
                point = {attr: val.value.strip() for (attr, val) in point_cells.items()}
                points.append(point)
    return points

def check_point_cells(point_cells):
    '''
    Check if all the given point cells have a valid entry.
    '''
    for (attr, val) in point_cells.items():
        if val.ctype in set([0,5,6]): return False
        if val.value == '': return False
    return True