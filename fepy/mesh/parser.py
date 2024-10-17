
def msh_parser(file):

    # Generate basic entities container

    # check that file format is .msh

    if file.split('.')[-1] != "msh":
        raise TypeError("extension needs to be of type 'msh'")

    # Read file line by line
    with open(file) as mesh_data:

        mesh_data = list(mesh_data)

        nlines = len(mesh_data)
        i = 0

        while i < nlines:
            if "$End" in mesh_data[i]:
                # If end of section go to next line
                state = "End"

            elif "$MeshFormat" in mesh_data[i]:
                state = "MeshFormat"
                i += 1

            elif "$PhysicalNames" in mesh_data[i]:
                state = "PhysicalNames"
                i += 1  # skip section header
                # read number of physical names
                num_physical_name = int(mesh_data[i])
                i += 1  # go to next line

            elif "$Entities" in mesh_data[i]:
                state = "Entities"
                i + 1

                line = mesh_data[i].split()

                num_points = line[0]
                #! TO DEBUG: index goes over bound
                num_curves = line[1]
                num_surfaces = line[2]
                num_volumes = line[3]

                i += 1

            match state:

                case "End": 
                    i += 1

                case "MeshFormat":
                    line = mesh_data[i].split()

                    msh_version = line[0]
                    file_mode = line[1]
                    int_size = line[2]

                    i += 1
                case "PhysicalNames":

                    # Initialiaze a boundary for each defined boundary
                    boundaries = dict()

                    # Loop over msh file within the physical name section
                    while "$End" not in mesh_data[i]:
                        boundary = mesh_data[i].split()

                        # define variables for current boundary
                        btype = boundary[0]
                        bid = boundary[1]
                        bname = boundary[2]

                        temp_dict = {}

                        temp_dict = {"id":  bid, "type": btype}

                        boundaries[bname] = temp_dict

                        i += 1
                case "Entities":
                    
                    # Generate dictionary for each type of entities
                    points_entities = {}
                    curves_entities = {}
                    surfaces_entites = {}
                    volumes_entites = {}

                    # loop over the points in the file, must update i on each loop
                    # num_points is assigned earlier
                    for j in range(num_points):
                        line = mesh_data[i]

                        # extract ddata
                        tag = line[0]
                        x = line[1]
                        y = line[2]
                        z = line[3]
                        num_physical_tags = line[4]
                        physical_tags = []

                        # if theres tags
                        k = 0
                        if num_physical_tags >= 1:
                            # append tags number
                            while k < num_physical_tags:
                                physical_tags.append(line[5 + k])
                                k += 1

                        i+=1

                    # loop over the curves in the file, must update i on each loop
                    # num_curves is assigned earlier
                    for j in range(num_curves):
                        line = mesh_data[i]

                        tag = line[0]
                        min_x = line[1]
                        min_y = line[2]
                        min_z = line[3]
                        max_x = line[4]
                        max_y = line[5]
                        max_z = line[6]
                        num_physical_tags = line[7]

                        physical_tags = []

                        # if theres tags
                        k = 0
                        if num_physical_tags >= 1:
                            # append tags number
                            while k < num_physical_tags:
                                physical_tags.append(line[8 + k])
                                k += 1
                            k += 8  # locate the iterator for bounding points
                        num_bounding_points = line[k]

                        bounding_points = []

                        z = 0 # iterator for bounding points
                        if num_bounding_points >= 1:
                            while z < num_bounding_points:
                                bounding_points.append(line[k + z])
                                z += 1


                        i+=1

                    for j in range(num_surfaces):
                        pass

                    for j in range (num_volumes):
                        pass
                    


                case "_":
                    ValueError(
                        "Error in reading .msh file: Trying to parse a section called {state}")


def main():
    print(__name__)


if __name__ == "__main__":
    main()
