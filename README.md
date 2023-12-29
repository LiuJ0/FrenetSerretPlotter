### Frenet-Serret Plotter

A common topic of interest in calculus for parametric curves are the Frenet-Serret basis. (See [Wikipedia](https://en.wikipedia.org/wiki/Frenet%E2%80%93Serret_formulas)

This program plots a parametric curve and its Frenet-Serret basis to help visualize the concept. 

### Examples
#### Helix
Helices are curves with a constant Darboux vector. Therefore, the Frenet-Serret basis is a constant rotation in the same direction. 
To see this, use the function 
$$ \textbf{x}(t) = ( \cos(t), \sin(t), t )$$

#### Planar Curves
Curves that can be contained in a plane are planar. Therefore, the Binormal vector is constant.
To see this, plot a circle in the xy-plane (contained in the plane z = 1). 
$$ \textbf{x}(t) = ( \cos(t), \sin(t), 1 )$$

#### Parameterization
It can be shown that curvature and torsion are invariant under reparameterization. 
To explore this, observe that the functions 
$$ \textbf{x}(t) = ( \cos(t), \sin(t), t )$$
and 
$$ \textbf{x}(t) = ( \cos(t^3), \sin(t^3), t^3 )$$
Have identical curvature and torsion.

#### A detail about calculations
The standard formula for the Frenet-Serret basis are given by 
$$ \textbf{T} = \frac{\textbf{x}'}{|\textbf{x}'|} $$
$$ \textbf{N} = \frac{\textbf{T}'}{|\textbf{T}'|} $$
$$ \textbf{B} = \textbf{T} \times \textbf{N} $$
The computation of the normal vector is particularly difficult because it requires the derivative of the tangent vector, which can become complicated. Therefore, an alternative formula is used:
$$ \textbf{N} = \frac{1}{\|\textbf{x}'' - (\textbf{x}'' \cdot \textbf{T}) \textbf{T}\|}\textbf{x}'' - (\textbf{x}'' \cdot \textbf{T}) \textbf{T} $$
