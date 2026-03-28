import meshing
import fem_solver
import postprocessing

# Set GENERATE_MESH to True to re-generate the mesh. If set to False, it will try to load the existing mesh (if any)
GENERATE_MESH=False

def run_rectangular_waveguide(width, height, mesh_size):
    if GENERATE_MESH:
        meshing.generate_rectangular_mesh(width, height, mesh_size)

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

