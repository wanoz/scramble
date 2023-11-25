import math
from typing import List

# Encryption and decryption support functions
def char_position(letter):
    return ord(letter) - 97

def pos_to_char(pos):
    return chr(pos + 97)

# Encrypt list of texts
def encrypt(texts: List[str], mkey: str) -> List[str]:
    enc_mkey = []
    enc_salt = 0
    for i, c in enumerate(mkey):
        enc_mkey += [str(char_position(c) + int((math.e)**(i + 1)))]
        if (i + 1) % 2 == 0:
            enc_salt += 42*(i + 1)*math.log(i + 1, math.e)*char_position(c) # set salt
    enc_mkey = ''.join(enc_mkey[::-1])

    enc_texts = []
    for word in texts:
        enc_word = []
        for c in word:
            enc_word += [str(char_position(c) + int(enc_salt))] + ['x'] # add salt during encrypt
        enc_word = ''.join(enc_word + [enc_mkey])
        enc_texts.append(enc_word)

    # Encrypting list order
    idx = generate_sort_idx(enc_texts, enc_salt) # use salt for sort index generation
    enc_texts = encrypt_sort(enc_texts, idx)
        
    return enc_texts

# Decrypt list of encrypted texts
def decrypt(enc_texts: List[str], mkey: str) -> str:
    enc_mkey = []
    enc_salt = 0
    for i, c in enumerate(mkey):
        enc_mkey += [str(char_position(c) + int((math.e)**(i + 1)))]
        if (i + 1) % 2 == 0:
            enc_salt += 42*(i + 1)*math.log(i + 1, math.e)*char_position(c) # set salt
    enc_mkey = ''.join(enc_mkey[::-1])
    
    # Decrypting list order
    idx = generate_sort_idx(enc_texts, enc_salt) # use salt for sort index generation
    enc_texts = decrypt_sort(enc_texts, idx)

    texts = []
    for enc_word in enc_texts:
        enc_word = enc_word.replace(enc_mkey, '')
        enc_word = [c for c in enc_word.split('x') if c != '']
        word = []
        for n in enc_word:
            word += [str(pos_to_char(int(n) - int(enc_salt)))] # remove salt during decrypt
        
        texts.append(''.join(word))
        
    return texts

# Generate sort index for encrypt and decrypt
def generate_sort_idx(input_list: List[str], n: int) -> List[int]:
    if len(str(int(n))) < len(input_list):
        n = 1234567654321*int(n) 
    idx = [i for i in str(n)[-len(input_list):]]
    return idx

# Encrypt list order
def encrypt_sort(input_list: List[str], idx: List[int]) -> List[str]:
    idx_sort = sorted(range(len(idx)), key=idx.__getitem__)
    output_list = [input_list[i] for i in idx_sort]
    return output_list

# Decrypt list order
def decrypt_sort(input_list: List[str], idx: List[int]) -> List[str]:
    idx_sort = sorted(range(len(idx)), key=idx.__getitem__)
    output_ori_map = {i:input_list[pos] for pos, i in enumerate(idx_sort)}
    output_list = [output_ori_map[k] for k in sorted(output_ori_map)]
    return output_list

# Execute main script
if __name__ == '__main__':
    while True:
        mode = input('\nSelect from options: Encrypt from txt file (0), Encrypt (1), Decrypt (2), Exit (3): ')
        options = ['0', '1', '2', '3']
        options_msg = ', '.join(options[:-1]) + f"or {options[-1]}"
        if mode in options:
            break
        else:
            print(f"Please enter either {options_msg} based on selection options.")

    # Encryption of texts from txt file
    if mode == '0':
        while True:
            mkey = input('\nSet master key: ')
            
            if len(mkey) >= 4:
                break
            else:
                print('Please set a master key that contains at least 4 characters.')

        while True:
            filename = input('Enter the name of the txt file: ')
            texts = []
            if not filename.endswith('.txt'):
                filename = f"{filename}.txt"
            try:
                with open(f"{filename}", 'r') as f:
                    texts = [text for text in f]
                break
            except:
                print('Cannot locate and/or read input txt file.')

        # Encrypting
        enc_texts = encrypt(texts, mkey)
        check_texts = decrypt(enc_texts, mkey)

        # Check encrypt and decrypt function
        try: 
            assert check_texts == texts
            print('No issues encountered.')
        except AssertionError:
            print('Issue encountered during encrypt and decrypt process!')
            
        # Save file
        with open('enc_keys.txt','w') as f:
            f.write('\n'.join(enc_texts))
        print('Task completed\n')

    # Encryption of texts
    if mode == '1':
        while True:
            mkey = input('\nSet master key: ')
            
            if len(mkey) >= 4:
                break
            else:
                print('Please set a master key that contains at least 4 characters.')

        while True:
            texts = input('Enter texts to encrypt (note: each text is separated by comma): ')

            if len(texts) >= 4:
                texts = texts.replace(' ', '')
                texts = texts.split(',')
                break
            else:
                print('Please enter texts that contain at least 4 characters')

        # Encrypting
        enc_texts = encrypt(texts, mkey)
        check_texts = decrypt(enc_texts, mkey)

        # Check encrypt and decrypt function
        try: 
            assert check_texts == texts
            print('No issues encountered.')
        except AssertionError:
            print('Issue encountered during encrypt and decrypt process!')
            
        # Save file
        with open('enc_keys.txt','w') as f:
            f.write('\n'.join(enc_texts))
        print('Task completed\n')

    # Decryption of texts
    elif mode == '2':
        while True:
            mkey = input('\nPlease enter master key: ')
            
            if len(mkey) >= 4:
                break
            else:
                print('Please enter a master key that contains at least 4 characters.')

        # Load encrypted file
        file_read = False
        try:
            enc_texts = []
            with open('enc_keys.txt', 'r') as f:
                lines = f.readlines()
                for enc_word in lines:
                    enc_texts.append(enc_word.replace('\n', ''))
            file_read = True
        except:
            print('Fail to read encrypted file (note: the required file is named "enc_keys.txt")]n')

        # Decrypting
        decrypt_successful = False
        if file_read:
            try:
                texts = decrypt(enc_texts, mkey)
                for word in texts:
                    for c in word:
                        idx = char_position(c)
                        if idx > 25:
                            raise ValueError
                decrypt_successful = True
            except:
                print('Decryption failed. Please ensure encrypted contents and/or master key are valid\n')

        if decrypt_successful:
            print('\nDecrypted results:')
            texts = [f'{str(i + 1)}. {w}\n' for i, w in enumerate(texts)]
            # print(char_position(texts[0][-1]))
            texts = ''.join(texts)
            print(texts)
            print('Task completed\n')
    else:
        print('')

