from qiskit import QuantumCircuit
import random
from gate_finder import single_square_gates,measure_gates
import yaml
import matplotlib.pyplot as plt
from math import pi
with open("datasets/square_dataset/data.yaml") as file:
    try:
        names=yaml.safe_load(file)["names"]
    except yaml.YAMLError as e:
        print(e)

#Creates a quantum circuit consisting of 10 gates
class Simple_Square_Gates:
    def __init__(self):
        self.circuit=QuantumCircuit(1)
        self.gates=[]
        for x in range(10):
            #Here, I to apply random gates based on names from the file. TODO: Using eval is dangerous.
            method=eval("self.circuit."+random.choice(list(names.values())))
            args=[]
            #Note: 1 argument is the qubit, the other is the self???
            for x in range(method.__code__.co_argcount - (0 if method.__defaults__ is None else len(method.__defaults__))-2):
                a=random.uniform(-1,1000)
                if(a<0):
                    a=pi/random.randint(2,10)
                args.append(a)
            method(*args,0)
            self.gates.append(method.__name__)
    def export(self, path, validate=False):
        #Determines whether to export the figure to the training or validation directory.
        spl="train" if not validate else "val"
        #Generates the image.
        self.circuit.draw(output="mpl")
        plt.savefig(f"datasets/square_dataset/images/{spl}/{path}.png")
        plt.close()
        #Generates the labels.
        with open(f"datasets/square_dataset/labels/{spl}/{path}.txt","w") as file:
            widths,min_y,max_y,w,h=single_square_gates(f"datasets/square_dataset/images/{spl}/{path}.png")
            for x in range(10):
                #Label Format: Gate Name, 
                file.write(f"{next(k for k, v in names.items() if v == self.gates[x])} {(widths[x][1]+widths[x][0])/(2*w)} {(min_y+max_y)/(2*h)} {(widths[x][1]-widths[x][0])/w} {(max_y-min_y)/h}\n")

#Designed to generate quantum circuits to train the AI about measurement gates.
class Measure_Gate:
    def __init__(self):
        self.circuit= QuantumCircuit(1)
        args=[]
        method=eval("self.circuit."+random.choice(list(names.values())))
        #For now, just copied from the other function. I will make this pythonic after I verify it works.
        for _ in range(method.__code__.co_argcount - (0 if method.__defaults__ is None else len(method.__defaults__))-2):
            a=random.uniform(-1,1000)
            if(a<0):
                a=pi/random.randint(2,10)
            args.append(a)
        method(*args,0)
        self.circuit.measure_all()
    def export(self, path, validate=False):
        #Determines whether to export the figure to the training or validation directory.
        spl="train" if not validate else "val"
        #Generates the image.
        self.circuit.draw(output="mpl")
        plt.savefig(f"datasets/measure_dataset/images/{spl}/{path}.png")
        plt.close()
        #Generates the labels.
        with open(f"datasets/measure_dataset/labels/{spl}/{path}.txt","w") as file:
            min_x,max_x,min_y,max_y,w,h=measure_gates(f"datasets/measure_dataset/images/{spl}/{path}.png")
            file.write(f"0 {(min_x+max_x)/(2*w)} {(min_y+max_y)/(2*h)} {(max_x-min_x)/w} {(max_y-min_y)/h}\n")
            
def generate(class_name, num, split, start1=0,start2=0):
    for x in range(int(num*split)):
        class_name().export(str(x+start1))
    for x in range(int(num*(1-split))):
        class_name().export(str(x+start2), True)
