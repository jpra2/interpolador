from packs.manager.mesh_data import MeshData
from packs.manager import MeshProperty
import os

def main():
    fine_mesh_properties_name = 'spe10_perturbada'
    mesh_property = MeshProperty()
    mesh_property.insert_mesh_name(fine_mesh_properties_name)
    mesh_property.load_data()
    fids = mesh_property['faces']
    
    path = os.path.join('mesh', 'layer_spe10_perturbada.msh')
    mesh_data = MeshData(dim=2, mesh_path=path)
    mesh_data.create_tag('FACEID', data_type='int')
    mesh_data.insert_tag_data('FACEID', fids, elements_type='faces')
    mesh_data.export_all_elements_type_to_vtk('teste1', element_type='faces')
    