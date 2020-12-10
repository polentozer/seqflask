def fasta_parser(handle):
    '''Parser for fasta sequences.'''
    stream = handle.split()
    sequences = []

    for line in stream:
        if line[0] == '>':
            seq_name = line[1:].strip()
            break
    else:
        return sequences

    temp = []
    for line in stream:
        if line[0] == '>':
            if temp:
                sequences.append((seq_name, "".join(temp)))
            seq_name = line[1:].strip()
            temp = []
            continue
        else:
            temp.append(line.strip().upper())
    else:
        sequences.append((seq_name, "".join(temp)))
    
    # logger.info(f'Input {len(sequences)} sequences...')

    return sequences
