def string_to_points(gcode):
    '''
    Convert gcode string to points
    '''
    points = []
    for line in gcode.split('\n'):
        if line.startswith('G01'):
            # print(line.split('X')[1].split('Y')[0])
            x, y = line.split('X')[1].split('Y')[0], line.split('Y')[1].split(' ')[0]
            points.append([float(x), float(y)])
    return points

def file_to_points(filepath):
    '''
    Convert gcode file to points
    '''
    with open(filepath, 'r') as f:
        gcode = f.read()
    return string_to_points(gcode)