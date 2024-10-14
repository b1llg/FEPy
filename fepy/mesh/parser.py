

def msh_parse(file):
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
            if "$MeshFormat" in  mesh_data[i]:
                state = "MeshFormat"
            elif "$PhysicalNames" in mesh_data[i]:
                state = "PhysicalNames"


            if state == "MeshFormat":
                pass

                        

            
            

def main():
    print(__name__)

if __name__ == "__main__":
    main()