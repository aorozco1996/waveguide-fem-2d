import meshio
import numpy as np
from scipy.sparse.linalg import eigsh

def load_mesh(filename):
    # Read the .msh file
    mesh = meshio.read(filename)

    # Get nodes. Only keep x and y coordinates
    nodes = mesh.points[:, :2]

    # Get elements. Assume only triangular elements
    elements = mesh.cells_dict["triangle"]

    # Get boundary nodes
    boundary_lines = mesh.cells_dict["line"]
    boundary_nodes = np.unique(boundary_lines)

    return nodes, elements, boundary_nodes

def _assemble_local_matrix():
    pass

def assemble_te_matrices():
    pass

def assemble_tm_matrices():
    pass

