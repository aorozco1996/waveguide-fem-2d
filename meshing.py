import gmsh

# Set DEBUG to True to visualize the mesh in the GUI. Close the GUI to continue execution
DEBUG=True

def generate_rectangular_mesh(a, b, mesh_size):
    # Initialize Gmsh
    gmsh.initialize()
    # Print messages to console
    gmsh.option.setNumber("General.Terminal", 1)
    # Create model
    gmsh.model.add("rectangular_waveguide")

    # Create points for waveguide corners
    gmsh.model.geo.addPoint(0, 0, 0, mesh_size, 1)
    gmsh.model.geo.addPoint(a, 0, 0, mesh_size, 2)
    gmsh.model.geo.addPoint(a, b, 0, mesh_size, 3)
    gmsh.model.geo.addPoint(0, b, 0, mesh_size, 4)

    # Connect points with lines
    gmsh.model.geo.addLine(1, 2, 1)
    gmsh.model.geo.addLine(2, 3, 2)
    gmsh.model.geo.addLine(3, 4, 3)
    gmsh.model.geo.addLine(4, 1, 4)

    # Define curve loop for surface
    gmsh.model.geo.addCurveLoop([1, 2, 3, 4], 1)

    # Create plane surface
    gmsh.model.geo.addPlaneSurface([1], 1)

    # Synchronize entities
    gmsh.model.geo.synchronize()

    # Define physical groups for PEC walls and surface
    gmsh.model.addPhysicalGroup(1, [1, 2, 3, 4], 1)
    gmsh.model.setPhysicalName(1, 1, "PEC")

    gmsh.model.addPhysicalGroup(2, [1], 2)
    gmsh.model.setPhysicalName(2, 2, "surface")

    # Generate mesh
    gmsh.model.mesh.generate(2)

    # Display surfaces and nodes
    gmsh.fltk.initialize()

    # Visualization options
    gmsh.option.setNumber("General.Axes", 1)
    gmsh.option.setColor("General.Background", 255, 255, 255)
    gmsh.option.setColor("General.Foreground", 0, 0, 0)

    # Export mesh image
    gmsh.write("figures/rectangular_waveguide.png")

    # Save mesh to file
    gmsh.write('rectangular_waveguide.msh')


    if DEBUG:
        # Visualize mesh
        gmsh.fltk.run()

    # Finalize Gmsh
    gmsh.finalize()


def generate_circular_mesh(r, mesh_size):
    # Initialize Gmsh
    gmsh.initialize()
    # Print messages to console
    gmsh.option.setNumber("General.Terminal", 1)
    # Create model
    gmsh.model.add('circular_waveguide')
    # Create points for circular waveguide
    gmsh.model.geo.addPoint(r, r, 0, mesh_size, 1)  # Center
    gmsh.model.geo.addPoint(2*r, r, 0, mesh_size, 2)
    gmsh.model.geo.addPoint(0, r, 0, mesh_size, 3)


    gmsh.model.geo.addCircleArc(2, 1, 3, 1)  # Top half
    gmsh.model.geo.addCircleArc(3, 1, 2, 2)  # Bottom half

    gmsh.model.geo.addCurveLoop([1, 2], 1)

    # Create plane surface
    gmsh.model.geo.addPlaneSurface([1], 1)

    # Synchronize entities
    gmsh.model.geo.synchronize()

    # Define physical groups for PEC walls and surface
    gmsh.model.addPhysicalGroup(1, [1, 2], 1)
    gmsh.model.setPhysicalName(1, 1, "PEC")

    gmsh.model.addPhysicalGroup(2, [1], 2)
    gmsh.model.setPhysicalName(2, 2, "surface")

    # Generate mesh
    gmsh.model.mesh.generate(2)

    # Display surfaces and nodes
    gmsh.fltk.initialize()

    # Visualization options
    gmsh.option.setNumber("General.Axes", 1)
    gmsh.option.setColor("General.Background", 255, 255, 255)
    gmsh.option.setColor("General.Foreground", 0, 0, 0)

    # Export mesh image
    gmsh.write("figures/circular_waveguide.png")

    # Save mesh to file
    gmsh.write('circular_waveguide.msh')

    if DEBUG:
        # Visualize mesh
        gmsh.fltk.run()

    # Finalize Gmsh
    gmsh.finalize()

