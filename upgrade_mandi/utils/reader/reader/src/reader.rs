use calamine::{DataType, Xlsx, XlsxError, open_workbook};
use std::ffi::{CStr, CString};
use std::os::raw::c_char;
use std::ptr;

/**
 * value: Pointer to a C string
 * kind: 0: Empty, 1: String, 2: Int, 3: Float, 4: Bool, 5: Date
 *
 * functionality: This struct holds the value of the cell and the type of the cell
 */
#[repr(C)]
pub struct Cell {
    value: *mut c_char,
    kind: u8, // 0: Empty, 1: String, 2: Int, 3: Float, 4: Bool, 5: Date
}

/**
 * data: Pointer to an array of C strings (* Cell)
 * rows: Number of rows in the table
 * cols: Number of columns in the table
 * functionality: This struct holds single dimension array to hold the data of the excel matrix data
 * and the number of rows and columns in the table.
 */
#[repr(C)]
pub struct Table {
    data: *mut Cell,
    rows: usize,
    cols: usize,
}

#[unsafe(no_mangle)]
pub extern "C" fn read_excel(file_name: *const c_char, sheet_name: *const c_char) -> *mut Table {
    if file_name.is_null() || sheet_name.is_null() {
        return ptr::null_mut();
    }

    let c_file = unsafe { CStr::from_ptr(file_name) };
    let c_sheet = unsafe { CStr::from_ptr(sheet_name) };

    let file_name_str = match c_file.to_str() {
        Ok(s) => s.to_string(),
        Err(_) => return ptr::null_mut(),
    };

    let sheet_name_str = match c_sheet.to_str() {
        Ok(s) => s.to_string(),
        Err(_) => return ptr::null_mut(),
    };

    match do_read_excel(file_name_str, sheet_name_str) {
        Ok(table) => table,
        Err(_) => ptr::null_mut(),
    }
}

fn do_read_excel(file_name: String, sheet_name: String) -> Result<*mut Table, XlsxError> {
    let mut workbook: Xlsx<_> = open_workbook(file_name)?;
    let range = workbook.worksheet_range_ref(&sheet_name)?;

    let rows = range.height();
    let cols = range.width();

    // Flatten directly into a vector of C strings
    let mut flat: Vec<Cell> = Vec::with_capacity(rows * cols);

    for row in range.rows() {
        for cell in row {
            let value = if cell.is_datetime() {
                match cell.as_date() {
                    Some(s) => s.to_string(),
                    _ => "".to_string(),
                }
            } else {
                match cell.as_string() {
                    Some(s) => s.to_string(),
                    _ => "".to_string(),
                }
            };

            let kind = if cell.is_empty() {
                0
            } else if cell.is_string() {
                1
            } else if cell.is_int() {
                2
            } else if cell.is_float() {
                3
            } else if cell.is_bool() {
                4
            } else if cell.is_datetime() {
                5
            } else {
                0
            };

            flat.push(Cell {
                value: CString::new(value).unwrap().into_raw(),
                kind,
            });
        }
    }

    let data_ptr = flat.as_mut_ptr();
    std::mem::forget(flat); // Prevent Rust from freeing memory

    let table = Box::new(Table {
        data: data_ptr,
        rows,
        cols,
    });

    Ok(Box::into_raw(table))
}

#[unsafe(no_mangle)]
pub extern "C" fn free_table(table_ptr: *mut Table) {
    if table_ptr.is_null() {
        return;
    }

    let table = unsafe { Box::from_raw(table_ptr) };
    let total = (table.rows * table.cols) as isize;

    // Free each C string
    for i in 0..total {
        let cell = unsafe { (*table).data.offset(i) };
        if unsafe { !(*cell).value.is_null() } {
            unsafe {
                let _ = CString::from_raw((*cell).value);
                (*cell).value = std::ptr::null_mut();
            };
        }
    }

    // Free the data pointer itself
    unsafe {
        Vec::from_raw_parts(table.data, total as usize, total as usize);
    }
}
