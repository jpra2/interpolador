import gmsh
import random
import os
import numpy as np

from packs.get_connect import extrair_conectividade_2d

def main(seed=3):
    path = os.path.join('mesh', 'layer_spe10.msh')
    path2 = os.path.join('mesh', 'layer_spe10_perturbada.msh')
    
    Lx = 60
    Ly = 220
    
    random.seed(seed)
    
    gmsh.initialize()
    gmsh.open(path)
    
    fator_ruido = 0.15

    # 3. Obter todos os nós da malha
    node_tags, coords, _ = gmsh.model.mesh.getNodes()
    elem_types, elem_tags, elem_node_tags = gmsh.model.mesh.getElements()
    coords = np.array(coords, dtype=float).reshape(-1, 3)
    
    ids, nos_por_elemento = extrair_conectividade_2d()
    
    np.save(os.path.join('results', 'elements_ids.npy'), ids)
    np.save(os.path.join('results', 'nodes_per_element.npy'), nos_por_elemento)
    np.save(os.path.join('results', 'node_tags.npy'), node_tags)
    np.save(os.path.join('results', 'coords.npy'), coords)
    
    import pdb; pdb.set_trace()
    
    # Colocar as coordenadas em um dicionário {id_do_no: [x, y, z]} para facilitar a edição
    mapa_coordenadas = {tag: list(coords[i*3 : (i+1)*3]) for i, tag in enumerate(node_tags)}

    nos_no_contorno = set()
    linhas = gmsh.model.getEntities(dim=1)
    
    nos1 = gmsh.model.getEntities(dim=0)
    
    for dim, tag in nos1:
        tag_do_no, _, _ = gmsh.model.mesh.getNodes(dim, tag)
        nos_no_contorno.update(tag_do_no)   
    
    for dim, tag in linhas:
        tags_da_linha, _, _ = gmsh.model.mesh.getNodes(dim, tag)
        nos_no_contorno.update(tags_da_linha)
    
    
    nos_no_contorno = np.array(list(nos_no_contorno))
    
    # 3. Aplicar a perturbação vetorizada nas coordenadas internas
    for i, tag in enumerate(node_tags):
        if tag not in nos_no_contorno:
            # Recupera as posições originais decimais puras
            
            x, y, z = coords[i]
            
            # Gera o deslocamento aleatório
            dx = (random.random() - 0.5) * fator_ruido * Lx
            dy = (random.random() - 0.5) * fator_ruido * Ly
            
            novo_x = x + dx
            novo_y = y + dy
            novo_z = z # Ative 'z + dz' se a malha for tridimensional
            
            # 5. ATUALIZAÇÃO DIRETA E SEGURA:
            # Força o envio como uma lista nativa de floats do Python [x, y, z]
            gmsh.model.mesh.setNode(int(tag), [novo_x, novo_y, novo_z], [])
                
            
    # # 5. Criar um novo modelo limpo para salvar a malha perturbada sem conflitos
    # gmsh.model.add("malha_com_jitter")

    # # Criamos uma entidade discreta (superfície ID 1) para ancorar a malha
    # gmsh.model.addDiscreteEntity(2, 1)

    # # Adicionar os nós reconstruídos (usa a API padrão addNodes)
    # gmsh.model.mesh.addNodes(2, 1, node_tags, coords.flatten())
    
    
    # for e_type, e_tags, e_n_tags in zip(elem_types, elem_tags, elem_node_tags):
    #     gmsh.model.mesh.addElements(2, 1, [e_type], [e_tags], [e_n_tags])
    
    # 1. Forçar a versão do formato MSH para 2.2 (Legado)
    gmsh.option.setNumber("Mesh.MshFileVersion", 2.2)

    # 2. Configurar o formato de escrita para ASCII (0 = ASCII, 1 = Binário)
    gmsh.option.setNumber("Mesh.Binary", 0)
        
    gmsh.write(path2)
    
    gmsh.finalize()
     
    
if __name__ == "__main__":
    
    main()
