import math


def get_interval(d):
    intervals = [
        (0, 7, 3),
        (8, 15, 3),
        (16, 31, 4),
        (32, 63, 5),
        (64, 127, 6),
        (128, 255, 7),
    ]
    for l_k, u_k, n in intervals:
        if l_k <= d <= u_k:
            return l_k, u_k, n
    return None


def embed_pvd(p1, p2, secret_char):
    d = abs(p2 - p1)

    l_k, _, n = get_interval(d)

    bin_char = format(ord(secret_char), "08b")
    secret_bits = bin_char[:n]

    b = int(secret_bits, 2)

    d_prime = l_k + b

    m = d_prime - d
    delta_p1 = math.floor(abs(m) / 2)
    delta_p2 = math.ceil(abs(m) / 2)

    if m == 0:
        p1_new, p2_new = p1, p2
    elif m > 0:
        if p2 >= p1:
            p1_new = p1 - delta_p1
            p2_new = p2 + delta_p2
        else:
            p1_new = p1 + delta_p1
            p2_new = p2 - delta_p2
    else:
        if p2 >= p1:
            p1_new = p1 + delta_p1
            p2_new = p2 - delta_p2
        else:
            p1_new = p1 - delta_p1
            p2_new = p2 + delta_p2

    p1_new = max(0, min(255, p1_new))
    p2_new = max(0, min(255, p2_new))

    return bin_char, secret_bits, p1_new, p2_new


def extract_pvd(p1_new, p2_new):
    d_prime = abs(p2_new - p1_new)

    l_k, _, n = get_interval(d_prime)

    b = d_prime - l_k

    extracted_bits = format(b, f"0{n}b")

    return extracted_bits


def run_tests():
    print(
        f"{'Test':<5} | {'P1':<4} {'P2':<4} | {'Char':<4} | {'Bin (8-bit)':<10} | {'n bits':<8} | {'New P1':<6} {'New P2':<6} | {'Extracted'}"
    )
    print("-" * 85)

    test_cases = [
        (26, 30, "A"),
        (125, 100, "M"),
        (200, 254, "r"),
        (147, 235, "S"),
        (0, 200, "!"),
        (50, 50, "Z"),
        (10, 2, "b"),
        (31, 0, "C"),
        (95, 63, "~"),
        (255, 128, "k"),
        (255, 0, "?"),
        (1, 254, "9"),
        (240, 245, " "),
    ]

    for i, (p1, p2, char) in enumerate(test_cases, 1):
        full_bin, secret_bits, p1_new, p2_new = embed_pvd(p1, p2, char)

        extracted = extract_pvd(p1_new, p2_new)

        print(
            f"{i:<5} | {p1:<4} {p2:<4} | {char:<4} | {full_bin:<10} | {secret_bits:<8} | {p1_new:<6} {p2_new:<6} | {extracted}"
        )


def read_pixel(prompt):
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Please enter a valid integer.")
            continue

        if 0 <= value <= 255:
            return value

        print("Pixel value must be between 0 and 255.")


def read_single_char(prompt):
    while True:
        value = input(prompt)
        if len(value) == 1:
            return value
        print("Please enter exactly one character.")


def run_embed_interactive():
    print("\nEmbed using PVD")
    p1 = read_pixel("Enter P1 (0-255): ")
    p2 = read_pixel("Enter P2 (0-255): ")
    char = read_single_char("Enter one character to embed: ")

    full_bin, secret_bits, p1_new, p2_new = embed_pvd(p1, p2, char)

    print("\nResult")
    print(f"Character (8-bit): {full_bin}")
    print(f"Embedded bits:      {secret_bits}")
    print(f"New P1, P2:         {p1_new}, {p2_new}")


def run_extract_interactive():
    print("\nExtract using PVD")
    p1_new = read_pixel("Enter modified P1 (0-255): ")
    p2_new = read_pixel("Enter modified P2 (0-255): ")

    extracted_bits = extract_pvd(p1_new, p2_new)

    print("\nResult")
    print(f"Extracted bits: {extracted_bits}")


def show_menu():
    print("\nPVD Operations Menu")
    print("1. Run test cases")
    print("2. Embed one character")
    print("3. Extract bits")
    print("4. Exit")


def main():
    while True:
        show_menu()
        choice = input("Choose an operation (1-4): ").strip()

        if choice == "1":
            print()
            run_tests()
        elif choice == "2":
            run_embed_interactive()
        elif choice == "3":
            run_extract_interactive()
        elif choice == "4":
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