def generate_single_ridge_mesh(a, b, w, d, mesh_size):
    # Initialize Gmsh
    gmsh.initialize()
    # Print messages to console
    gmsh.option.setNumber("General.Terminal", 1)
    # Create model
    gmsh.model.add("single_ridge_waveguide")

    # Create points for waveguide corners
    gmsh.model.geo.addPoint(0, 0, 0, mesh_size, 1)
    gmsh.model.geo.addPoint(a, 0, 0, mesh_size, 2)
    gmsh.model.geo.addPoint(a, b, 0, mesh_size, 3)
    gmsh.model.geo.addPoint(a - (a - w) / 2, b, 0, mesh_size, 4)
    gmsh.model.geo.addPoint(a - (a - w) / 2, b - d, 0, mesh_size, 5)
    gmsh.model.geo.addPoint((a - w) / 2, b - d, 0, mesh_size, 6)
    gmsh.model.geo.addPoint((a - w) / 2, b, 0, mesh_size, 7)
    gmsh.model.geo.addPoint(0, b, 0, mesh_size, 8)

    # Connect points with lines
    gmsh.model.geo.addLine(1, 2, 1)
    gmsh.model.geo.addLine(2, 3, 2)
    gmsh.model.geo.addLine(3, 4, 3)
    gmsh.model.geo.addLine(4, 5, 4)
    gmsh.model.geo.addLine(5, 6, 5)
    gmsh.model.geo.addLine(6, 7, 6)
    gmsh.model.geo.addLine(7, 8, 7)
    gmsh.model.geo.addLine(8, 1, 8)

    # Define curve loop for surface
    gmsh.model.geo.addCurveLoop([1, 2, 3, 4, 5, 6, 7, 8], 1)

    # Create plane surface
    gmsh.model.geo.addPlaneSurface([1], 1)

    # Synchronize entities
    gmsh.model.geo.synchronize()

    # Define physical groups for PEC walls and surface
    gmsh.model.addPhysicalGroup(1, [1, 2, 3, 4, 5, 6, 7, 8], 1)
    gmsh.model.setPhysicalName(1, 1, "PEC")

    gmsh.model.addPhysicalGroup(2, [1], 2)
    gmsh.model.setPhysicalName(2, 2, "surface")

    # Generate mesh
    gmsh.model.mesh.generate(2)

    # Display surfaces and nodes
    gmsh.fltk.initialize()

    # Visualization options
    gmsh.option.setNumber("General.Axes", 1)
    gmsh.option.setColor("General.Background", 255, 255, 255)
    gmsh.option.setColor("General.Foreground", 0, 0, 0)

    # Export mesh image
    gmsh.write("figures/single_ridge_waveguide.png")

    # Save mesh to file
    gmsh.write('single_ridge_waveguide.msh')

    if DEBUG:
        # Visualize mesh
        gmsh.fltk.run()

    # Finalize Gmsh
    gmsh.finalize()

def generate_double_ridge_mesh(a, b, w, d, mesh_size):
    # Initialize Gmsh
    gmsh.initialize()
    # Print messages to console
    gmsh.option.setNumber("General.Terminal", 1)
    # Create model
    gmsh.model.add("double_ridge_waveguide")

    # Create points for waveguide corners
    gmsh.model.geo.addPoint(0, 0, 0, mesh_size, 1)
    gmsh.model.geo.addPoint((a - w) / 2, 0, 0, mesh_size, 2)
    gmsh.model.geo.addPoint((a - w) / 2, d, 0, mesh_size, 3)
    gmsh.model.geo.addPoint(a - (a - w) / 2, d, 0, mesh_size, 4)
    gmsh.model.geo.addPoint(a - (a - w) / 2, 0, 0, mesh_size, 5)
    gmsh.model.geo.addPoint(a, 0, 0, mesh_size, 6)
    gmsh.model.geo.addPoint(a, b, 0, mesh_size, 7)
    gmsh.model.geo.addPoint(a - (a - w) / 2, b, 0, mesh_size, 8)
    gmsh.model.geo.addPoint(a - (a - w) / 2, b - d, 0, mesh_size, 9)
    gmsh.model.geo.addPoint((a - w) / 2, b - d, 0, mesh_size, 10)
    gmsh.model.geo.addPoint((a - w) / 2, b, 0, mesh_size, 11)
    gmsh.model.geo.addPoint(0, b, 0, mesh_size, 12)

    # Connect points with lines
    gmsh.model.geo.addLine(1, 2, 1)
    gmsh.model.geo.addLine(2, 3, 2)
    gmsh.model.geo.addLine(3, 4, 3)
    gmsh.model.geo.addLine(4, 5, 4)
    gmsh.model.geo.addLine(5, 6, 5)
    gmsh.model.geo.addLine(6, 7, 6)
    gmsh.model.geo.addLine(7, 8, 7)
    gmsh.model.geo.addLine(8, 9, 8)
    gmsh.model.geo.addLine(9, 10, 9)
    gmsh.model.geo.addLine(10, 11, 10)
    gmsh.model.geo.addLine(11, 12, 11)
    gmsh.model.geo.addLine(12, 1, 12)

    # Define curve loop for surface
    gmsh.model.geo.addCurveLoop([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 1)

    # Create plane surface
    gmsh.model.geo.addPlaneSurface([1], 1)

    # Synchronize entities
    gmsh.model.geo.synchronize()

    # Define physical groups for PEC walls and surface
    gmsh.model.addPhysicalGroup(1, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 1)
    gmsh.model.setPhysicalName(1, 1, "PEC")

    gmsh.model.addPhysicalGroup(2, [1], 2)
    gmsh.model.setPhysicalName(2, 2, "surface")

    # Generate mesh
    gmsh.model.mesh.generate(2)

    # Display surfaces and nodes
    gmsh.fltk.initialize()

    # Visualization options
    gmsh.option.setNumber("General.Axes", 1)
    gmsh.option.setColor("General.Background", 255, 255, 255)
    gmsh.option.setColor("General.Foreground", 0, 0, 0)

    # Export mesh image
    gmsh.write("figures/double_ridge_waveguide.png")

    # Save mesh to file
    gmsh.write('double_ridge_waveguide.msh')

    if DEBUG:
        # Visualize mesh
        gmsh.fltk.run()

    # Finalize Gmsh
    gmsh.finalize()