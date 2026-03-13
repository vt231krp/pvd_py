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


# Algorithm for Embedding Data
def embed_pvd(p1, p2, secret_char):
    # Calculate initial difference
    d = abs(p2 - p1)

    # Determine interval and bits capacity
    l_k, _, n = get_interval(d)

    # Convert secret character to binary (8 bits) and take the first 'n' bits
    bin_char = format(ord(secret_char), "08b")
    secret_bits = bin_char[:n]

    # Convert those n bits to decimal
    b = int(secret_bits, 2)

    # Calculate new difference
    d_prime = l_k + b

    # Pixel Correction
    m = d_prime - d
    delta_p1 = math.floor(abs(m) / 2)
    delta_p2 = math.ceil(abs(m) / 2)

    # Apply conditions to distribute the changes safely
    if m == 0:
        p1_new, p2_new = p1, p2
    elif m > 0:
        if p2 >= p1:
            p1_new = p1 - delta_p1
            p2_new = p2 + delta_p2
        else:
            p1_new = p1 + delta_p1
            p2_new = p2 - delta_p2
    else:  # m < 0
        if p2 >= p1:
            p1_new = p1 + delta_p1
            p2_new = p2 - delta_p2
        else:
            p1_new = p1 - delta_p1
            p2_new = p2 + delta_p2

    # Ensure pixels stay within [0, 255] boundary
    p1_new = max(0, min(255, p1_new))
    p2_new = max(0, min(255, p2_new))

    return bin_char, secret_bits, p1_new, p2_new


# Algorithm for Extracting Data
def extract_pvd(p1_new, p2_new):
    # Calculate difference of the new pixels
    d_prime = abs(p2_new - p1_new)

    # Find which interval it belongs to
    l_k, _, n = get_interval(d_prime)

    # Extract the decimal value of the hidden bits
    b = d_prime - l_k

    # Convert back to binary (padded to n bits)
    extracted_bits = format(b, f"0{n}b")

    return extracted_bits


# Testing the Implementation
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
    ]

    for i, (p1, p2, char) in enumerate(test_cases, 1):
        # Embed
        full_bin, secret_bits, p1_new, p2_new = embed_pvd(p1, p2, char)

        # Extract to verify it works
        extracted = extract_pvd(p1_new, p2_new)

        # Print results matching the table in the manual
        print(
            f"{i:<5} | {p1:<4} {p2:<4} | {char:<4} | {full_bin:<10} | {secret_bits:<8} | {p1_new:<6} {p2_new:<6} | {extracted}"
        )


if __name__ == "__main__":
    run_tests()
