from mnemonic import Mnemonic

def generate_mnemonic(length=24):
    mnemo = Mnemonic("english")
    return mnemo.generate(strength=256)

if __name__ == "__main__":
    # Prompt for the number of mnemonics to generate
    num_mnemonics = int(input("Enter the number of mnemonics to generate: "))
    
    for i in range(1, num_mnemonics + 1):
        mnemonic = generate_mnemonic(length=24)
        filename = f"mnemonic{i}.txt"
        with open(filename, 'w') as f:
            f.write(mnemonic)
        print(f"Mnemonic {i}: {mnemonic} (saved to {filename})")
