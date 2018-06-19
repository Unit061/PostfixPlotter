import math
from PIL import Image
from RpnCalc import *


def make_plot_rpn(rpn_expr, width=400, height=400, fp='temp.png'):
    """Create a single band image from an rpn function with variables [x, y] based on relative pixel locations
    rpn_expr -- expression given in postfix notation to be plotted
    """
    xmin = -1.0
    xmax = 1.0
    ymin = -1.0
    ymax = 1.0
    x_units_per_px = (xmax - xmin) / width
    y_units_per_px = (ymax - ymin) / height

    canvas = Image.new('L', (width, height), 'white')
    pixels = canvas.load()

    for i in range(width * height):
        px_x = i % width
        px_y = i // width

        if px_x == 0:
            print(str(100.0 * px_y / height) + "% done")

        x = xmin + px_x * x_units_per_px
        y = ymin + px_y * y_units_per_px

        variables = {'x':x, 'y':y, 'pi':math.pi}
        value = rpn(rpn_expr, variables)
        value = int(127.5 + 127.5 * value)  # Convert from [-1, 1] to [0, 255]
        value = min(255, max(0, value))  # Filter out of range results
        pixels[px_x, px_y] = value

    canvas.save(fp)
    return canvas


def rand_rpn_plots(num_pics, width=400, height=400, p_nest=.95, fp=""):
    """Generate and save a batch of images constructed from randomly generated layers in several color modes 
    """
    for i in range(num_pics):
        layers = []
        exprs = []
        for band in range(4):  # 4 layers for each of the color modes including cmyk
            expr = random_rpn_expr(p_nest)
            exprs.append(expr)
            this_fp = fp + "{}_{}.png".format(i, band)
            layer = make_plot_rpn(expr, width, height, this_fp)
            layers.append(layer)
            with open(fp+'log.txt', 'a') as log:
                log.write("{} : {} \n".format(this_fp, exprs[band]))

        # Render each image in different color spaces
        modes = ['RGB', 'HSV', 'YCbCr', 'CMYK']
        for m in range(len(modes)):
            mode = modes[m]
            if mode == 'CMYK':
                img = Image.merge(mode, layers[0:4])
            else:
                img = Image.merge(mode, layers[0:3])
            img = img.convert('RGB')  # Convert to save as png
            img.save("{}{}{}.jpg".format(fp, i, mode))


def custom_plot():
  """Generate a plot in a given color scheme from given RPN expressions
  """
  mode = input('Type a color mode: [HSV, RGB, CMYK, YCbCr]')
  num_bands = int(input('How many color bands is that?'))
  width = int(input('Width?'))
  height = int(input('Height?'))
  fp = input("Filepath? (Don't include extension)") + ".jpg"
  exprs = []
  for i in range(num_bands):
    expr = input('Enter band #{}'.format(i))
    exprs.append(expr)
    
  layers = []
  for expr in exprs:
    print(expr)
    layer = make_plot_rpn(expr, width, height)
    layers.append(layer)
  img = Image.merge(mode, layers)
  img.show()
  img.save(fp)
  print(exprs)
