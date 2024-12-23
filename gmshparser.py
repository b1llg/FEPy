import os

class GMSHParser:
    def __init__(self, filename):
        self.filename = filename
        self.sections = {}
        
    def parse(self):
        """Parse the GMSH .msh file and store sections in self.sections"""
        current_section = None
        current_content = []
        
        with open(self.filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                    
                if line.startswith('$'):
                    if line.startswith('$End'):
                        # End of section
                        if current_section:
                            self.sections[current_section] = self._parse_section(current_section, current_content)
                            current_section = None
                            current_content = []
                    else:
                        # Start of section
                        current_section = line[1:]  # Remove $ prefix
                else:
                    if current_section:
                        current_content.append(line)
    
    def _parse_section(self, section_name, content):
        """Parse specific sections based on their format"""
        if not content:
            return None
            
        if section_name == 'MeshFormat':
            return self._parse_mesh_format(content)
        elif section_name == 'PhysicalNames':
            return self._parse_physical_names(content)
        elif section_name == 'Entities':
            return self._parse_entities(content)
        elif section_name == 'Nodes':
            return self._parse_nodes(content)
        elif section_name == 'Elements':
            return self._parse_elements(content)
        return content  # Return raw content for unimplemented sections
    
    def _parse_mesh_format(self, content):
        """
        Parse the MeshFormat section
        Format: version file-type data-size
        """
        if not content:
            return None
            
        parts = content[0].split()
        if len(parts) != 3:
            raise ValueError(f"Invalid MeshFormat line: expected 3 values, got {len(parts)}")
            
        return {
            'version': float(parts[0]),
            'file_type': int(parts[1]),
            'data_size': int(parts[2])
        }
    
    def _parse_physical_names(self, content):
        """Parse the PhysicalNames section"""
        if not content:
            return None
        num_names = int(content[0])
        names = []
        for line in content[1:num_names+1]:
            dim, tag, name = line.split(' ', 2)
            names.append({
                'dimension': int(dim),
                'tag': int(tag),
                'name': name.strip('"')
            })
        return names
    
    def _parse_entities(self, content):
        """Parse the Entities section"""
        if not content:
            return None
        num_points, num_curves, num_surfaces, num_volumes = map(int, content[0].split())
        
        entities = {
            'points': [],
            'curves': [],
            'surfaces': [],
            'volumes': []
        }
        
        current_line = 1
        
        # Parse points
        for _ in range(num_points):
            parts = content[current_line].split()
            point = {
                'tag': int(parts[0]),
                'x': float(parts[1]),
                'y': float(parts[2]),
                'z': float(parts[3])
            }
            if len(parts) > 4:
                num_phys_tags = int(parts[4])
                point['physical_tags'] = [int(parts[i]) for i in range(5, 5 + num_phys_tags)]
            entities['points'].append(point)
            current_line += 1
            
        # Parse curves, surfaces, and volumes similarly...
        # (Implementation simplified for brevity - would need to be expanded for full functionality)
        
        return entities
    
    def _parse_nodes(self, content):
        """Parse the Nodes section"""
        if not content:
            return None
        num_blocks, num_nodes, min_tag, max_tag = map(int, content[0].split())
        
        nodes = {
            'num_blocks': num_blocks,
            'num_nodes': num_nodes,
            'min_tag': min_tag,
            'max_tag': max_tag,
            'blocks': []
        }
        
        current_line = 1
        for _ in range(num_blocks):
            entity_dim, entity_tag, parametric = map(int, content[current_line].split())
            num_nodes_in_block = int(content[current_line + 1])
            
            block = {
                'entity_dim': entity_dim,
                'entity_tag': entity_tag,
                'parametric': parametric,
                'nodes': []
            }
            
            # Skip node tags
            current_line += 2
            tags = []
            for _ in range(num_nodes_in_block):
                tags.append(int(content[current_line]))
                current_line += 1
            
            # Read coordinates
            for i in range(num_nodes_in_block):
                coords = list(map(float, content[current_line].split()))
                node = {
                    'tag': tags[i],
                    'x': coords[0],
                    'y': coords[1],
                    'z': coords[2]
                }
                if parametric:
                    if entity_dim >= 1:
                        node['u'] = coords[3]
                    if entity_dim >= 2:
                        node['v'] = coords[4]
                    if entity_dim == 3:
                        node['w'] = coords[5]
                block['nodes'].append(node)
                current_line += 1
            
            nodes['blocks'].append(block)
        
        return nodes
    
    def _parse_elements(self, content):
        """Parse the Elements section"""
        if not content:
            return None
        num_blocks, num_elements, min_tag, max_tag = map(int, content[0].split())
        
        elements = {
            'num_blocks': num_blocks,
            'num_elements': num_elements,
            'min_tag': min_tag,
            'max_tag': max_tag,
            'blocks': []
        }
        
        current_line = 1
        for _ in range(num_blocks):
            entity_dim, entity_tag, element_type = map(int, content[current_line].split())
            num_elements_in_block = int(content[current_line + 1])
            
            block = {
                'entity_dim': entity_dim,
                'entity_tag': entity_tag,
                'element_type': element_type,
                'elements': []
            }
            
            current_line += 2
            for _ in range(num_elements_in_block):
                parts = list(map(int, content[current_line].split()))
                element = {
                    'tag': parts[0],
                    'nodes': parts[1:]
                }
                block['elements'].append(element)
                current_line += 1
                
            elements['blocks'].append(block)
            
        return elements

# Usage example
if __name__ == "__main__":
    
    file = "example_5p14.msh"
    path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
    file = os.path.join(path, file)
    
    parser = GMSHParser(file)
    parser.parse()
    
    # Access parsed sections
    mesh_format = parser.sections.get('MeshFormat')
    nodes = parser.sections.get('Nodes')
    elements = parser.sections.get('Elements')