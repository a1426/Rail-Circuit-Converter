from PIL import Image

def single_square_gates(img):
    im=Image.open(img)
    width, height = im.size
    #Forces RGB rather than RGBA
    im=im.convert("RGB")
    #A rather crude aproach, we look for the non-greyscale colors in the image.
    #We must use a .png file, as artifacts can throw this approach off.
    min_y,max_y=height,0
    previously_colored=False
    x_ranges=[]
    for x in range(width):
        colored_column=False
        for y in range(height):
            r,g,b=im.getpixel((x,y))
            if(r==g==b):
                continue
            #Since the gates will all be on a single line, we can assume that all have the same minimum and maximum.
            if(y<min_y):
                min_y=y
            if(y>max_y):
                max_y=y
            colored_column=True
        if(colored_column and not previously_colored):
                x_ranges.append([x])
        if(previously_colored and not colored_column):
            x_ranges[-1].append(x)
        previously_colored=colored_column
    return (x_ranges,min_y,max_y,width,height)

def measure_gates(img):
    im=Image.open(img)
    width, height = im.size
    #Forces RGB rather than RGBA
    im=im.convert("RGB")
    #Here, we check for the rightmost occurence of 168,168,168, the color of the measurement gate, since we know it is at the end.
    detected=False
    for x in range(width-1,0,-1):
        for y in range(height):
            r,g,b=im.getpixel((x,y))
            if(r==g==b==168):
                max_x=min_x=x
                min_y=max_y=y
                detected=True
                break
        if detected:
            break
    while(True):
        r,g,b=im.getpixel((min_x,min_y))
        if(r==g==b==168):
            min_x-=1
        else: break
    while(True):
        r,g,b=im.getpixel((max_x,max_y))
        if(r==g==b==168):
            max_y+=1
        else: break        
    return (min_x,max_x,min_y,max_y,width,height)
