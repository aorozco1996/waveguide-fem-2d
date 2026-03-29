import numpy as np

import meshing
import fem_solver
import postprocessing

# Set GENERATE_MESH to True to re-generate the mesh. If set to False, it will try to load the existing mesh (if any)
GENERATE_MESH=False

def run_rectangular_waveguide(width, height, mesh_size):
    print('Running Rectangular Waveguide FEM simulation...')
    print(f'Waveguide dimensions: a = {width} [m], b = {height} [m]')
    if GENERATE_MESH:
        print('Generating mesh...')
        meshing.generate_rectangular_mesh(width, height, mesh_size)

    # Load mesh data
    nodes, elements, boundary_nodes = fem_solver.load_mesh('rectangular_waveguide.msh')

    print('Mesh Details')
    print(f'Element size: {mesh_size} [m]')
    print(f'Total nodes: {len(nodes)}')
    print(f'Total elements: {len(elements)}')
    print(f'Total boundary nodes: {len(boundary_nodes)}')

    # Assemble tm and te matrices
    A_tm, B_tm = fem_solver.assemble_tm_matrices(nodes, elements, boundary_nodes)
    A_te, B_te = fem_solver.assemble_te_matrices(nodes, elements)

    # Solve eigenvalue problems
    kc_sq_tm, Ez_tm = fem_solver.solve_eigenvalue_problem(A_tm, B_tm, num_modes=4)
    kc_sq_te, Hz_te = fem_solver.solve_eigenvalue_problem(A_te, B_te, num_modes=5)

    # Omit degenerate modes so that there are 6 unique eigenvalues
    kc_sq_tm_unique = kc_sq_tm[1:]
    Ez_tm_unique = Ez_tm[1:]

    kc_sq_te_unique = np.concatenate((kc_sq_te[1:2], kc_sq_te[3:]))
    Hz_te_unique = np.concatenate((Hz_te[1:2], Hz_te[3:]))

    # Plot dispersion curves
    postprocessing.plot_dispersion_curves(kc_sq_tm_unique, kc_sq_te_unique, width, b=height, waveguide_type='rectangular')

    # Plot modal distributions


def run_circular_waveguide(radius, mesh_size):
    print('Running Circular Waveguide FEM simulation...')
    print(f'Waveguide dimensions: a = {radius} [m]')
    if GENERATE_MESH:
        print('Generating mesh...')
        meshing.generate_circular_mesh(radius, mesh_size)

    # Load mesh data
    nodes, elements, boundary_nodes = fem_solver.load_mesh('circular_waveguide.msh')

    print('Mesh Details')
    print(f'Element size: {mesh_size} [m]')
    print(f'Total nodes: {len(nodes)}')
    print(f'Total elements: {len(elements)}')
    print(f'Total boundary nodes: {len(boundary_nodes)}')

    # Assemble tm and te matrices
    A_tm, B_tm = fem_solver.assemble_tm_matrices(nodes, elements, boundary_nodes)
    A_te, B_te = fem_solver.assemble_te_matrices(nodes, elements)

    # Solve eigenvalue problems
    kc_sq_tm, Ez_tm = fem_solver.solve_eigenvalue_problem(A_tm, B_tm, num_modes=4)
    kc_sq_te, Hz_te = fem_solver.solve_eigenvalue_problem(A_te, B_te, num_modes=7)

    print(kc_sq_tm)
    print(kc_sq_te)

    # Omit degenerate modes so that there are 6 unique eigenvalues
    kc_sq_tm_unique = np.concatenate((kc_sq_tm[:2], kc_sq_tm[3:]))
    Ez_tm_unique = np.concatenate((Ez_tm[:2], Ez_tm[3:]))
    kc_sq_te_unique = np.concatenate((kc_sq_te[1:2], kc_sq_te[3:4], kc_sq_te[6:7]))
    Hz_te_unique = np.concatenate((Hz_te[1:2], Hz_te[3:4], Hz_te[6:7]))

    print(kc_sq_tm_unique)
    print(kc_sq_te_unique)

    # # Plot dispersion curves
    postprocessing.plot_dispersion_curves(kc_sq_tm_unique, kc_sq_te_unique, radius, waveguide_type='circular')

    # Plot modal distributions

def run_single_ridge_waveguide(width, height, ridge_width, ridge_depth, mesh_size):
    if GENERATE_MESH:
        meshing.generate_single_ridge_mesh(width, height, ridge_width, ridge_depth, mesh_size)

def run_double_ridge_waveguide(width, height, ridge_width, ridge_depth, mesh_size):
    if GENERATE_MESH:
        meshing.generate_double_ridge_mesh(width, height, ridge_width, ridge_depth, mesh_size)

def main():
    mesh_size = 5e-4
    # Rectangular waveguide dimensions (a and b comparable to WR75 but with nicer metric dimensions)
    width = 20e-3  # a [m]
    height = width / 2  # b = a/2

    run_rectangular_waveguide(width, height, mesh_size)

    # Circular waveguide
    radius = 10e-3

    run_circular_waveguide(radius, mesh_size)

    # Single ridge waveguide
    ridge_width = 0.4 * width
    ridge_depth = 0.4 * height

    run_single_ridge_waveguide(width, height, ridge_width, ridge_depth, mesh_size)

    # double ridge waveguide
    ridge_width = 0.4 * width
    ridge_depth = 0.35 * height

    run_double_ridge_waveguide(width, height, ridge_width, ridge_depth, mesh_size)

if __name__ == '__main__':
    main()

