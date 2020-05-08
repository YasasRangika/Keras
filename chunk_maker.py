import os
import numpy as np


def split(filehandler, delimiter=',', row_limit=720000, output_name_template='chunk_%s.csv',
          output_path='n_folded/x_chunks/',
          keep_headers=True):
    import csv
    reader = csv.reader(filehandler, delimiter=delimiter)
    current_piece = 1
    current_out_path = os.path.join(
        output_path,
        output_name_template % current_piece
    )
    current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
    current_limit = row_limit
    if keep_headers:
        headers = next(reader)
        current_out_writer.writerow(headers)
    for i, row in enumerate(reader):
        if i + 1 > current_limit:
            current_piece += 1
            current_limit = row_limit * current_piece
            current_out_path = os.path.join(
                output_path,
                output_name_template % current_piece
            )
            current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
            if keep_headers:
                current_out_writer.writerow(headers)
        current_out_writer.writerow(row)


split(open('x_dataset.csv', 'r'))


arr = np.loadtxt('y_dataset.txt')
i = 1
for val in np.split(arr, 5):
    np.savetxt('n_folded/y_chunks/chunk_%s.txt' % i, val)
    i += 1
