import meshio
import numpy as np
from scipy.sparse import lil_matrix, csr_matrix
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

def _assemble_matrices(nodes, elements):
    # Initialize global matrices A and B
    num_nodes = len(nodes)
    A_matrix = lil_matrix((num_nodes, num_nodes), dtype=float)
    B_matrix = lil_matrix((num_nodes, num_nodes), dtype=float)

    # Factor from integration of basis function over triangular area (eq. 9.2.31 \cite{jin2011theory})
    barycentric_factor = (1.0 / 12.0) * np.array([
        [2.0, 1.0, 1.0],
        [1.0, 2.0, 1.0],
        [1.0, 1.0, 2.0]
    ])

    for element in elements:
        # Get (x, y) pairs from element nodes
        x1, y1 = nodes[element[0]]
        x2, y2 = nodes[element[1]]
        x3, y3 = nodes[element[2]]

        # Calculate cofactors (only need b and c)
        b1 = y2 - y3
        b2 = y3 - y1
        b3 = y1 - y2

        c1 = x3 - x2
        c2 = x1 - x3
        c3 = x2 - x1

        # Calculate area of triangular element
        area = abs(0.5 * (b1*c2 - b2*c1))

        # Evaluate the entry for matrix A for the current element
        A_element = (1 / (4.0 * area)) * np.array([
            [b1*b1 + c1*c1, b1*b2 + c1*c2, b1*b3 + c1*c3],
            [b2*b1 + c2*c1, b2*b2 + c2*c2, b2*b3 + c2*c3],
            [b3*b1 + c3*c1, b3*b2 + c3*c2, b3*b3 + c3*c3]
        ])

        # Evaluate the entry for matrix B for the current element
        B_element = barycentric_factor * area

        # Incrementally add to matrices A and B
        for i in range(3):
            for j in range(3):
                A_matrix[element[i], element[j]] += A_element[i, j]
                B_matrix[element[i], element[j]] += B_element[i, j]

    return A_matrix.tocsr(), B_matrix.tocsr()


def assemble_te_matrices(nodes, elements):
    # Assemble A and B matrices
    A_te, B_te = _assemble_matrices(nodes, elements)

    # No need to enforce boundary condition
    return A_te, B_te

def assemble_tm_matrices(nodes, elements, boundary_nodes):
    # Assemble A and B matrices
    A_matrix, B_matrix = _assemble_matrices(nodes, elements)

    # Exclude boundary nodes for boundary condition, i.e., Ez = 0 on Gamma
    interior_nodes = [i for i in range(len(nodes)) if i not in boundary_nodes]
    A_tm = A_matrix[interior_nodes, :][:, interior_nodes]
    B_tm = B_matrix[interior_nodes, :][:, interior_nodes]

    return A_tm, B_tm

def solve_eigenvalue_problem(A, B, num_modes=3):
    # Calculate eigenvalues and eigenvectors
    eigenvalues, eigenvectors = eigsh(A, k=num_modes, M=B, which='SM')

    # Sort eigenvalues and eigenvectors in increasing order
    order = np.argsort(eigenvalues)
    return eigenvalues[order], eigenvectors[:, order]