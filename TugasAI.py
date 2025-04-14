import random
import math

# Konfigurasi GA
POPULATION_SIZE = 50
CHROMOSOME_LENGTH = 32  # 16 bit untuk x1, 16 bit untuk x2
GEN_MAX = 100
PC = 0.8  # Probabilitas crossover
PM = 0.01  # Probabilitas mutasi
X_MIN = -10
X_MAX = 10

# Fungsi konversi biner ke real
def binary_to_real(binary_str):
    """Decode binary string to real number in range [-10, 10]"""
    max_int = 2**len(binary_str) - 1
    int_value = int(binary_str, 2)
    real_value = X_MIN + (X_MAX - X_MIN) * int_value / max_int
    return real_value
