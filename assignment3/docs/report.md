# Assignment#3

2015004584, Bae Jiun

This is assignment#3 in **CSE4020** at Hanyang Univ.

## Implements

### Assignment

- [x] Manipulate the camera
  - [x] Rotation
  - [x] Zoom
- [x] Load obj file and render
  - [x] Drag and drop to load obj file
  - [x] Display mesh only using vertex position, normals and faces
  - [x] Toogle wireframe / solid mode by pressing Z key
  - [x] Print informations when open a new `.obj` file
- [x] Lighting
  - [x] Use multiple light sources

Additional Implements

- [x] Use `glDrawArrays` to render a mesh
- [x] Trianglize quad or polygons

### Lightings

I made a great class for lighting called **Light** on `lib/light.py`.  You can easily implement lighting as below, and up to 8 can be created depending on the support of OpenGL.

```
# register light instance
Light({
    'pos':      ( 1., 0., 0., 0.),
    'ambient':  ( .1, 0., 0., 1.),
    'diffuse':  ( 1., 0., 0., 1.),
    'specular': ( 1., 0., 0., 1.),
})

# render lights
Light.render()
```

In this assignments, there are 4 lights with position `(1, 0, 0,)`, `(0, 1, 0)`, `(0, 0, 1)` and `(-1, -1, -1)`. See L#24 at `main.py` for more detail.

### Object

Also, I made a class for object called **OBJ** which can read `.obj` file, trianglize it and render it. You can import object with one line as below.

```
# load .obj file and parse
obj = OBJ.read_obj(obj_file_path)

# render object
obj.render()
```

In this assignments, only one object without texcoord, but multiple size faces.

**OBJ** class has some *staticmehtods* for parsing and trianglize.

- ***`trianglize`***

  This implements based on `Seidel's algorithm` ([See also](http://gamma.cs.unc.edu/SEIDEL/)) using `numpy`.

- ***`read_obj`***

  Parses the `.obj` file to extract *vertex*, *normal*, *texcoords*, and *face* values. It call `trianglize` automatically to trianglize quad or polygon.

## Usage

### Requirements

Install dependency as below

```
pip install -r requirements.txt
```

or install directly.

- `PyOpenGL`
- `PyOpenGL-accelerate`
- `glfw`
- `numpy`

These are the basic libraries in the CSE4020. Most are pre-installed and do not need to be installed.

### Run

Run as below

```
python main.py
```

and drag and drop `.obj` file to look.

## Samples

![mercy](https://github.com/MaybeS/CSE4020/blob/master/assignment3/images/mercy.png?raw=true)

![tracer](https://github.com/MaybeS/CSE4020/blob/master/assignment3/images/tracer.png?raw=true)