## Frenet-Serret Plotter

A common topic of interest in calculus for parametric curves are the Frenet-Serret basis. (See [Wikipedia](https://en.wikipedia.org/wiki/Frenet%E2%80%93Serret_formulas))

This program plots a parametric curve and its Frenet-Serret basis to help visualize the concept. 

### Usage

```
python frenet_serret_plotter.py
```
Options: 
* -h, --help: show help message and exit
* --x X: x component of the parametric curve, in LaTeX format
* --y Y: y component of the parametric curve, in LaTeX format
* --z Z: z component of the parametric curve, in LaTeX format
* --start START: start of the parametric curve
* --end END: end of the parametric curve

This will plot the curve given by (x(t), y(t), z(t)) for $t \in [\text{start}, \text{end}]$. 

An important note: If any of your arguments contain a leading hyphen (-), you should put a space in front. For example, the curve 
$$ \textbf{x}(t) = ( -\cos(t), \sin(t), t )$$
should be entered as 
```
python frenet_serret_plotter.py --x " -\cos{t}" --y "\sin{t}" --z "t" --start 0 --end "2\pi"
                                     ^
```

### Examples
#### Helix
Helices are curves with a constant curvature and torsion. 
To see this, run 
```
python frenet_serret_plotter.py --x "\cos{t}" --y "\sin{t}" --z "t" --start 0 --end "2\pi"
```
which plots the function
$$ \textbf{x}(t) = ( \cos(t), \sin(t), t  )$$

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
