from Bio import SeqIO
from Bio.Align.Applications import MafftCommandline


class Probe:
    def __init__(self, probe, seq_of_probe, end_seq_id, position, is_forward):
        self.probe = probe
        self.seq_of_probe = seq_of_probe

        self.end_seq_id = end_seq_id
        self.position = position

        if is_forward:
            self.start_seq_id = self.seq_of_probe
        else:
            self.start_seq_id = 0

    def __str__(self):
        return "Probe: " + self.probe + "\n" \
            + "Probe taken from seq with id: " + str(self.seq_of_probe) + "\n" \
            + "Probe is valid for sequences with ids: [" + str(self.start_seq_id) + "; " + str(self.end_seq_id) + "]\n" \
            + "Start position: " + str(self.position) + "\n"

    def interval(self):
        return self.start_seq_id, self.end_seq_id


def get_seqs(filepath):
    seq_records = SeqIO.parse(filepath, format="fasta")
    seqs = []
    for seq_record in seq_records:
        seqs.append(seq_record)

    return seqs


def longest_seq_count(seq_records, name):
    name = name.lower()
    longest = -1
    seqs = []
    for seq in seq_records:
        if name not in seq.description.lower():
            continue
        seqs.append(seq)

    for seq in seqs:
        seq_length = len(seq)
        longest = seq_length if seq_length > longest else longest
    return seqs, longest


def filter_seq_by_length_and_name(seq_records, name, percent):
    seqs, longest = longest_seq_count(seq_records, name)
    lowest_allowed_length = (longest * percent) / 100

    filtered = filter(lambda seq: len(seq) >= lowest_allowed_length, seqs)
    return filtered


def realign_with_mafft(filepath):
    mafft_path = "mafft/mafft.bat"
    output_path = "Resources/mafft_realigned.fasta"
    mafft_cline = MafftCommandline(cmd=mafft_path, input=filepath, thread=8, reorder=True)

    stdout, stderr = mafft_cline()
    with open(output_path, "w") as handle:
        handle.write(stdout)

    return output_path


def filter_and_realign(filepath):
    seq_records = SeqIO.parse(filepath, format="fasta")
    seq_records = filter_seq_by_length_and_name(seq_records, name="Bat", percent=80)

    filtered_path = "Resources/longer_than_80_percent_of_the_longest.fasta"
    SeqIO.write(seq_records, filtered_path, "fasta")

    return realign_with_mafft("Resources/longer_than_80_percent_of_the_longest.fasta")


def get_initial_probe(seq, fragment_size):
    count = 0
    initial_probe = []
    last_index = 0
    for base_pair in seq:
        last_index += 1
        if count >= fragment_size:
            break
        if base_pair == '-':
            continue
        initial_probe.append(base_pair)
        count += 1

    return "".join(initial_probe), last_index


def get_next_probe_symbol(seq, probe, index):
    seq_length = len(seq)
    new_probe = probe[1:]

    while index < seq_length:
        base_pair = seq[index]
        index += 1
        if base_pair == '-':
            continue

        new_probe += base_pair
        break

    return new_probe, index


def match_and_adjust_probe(seq, probe):
    max_mismatches = 3
    mismatches = 0
    i = 5
    j = 5
    seq_length = len(seq)
    probe_length = len(probe)

    if seq_length <= 5 or seq[0:5] != probe[0:5]:
        return None

    while i < probe_length and j < seq_length:
        if mismatches > max_mismatches:
            return probe[0:(i-1)]

        base_pair = seq[j]

        if base_pair == '-':
            j += 1
            continue

        if base_pair != probe[i]:
            mismatches += 1

        i += 1
        j += 1

    return probe[0:i]


def insert_probe(probes, probe):

    # for p in probes:
    #     if p.start_seq_id <= probe.start_seq_id and \
    #        p.end_seq_id >= probe.end_seq_id:
    #         return
    probes.append(probe)


def get_probes(seq_records, only_forward):
    fragment_size = 80
    probes = []

    seq_id = 0
    records_count = len(seq_records)

    while seq_id < records_count:
        seq = seq_records[seq_id].seq
        seq_length = len(seq)

        i = 0
        last_valid_probe = None

        initial_probe, last_index = get_initial_probe(seq, fragment_size)

        last_best_probe = None

        while last_index < seq_length:
            probe = initial_probe

            other_seq_id = seq_id + 1 if only_forward else 0
            while other_seq_id < records_count:
                other_seq = seq_records[other_seq_id].seq
                probe = match_and_adjust_probe(other_seq[i:], probe)

                if probe is None:
                    break
                else:
                    last_valid_probe = Probe(probe, seq_id, other_seq_id, i, only_forward)

                other_seq_id += 1

            if last_valid_probe is not None:
                if last_best_probe is None:
                    last_best_probe = last_valid_probe
                else:
                    if last_best_probe.end_seq_id <= last_valid_probe.end_seq_id:
                        last_best_probe = last_valid_probe
                    elif len(last_best_probe.probe) < len(last_valid_probe.probe):
                        last_best_probe = last_valid_probe

            initial_probe, last_index = get_next_probe_symbol(seq, initial_probe, last_index)
            i += 1

        seq_id += 1
        if last_best_probe is not None:
            insert_probe(probes, last_best_probe)

    return probes


def find_minimal_set(probes, target):
    probes.sort(key=lambda p: p.start_seq_id)
    filtered = probes.copy()

    for p1 in probes:
        for p2 in probes:
            if p1 != p2 and \
               p1.start_seq_id <= p2.start_seq_id and \
               p1.end_seq_id >= p2.end_seq_id:
                if p2 in filtered:
                    filtered.remove(p2)

    solution = [filtered[0]]
    filtered_length = len(filtered)
    i = 0
    while i < filtered_length:
        p1 = filtered[i]

        j = i + 1
        minimal = p1.end_seq_id
        largest = 1
        best_match_id = None
        while j < filtered_length:
            p2 = filtered[j]
            if p2.start_seq_id <= minimal and (p2.end_seq_id - p2.start_seq_id) > largest:
                largest = p2.end_seq_id - p2.start_seq_id
                best_match_id = j
            j += 1

        if best_match_id is None:
            solution.append(filtered[i])
            i += 1
        else:
            solution.append(filtered[best_match_id])
            i = best_match_id + 1

    return solution


def main():
    realigned_path = filter_and_realign("Resources/input.fasta")

    seq_records = get_seqs(realigned_path)
    probes = get_probes(seq_records, only_forward=True) + get_probes(seq_records, only_forward=False)
    filtered = find_minimal_set(probes, (0, len(seq_records) - 1))

    print("Minimal set ouf probes: \n\n")
    for probe in filtered:
        print(probe)


if __name__ == '__main__':
    main()


