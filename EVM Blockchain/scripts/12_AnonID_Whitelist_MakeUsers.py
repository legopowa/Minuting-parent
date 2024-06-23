from mnemonic import Mnemonic

def generate_mnemonic(length=24):
    mnemo = Mnemonic("english")
    return mnemo.generate(strength=256)

def main():
    num_mnemonics = 3  # Fixed to generate three mnemonics

    for i in range(1, num_mnemonics + 1):
        mnemonic = generate_mnemonic(length=24)
        filename = f"mnemonic{i}.txt"
        with open(filename, 'w') as f:
            f.write(mnemonic)
        print(f"Mnemonic {i}: {mnemonic} (saved to {filename})")
