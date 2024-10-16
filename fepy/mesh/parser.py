import pyexodus


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
                i += 1 # skip section header
                num_physical_name = int(mesh_data[i]) # read number of physical names
                i += 1 # go to next line

            elif "$Entities" in  mesh_data[i]:
                 state = "Entities"
                 i + 1

                 """
                 ******************* WIP
                 """

            match state:
                case "MeshFormat":
                    line = mesh_data[i].split()

                    msh_version = line[0]
                    file_mode = line[1]
                    int_size = line[2]

                    i += 1
                case "PhysicalNames":

                    #Initialiaze a boundary for each defined boundary
                    boundaries = dict()

                    # Loop over msh file within the physical name section
                    while "$End" not in mesh_data[i]:
                        boundary = mesh_data[i].split()

                        # define variables for current boundary
                        btype = boundary[0]
                        bid = boundary[1]
                        bname = boundary[2]

                        temp_dict = {}

                        temp_dict = {"id":  bid, "type" : btype}

                        boundaries[bname] = temp_dict

                        i += 1

                    
                    
                case "End":
                    i += 1

                case "_":
                    ValueError(
                        "Error in reading .msh file: Trying to parse a section called {state}")


def main():
    print(__name__)


if __name__ == "__main__":
    main()
