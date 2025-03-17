import math
class Function:

    @staticmethod
    def rastrigin(valores:list[float]):
        A = 10.0
        dimension = len(valores)
        return A * dimension + sum([(xi**2 - A * math.cos(2 * math.pi * xi)) for xi in valores])

    @staticmethod
    def schwefel(valores):
        dimension = len(valores)
        return 418.9829 * dimension - sum([xi * math.sin(math.sqrt(abs(xi))) for xi in valores])

    @staticmethod
    def michalewicz( valores):
        dimension = len(valores)
        
        m = 10.0
        return -sum([math.sin(xi) * math.sin(i * xi**2 / math.pi)**(2 * m) for i, xi in enumerate(valores, 1)])



    @staticmethod
    def levy( valores):
        dimension = len(valores)
        
        w = [(1 + (xi - 1) / 4) for xi in valores]
        term1 = math.sin(math.pi * w[0])**2
        term3 = (w[-1] - 1)**2 * (1 + math.sin(2 * math.pi * w[-1])**2)
        sum_term = sum([(wi - 1)**2 * (1 + 10 * math.sin(math.pi * wi + 1)**2) for wi in w[:-1]])
        
        return term1 + sum_term + term3

    @staticmethod
    def zakharov(  valores):
        dimension = len(valores)
        
        sum1 = sum([xi**2 for xi in valores])
        sum2 = sum([0.5 * i * xi for i, xi in enumerate(valores, 1)])
        
        return sum1 + sum2**2 + sum2**4


    @staticmethod
    def sphere( valores):
        dimension = len(valores)
        
        # La función Sphere es simplemente la suma de los cuadrados de los valores.
        return sum([xi**2 for xi in valores])

    @staticmethod
    def ackley(valores):
        dimension = len(valores)
        
        a = 20
        b = 0.2
        c = 2 * math.pi
        sum1 = sum([xi**2 for xi in valores]) / dimension
        sum2 = sum([math.cos(c * xi) for xi in valores]) / dimension
        
        return -a * math.exp(-b * math.sqrt(sum1)) - math.exp(sum2) + a + math.e

    @staticmethod
    def griewank( valores):
        dimension = len(valores)
        
        sum_part = sum([xi**2 / 4000 for xi in valores])
        prod_part = math.prod([math.cos(xi / math.sqrt(i+1)) for i, xi in enumerate(valores)])
        
        return sum_part - prod_part + 1

    @staticmethod
    def rosenbrock( valores):
        dimension = len(valores)
        return sum([100 * (valores[i+1] - valores[i]**2)**2 + (1 - valores[i])**2 for i in range(dimension - 1)])


    @staticmethod 
    def prueba (valores):
        dimension = len(valores)
        a = 0
        for x in valores:
            a += x
        return a