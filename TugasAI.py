import random
import math

# Konfigurasi GA
POPULATION_SIZE = 32
CHROMOSOME_LENGTH = 8  # 4 bit untuk x1, 4 bit untuk x2
GEN_MAX = 100
PC = 0.8  # Probabilitas crossover
PM = 0.3  # Probabilitas mutasi
X_MIN = -10
X_MAX = 10

# Fungsi konversi biner ke real sesuai domain
def representasi_biner(binary_str):
    
    N = len(binary_str)
    a = 0.0 #permisalan untuk 
    b = sum([2 ** -(i + 1) for i in range(N)])

    for i, bit in enumerate(binary_str):
        count = 2 ** -(i + 1)
        a += int(bit) * count

    hasilAB = a / b
    x = X_MIN + (X_MAX - X_MIN) * hasilAB
    return x

# Fungsi fitness
def objective_function(x1, x2):
    try:
        value = - (math.sin(x1) * math.cos(x2) * math.tan(x1 + x2) +
                   (3/4) * math.exp(1 - math.sqrt(x1**2)))
        return value
    except:
        return float('inf')  # jika error karena tan(x1+x2) undefined

#inisialisasi populasi
def generate_chromosome():
    return ''.join(random.choice('01') for _ in range(CHROMOSOME_LENGTH))

def initialize_population():
    return [generate_chromosome() for _ in range(POPULATION_SIZE)]


# dekode biner ke real dan hitung fitness
def decode(chromosome):
    #Memecah kromosom jadi dua bagian (x1 dan x2), lalu konversi ke nilai real.
    
    mid = len(chromosome) // 2
    x1_bits = chromosome[:mid]
    x2_bits = chromosome[mid:]

    x1 = representasi_biner(x1_bits)
    x2 = representasi_biner(x2_bits)

    return x1, x2

# menghitung fungsi fitness
def fitness(chromosome):
    x1, x2 = decode(chromosome)
    return objective_function(x1, x2)

# seleksi orang tua (Roulette wheel)
def selection(population):
    fitnesses = [1 / (1 + abs(fitness(ch)) + 1e-6) for ch in population]
    total_fit = sum(fitnesses)
    probs = [f / total_fit for f in fitnesses]
    selected = random.choices(population, weights=probs, k=2)
    return selected

# crossover (1 point crossover)
def crossover(parent1, parent2):
    # Cek apakah crossover akan dilakukan berdasarkan probabilitas PC
    if random.random() <= PC:
        # Tentukan titik potong (crossover point) secara acak
        titik_silang = random.randint(1, CHROMOSOME_LENGTH - 1)

        # Buat dua anak hasil crossover
        anak1 = parent1[:titik_silang] + parent2[titik_silang:]
        anak2 = parent2[:titik_silang] + parent1[titik_silang:]

        return anak1, anak2
    else:
        # Jika tidak dilakukan crossover, anak = parent asli
        return parent1, parent2


# mutasi
def mutasi(chromosome):
    # Inisialisasi string baru untuk menyimpan hasil mutasi
    hasil_mutasi = ""

    # Iterasi setiap bit dalam kromosom
    for bit in chromosome:
        # Jika nilai random lebih besar dari PM, bit tidak berubah
        if random.random() > PM:
            hasil_mutasi += bit
        else:
            # Bit '0' menjadi '1', dan bit '1' menjadi '0'
            if bit == '0':
                hasil_mutasi += '1'
            else:
                hasil_mutasi += '0'

    return hasil_mutasi


# evolusi populasi
def evolve(population):
    new_population = []
    while len(new_population) < POPULATION_SIZE:
        p1, p2 = selection(population)
        c1, c2 = crossover(p1, p2)
        c1, c2 = mutasi(c1), mutasi(c2)
        new_population.extend([c1, c2])
    return new_population[:POPULATION_SIZE]

# mendapatkan kromosom terbaik dari populasi
def get_best(population):
    best = min(population, key=fitness)
    x1, x2 = decode(best)
    f_val = fitness(best)
    return best, x1, x2, f_val

# Main
def main():
    population = initialize_population()
    best_overall = None

    print("=== Proses Evolusi ===")
    for gen in range(GEN_MAX):
        population = evolve(population)
        current_best = get_best(population)

        if best_overall is None or current_best[3] < best_overall[3]:
            best_overall = current_best

        print(f"Generasi {gen + 1:3}: Fitness terbaik = {current_best[3]:.5f}")

    print("\n=== Hasil Akhir ===")
    print(f"Kromosom terbaik: {best_overall[0]}")
    print(f"x1 = {best_overall[1]:.5f}, x2 = {best_overall[2]:.5f}")
    print(f"Nilai f(x1, x2) = {best_overall[3]:.5f}")

if __name__ == "__main__":
    main()
