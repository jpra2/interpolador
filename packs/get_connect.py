import gmsh
import numpy as np

def extrair_conectividade_2d():
    """
    Lê a malha atual do Gmsh e retorna:
    - ids_elementos: Array NumPy (1D) com os IDs únicos de cada elemento 2D.
    - conectividade: Array NumPy (2D) onde cada linha contém as tags dos nós daquele elemento.
    """
    # 1. Recuperar todos os elementos da malha global
    elem_types, elem_tags, node_tags_per_elem = gmsh.model.mesh.getElements()
    
    lista_ids = []
    lista_conectividade = []
    
    # 2. Filtrar apenas elementos de dimensão 2 (Superfícies/Retângulos)
    for i, e_type in enumerate(elem_types):
        # Descobre a dimensão e quantos nós o tipo possui
        _, dim, num_nos, _, _, _ = gmsh.model.mesh.getElementProperties(e_type)
        
        if dim == 2:  # Filtro estrito para pegar apenas elementos de superfície
            tags_do_tipo = elem_tags[i]
            nos_do_tipo = node_tags_per_elem[i].copy()
            
            nos_do_tipo = nos_do_tipo.reshape(-1, 4)              
            
        
            return tags_do_tipo, nos_do_tipo
