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
    kc_sq_tm, Ez_tm = fem_solver.solve_eigenvalue_problem(A_tm, B_tm)
    kc_sq_te, Hz_te = fem_solver.solve_eigenvalue_problem(A_te, B_te)

    # Plot dispersion curves
    postprocessing.compare_cutoff_table(
        'rectangular',
        kc_sq_te,
        kc_sq_tm,
        a=width,
        b=height,
    )

    postprocessing.plot_dispersion_curves(
        'rectangular',
        kc_sq_te,
        kc_sq_tm,
        a=width,
        b=height,
    )
    # Plot modal distributions


def run_circular_waveguide(radius, mesh_size):
    if GENERATE_MESH:
        meshing.generate_circular_mesh(radius, mesh_size)

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

    # # Circular waveguide
    # radius = 10e-3
    #
    # run_circular_waveguide(radius, mesh_size)
    #
    # # Single ridge waveguide
    # ridge_width = 0.4 * width
    # ridge_depth = 0.4 * height
    #
    # run_single_ridge_waveguide(width, height, ridge_width, ridge_depth, mesh_size)
    #
    # # double ridge waveguide
    # ridge_width = 0.4 * width
    # ridge_depth = 0.35 * height
    #
    # run_double_ridge_waveguide(width, height, ridge_width, ridge_depth, mesh_size)

if __name__ == '__main__':
    main()

