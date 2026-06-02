import ninpol
from mesh import meshes
import meshio
import numpy as np
from rich import print as rprint

from packs.mpfa_methods.mesh_preprocess import preprocess_mesh

def create_mesh_test():
    mesh_path = str(meshes.m1)
    mesh = meshio.read(mesh_path)
    
    meus_dados_de_pressao = [
        np.zeros(len(block.data), dtype=np.float64) for block in mesh.cells
    ]
    
    meus_dados_permeabilidade = [
        np.zeros((len(block.data), 9), dtype=np.float64) for block in mesh.cells
    ]
    
    nquads = len(mesh.cells[2])
    
    perm = np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]).flatten()
    
    permeability = np.zeros((nquads, 9), dtype=np.float64)
    permeability[:] = perm
    meus_dados_permeabilidade[-1] = permeability
    
    point_data = {}
    cell_data = {
        "pressure": meus_dados_de_pressao,
        "permeability": meus_dados_permeabilidade
    }
    
    mesh = meshio.Mesh(
        points=mesh.points,
        cells=mesh.cells,
        point_data=point_data,
        cell_data=cell_data
    )
    
    meshio.write(str(meshes.m2), mesh)
    meshio.write(str(meshes.m3), mesh, file_format="h5m")
    rprint(f"[blue on white]Mesh {meshes.m2} created successfully.[/blue on white]")

def test1():
    create_mesh_test()
    
    mesh_path = str(meshes.m2)
    
    mesh_property = preprocess_mesh(mesh_path, mesh_properties_name='')
    
    interpolator = ninpol.Interpolator(logging=True)
    interpolator.load_mesh(mesh_path)
    
    weights, neumann = interpolator.interpolate("pressure", "gls")
    
    
    
    import pdb; pdb.set_trace()