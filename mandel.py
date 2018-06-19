def mandelbrot(x, y):
    maxiter = 255
    mult_factor = 5
    z = complex(x, y)
    c = z
    for n in range(maxiter):
        if abs(z) > 2:
            return n / maxiter
        z = z*z + c
    return 0
