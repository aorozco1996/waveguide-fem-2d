import numpy as np

import meshing
import fem_solver
import postprocessing

# Set GENERATE_MESH to True to re-generate the mesh. If set to False, it will try to load the existing mesh (if any)
# If generating meshes, click on the Gmsh window context that opens at runtime for the program to continue execution
GENERATE_MESH=True

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
    Ez_tm_unique = Ez_tm[:, 1:]

    kc_sq_te_unique = kc_sq_te[[1, 3, 4]]
    Hz_te_unique = Hz_te[:, [1, 3, 4]]

    # Plot dispersion curves
    postprocessing.plot_dispersion_curves(kc_sq_tm_unique, kc_sq_te_unique, width, b=height, waveguide_type='rectangular')

    # Plot modal distributions

    # TM modes: pad with zeros to match nodes dimensions
    interior_nodes = [i for i in range(len(nodes)) if i not in boundary_nodes]
    Ez_tm_full = np.zeros(len(nodes))
    tm_labels = ["TM$_{21}$", "TM$_{31}$", "TM$_{12}$"]
    tm_modes = [(2,1), (3,1), (1,2)]

    for i in range(3):
        Ez_tm_full[interior_nodes] = Ez_tm_unique[:, i]
        postprocessing.plot_fem_mode_distribution(nodes, elements, Ez_tm_full, 'Ez', mode_label=tm_labels[i])
        postprocessing.plot_analytical_mode_distribution(width, tm_modes[i][0], tm_modes[i][1], 'Ez', b=height)

    # TE modes
    te_labels = ["TE$_{10}$", "TE$_{01}$", "TE$_{11}$"]
    te_modes = [(1, 0), (0, 1), (1, 1)]

    for i in range(3):
        postprocessing.plot_fem_mode_distribution(nodes, elements, Hz_te_unique[:, i], 'Hz', mode_label=te_labels[i])
        postprocessing.plot_analytical_mode_distribution(width, te_modes[i][0], te_modes[i][1], 'Hz', b=height)


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

    # Omit degenerate modes so that there are 6 unique eigenvalues
    kc_sq_tm_unique = kc_sq_tm[[0, 1, 3]]
    Ez_tm_unique = Ez_tm[:, [0, 1, 3]]

    kc_sq_te_unique = kc_sq_te[[1, 3, 6]]
    Hz_te_unique = Hz_te[:, [1, 3, 6]]

    # Plot dispersion curves
    postprocessing.plot_dispersion_curves(kc_sq_tm_unique, kc_sq_te_unique, radius, waveguide_type='circular')

    # Plot modal distributions

    # TM modes: pad with zeros to match nodes dimensions
    interior_nodes = [i for i in range(len(nodes)) if i not in boundary_nodes]
    Ez_tm_full = np.zeros(len(nodes))
    tm_labels = ["TM$_{01}$", "TM$_{11}$", "TM$_{21}$"]
    tm_modes = [(0, 1), (1, 1), (2, 1)]

    for i in range(3):
        Ez_tm_full[interior_nodes] = Ez_tm_unique[:, i]
        postprocessing.plot_fem_mode_distribution(nodes, elements, Ez_tm_full, 'Ez', mode_label=tm_labels[i])
        postprocessing.plot_analytical_mode_distribution(radius, tm_modes[i][0], tm_modes[i][1], 'Ez', waveguide_type='circular')

    # TE modes
    te_labels = ["TE$_{11}$", "TE$_{21}$", "TE$_{31}$"]
    te_modes = [(1, 1), (2, 1), (3, 1)]

    for i in range(3):
        postprocessing.plot_fem_mode_distribution(nodes, elements, Hz_te_unique[:, i], 'Hz', mode_label=te_labels[i])
        postprocessing.plot_analytical_mode_distribution(radius, te_modes[i][0], te_modes[i][1], 'Hz', waveguide_type='circular')

