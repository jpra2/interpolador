# import ninpol
from mesh import meshes
import meshio
import numpy as np
from rich import print as rprint
import os



def create_mesh_test():
    # from packs.mpfa_methods.mesh_preprocess import preprocess_mesh
    # from packs.manager import MeshProperty
    
    # mesh_property = MeshProperty()
    # mesh_property.insert_mesh_name(meshes.quad1_preprocess)
    # mesh_property.load_data()
    
    # delta = mesh_property.edges_dim.min()/5
    # nodes_centroids = mesh_property['nodes_centroids']
    # min_nodes = nodes_centroids.min(axis=0)
    # max_nodes = nodes_centroids.max(axis=0)
    
    # nodes1 = mesh_property.nodes[
    #     nodes_centroids[:, 0] <= min_nodes[0] + delta
    # ]
    
    # nodes2 = mesh_property.nodes[
    #     nodes_centroids[:, 0] >= max_nodes[0] - delta
    # ]
    
    path = os.path.join('data', 'quad1')
    # np.save(os.path.join(path, 'nodes1.npy'), nodes1)
    # np.save(os.path.join(path, 'nodes2.npy'), nodes2)
    # np.save(os.path.join(path, 'nodes_centroids.npy'), nodes_centroids)
    # np.save(os.path.join(path, 'nodes.npy'), mesh_property.nodes)
    
    nodes1 = np.load(os.path.join(path, 'nodes1.npy'))
    nodes2 = np.load(os.path.join(path, 'nodes2.npy'))
    nodes_centroids = np.load(os.path.join(path, 'nodes_centroids.npy'))
    nodes = np.load(os.path.join(path, 'nodes.npy'))
    
    dirichlet_nodes = np.concatenate([nodes1, nodes2])
    
    dirichlet = np.zeros(len(nodes_centroids))
    dirichlet[nodes1] = 1.0
    dirichlet[nodes2] = 0.0
    
    neumann = np.zeros(len(nodes_centroids))
    
    neumann_nodes = np.setdiff1d(nodes, dirichlet_nodes)
    # neumann[neumann_nodes] = 0.0
    
    dirichlet_flag = np.zeros(len(nodes_centroids))
    dirichlet_flag[dirichlet_nodes] = 1
    
    neumann_flag = np.zeros(len(nodes_centroids))
    neumann_flag[neumann_nodes] = 1
    
    
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
    
    point_data = {
        "dirichlet_pressure": dirichlet,
        "dirichlet_flag_pressure" : dirichlet_flag,
        "neumann_pressure": neumann,
        "neumann_flag_pressure": neumann_flag
    }
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
    # meshio.write(str(meshes.m3), mesh, file_format="h5m")
    rprint(f"[blue on white]Mesh {meshes.m2} created successfully.[/blue on white]")

def test1():    
    create_mesh_test()
    
    mesh_path = str(meshes.m2)
    # mesh_property = preprocess_mesh(str(meshes.m1), mesh_properties_name=meshes.quad1_preprocess)
    import ninpol
    
    # mesh_path = str(meshes.m1)
    mesh = meshio.read(mesh_path)
    
    interpolator = ninpol.Interpolator(logging=True)
    # interpolator.load_mesh(mesh_path)
    interpolator.load_mesh(mesh_path)
    
    weights, neumann = interpolator.interpolate("pressure", "gls")
    
    
    
    import pdb; pdb.set_trace()