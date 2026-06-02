from packs.manager.mesh_data import MeshData
import os

def main():
    path = os.path.join('mesh', 'layer_spe10_perturbada.msh')
    mesh_data = MeshData(dim=2, mesh_path=path)
    mesh_data.export_all_elements_type_to_vtk('teste1', element_type='faces')
    