def run_single_ridge_waveguide(width, height, ridge_width, ridge_depth, mesh_size):
    print('Running Single Ridge Waveguide FEM simulation...')
    print(f'Waveguide dimensions: a = {width} [m], b = {height} [m], w = {ridge_width} [m], d = {ridge_depth} [m]')
    if GENERATE_MESH:
        print('Generating mesh...')
        meshing.generate_single_ridge_mesh(width, height, ridge_width, ridge_depth, mesh_size)

    # Load mesh data
    nodes, elements, boundary_nodes = fem_solver.load_mesh('single_ridge_waveguide.msh')

    print('Mesh Details')
    print(f'Element size: {mesh_size} [m]')
    print(f'Total nodes: {len(nodes)}')
    print(f'Total elements: {len(elements)}')
    print(f'Total boundary nodes: {len(boundary_nodes)}')

    # Assemble tm and te matrices
    A_tm, B_tm = fem_solver.assemble_tm_matrices(nodes, elements, boundary_nodes)
    A_te, B_te = fem_solver.assemble_te_matrices(nodes, elements)

    # Solve eigenvalue problems
    kc_sq_tm, Ez_tm = fem_solver.solve_eigenvalue_problem(A_tm, B_tm, num_modes=3)
    kc_sq_te, Hz_te = fem_solver.solve_eigenvalue_problem(A_te, B_te, num_modes=4)

    # Omit degenerate modes so that there are 6 unique eigenvalues
    kc_sq_tm_unique = kc_sq_tm
    Ez_tm_unique = Ez_tm

    kc_sq_te_unique = kc_sq_te[1:]
    Hz_te_unique = Hz_te[:,1:]


    # Plot dispersion curves
    postprocessing.plot_dispersion_curves(kc_sq_tm_unique, kc_sq_te_unique, width, b=height, waveguide_type='single_ridge')

    # Plot modal distributions

    # TM modes: pad with zeros to match nodes dimensions
    interior_nodes = [i for i in range(len(nodes)) if i not in boundary_nodes]
    Ez_tm_full = np.zeros(len(nodes))
    tm_labels = ["Dominant TM Mode", "First Higher-Order TM Mode", "Second Higher-Order TM Mode"]

    for i in range(3):
        Ez_tm_full[interior_nodes] = Ez_tm_unique[:, i]
        postprocessing.plot_fem_mode_distribution(nodes, elements, Ez_tm_full, 'Ez', mode_label=tm_labels[i])

    # TE modes
    te_labels = ["Dominant TE Mode", "First Higher-Order TE Mode", "Second Higher-Order TE Mode"]

    for i in range(3):
        postprocessing.plot_fem_mode_distribution(nodes, elements, Hz_te_unique[:, i], 'Hz', mode_label=te_labels[i])

def run_double_ridge_waveguide(width, height, ridge_width, ridge_depth, mesh_size):
    print('Running Double Ridge Waveguide FEM simulation...')
    print(f'Waveguide dimensions: a = {width} [m], b = {height} [m], w = {ridge_width} [m], d = {ridge_depth} [m]')
    if GENERATE_MESH:
        print('Generating mesh...')
        meshing.generate_double_ridge_mesh(width, height, ridge_width, ridge_depth, mesh_size)

    # Load mesh data
    nodes, elements, boundary_nodes = fem_solver.load_mesh('double_ridge_waveguide.msh')

    print('Mesh Details')
    print(f'Element size: {mesh_size} [m]')
    print(f'Total nodes: {len(nodes)}')
    print(f'Total elements: {len(elements)}')
    print(f'Total boundary nodes: {len(boundary_nodes)}')

    # Assemble tm and te matrices
    A_tm, B_tm = fem_solver.assemble_tm_matrices(nodes, elements, boundary_nodes)
    A_te, B_te = fem_solver.assemble_te_matrices(nodes, elements)

    # Solve eigenvalue problems
    kc_sq_tm, Ez_tm = fem_solver.solve_eigenvalue_problem(A_tm, B_tm, num_modes=5)
    kc_sq_te, Hz_te = fem_solver.solve_eigenvalue_problem(A_te, B_te, num_modes=5)

    # Omit degenerate modes so that there are 6 unique eigenvalues
    kc_sq_tm_unique = kc_sq_tm[[0,2,4]]
    Ez_tm_unique = Ez_tm[:, [0,2,4]]

    kc_sq_te_unique = kc_sq_te[[1,2,4]]
    Hz_te_unique = Hz_te[:,[1,2,4]]

    # Plot dispersion curves
    postprocessing.plot_dispersion_curves(kc_sq_tm_unique, kc_sq_te_unique, width, b=height, waveguide_type='double_ridge')

    # Plot modal distributions

    # TM modes: pad with zeros to match nodes dimensions
    interior_nodes = [i for i in range(len(nodes)) if i not in boundary_nodes]
    Ez_tm_full = np.zeros(len(nodes))
    tm_labels = ["Dominant TM Mode", "First Higher-Order TM Mode", "Second Higher-Order TM Mode"]

    for i in range(3):
        Ez_tm_full[interior_nodes] = Ez_tm_unique[:, i]
        postprocessing.plot_fem_mode_distribution(nodes, elements, Ez_tm_full, 'Ez', mode_label=tm_labels[i])

    # TE modes
    te_labels = ["Dominant TE Mode", "First Higher-Order TE Mode", "Second Higher-Order TE Mode"]

    for i in range(3):
        postprocessing.plot_fem_mode_distribution(nodes, elements, Hz_te_unique[:, i], 'Hz', mode_label=te_labels[i])

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
    ridge_width = 0.3 * width
    ridge_depth = 0.4 * height

    run_single_ridge_waveguide(width, height, ridge_width, ridge_depth, mesh_size)

    # double ridge waveguide
    ridge_width = 0.3 * width
    ridge_depth = 0.35 * height

    run_double_ridge_waveguide(width, height, ridge_width, ridge_depth, mesh_size)

if __name__ == '__main__':
    main()

