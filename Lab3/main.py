from Bio import SeqIO
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
from tabulate import tabulate
import matplotlib.pyplot as plot


def check_phred33(encodings, ascii_code):
    if ascii_code > 73 or ascii_code < 33:
        encodings["Phred+33"] = False


def check_solexa64(encodings, ascii_code):
    if ascii_code > 104 or ascii_code < 59:
        encodings["Solexa+64"] = False


def check_illumina13(encodings, ascii_code):
    if ascii_code > 104 or ascii_code < 64:
        encodings["Illumina1.3"] = False


def check_illumina15(encodings, ascii_code):
    if ascii_code > 105 or ascii_code < 66:
        encodings["Illumina1.5"] = False


def check_illumina18(encodings, ascii_code):
    if ascii_code > 74 or ascii_code < 33:
        encodings["Illumina1.8"] = False


def check_encodings(line, encodings):
    for symbol in line:
        ascii_code = ord(symbol)
        check_phred33(encodings, ascii_code)
        check_solexa64(encodings, ascii_code)
        check_illumina13(encodings, ascii_code)
        check_illumina15(encodings, ascii_code)
        check_illumina18(encodings, ascii_code)


def print_encodings(filepath):
    encodings = {
        "Phred+33": True,
        "Solexa+64": True,
        "Illumina1.3": True,
        "Illumina1.5": True,
        "Illumina1.8": True
    }

    file = open(filepath, "r")
    lines = file.read().splitlines()

    process = False
    for line in lines:
        if line == "+":
            process = True
            continue
        elif process:
            process = False
            check_encodings(line, encodings)

    print("Possible encodings:")
    for key in encodings:
        if encodings[key]:
            print(key)


def print_gc_plot(x_axis, y_axis):
    plot.plot(x_axis, y_axis)
    plot.ylabel('Reads count')
    plot.xlabel('G/C percentage (%)')
    plot.show()


def get_gc_ratio(seq):
    gc_count = seq.count("G") + seq.count("C")
    return round(gc_count / len(seq), 2)


def get_gc_axis(seq_records):
    x_axis = []
    y_axis = []
    gc_ratios = []

    for seq_record in seq_records:
        gc_ratio = get_gc_ratio(seq_record.seq)
        gc_ratios.append(gc_ratio)

    for i in range(0, 100):
        probability = i / 100
        y_axis.append(gc_ratios.count(probability))
    for i in range(0, 100):
        x_axis.append(i)

    return x_axis, y_axis


def get_peaks(x_axis, y_axis):
    return x_axis[25:40][y_axis[25:40].index(max(y_axis[25:40]))]/100,\
           x_axis[45:55][y_axis[45:55].index(max(y_axis[45:55]))]/100,\
           x_axis[60:80][y_axis[60:80].index(max(y_axis[60:80]))]/100


def get_peak_sequences(seq_records, x_axis, y_axis):
    peak1, peak2, peak3 = get_peaks(x_axis, y_axis)
    peak1_seqs = []
    peak2_seqs = []
    peak3_seqs = []

    p1_has_five, p2_has_five, p3_has_five = False, False, False

    for seq_record in seq_records:
        if p1_has_five and p2_has_five and p3_has_five:
            break

        gc_ratio = get_gc_ratio(seq_record.seq)

        if gc_ratio == peak1 and not p1_has_five:
            peak1_seqs.append(seq_record)
            p1_has_five = len(peak1_seqs) == 5
        elif gc_ratio == peak2 and not p2_has_five:
            peak2_seqs.append(seq_record)
            p2_has_five = len(peak2_seqs) == 5
        elif gc_ratio == peak3 and not p3_has_five:
            peak3_seqs.append(seq_record)
            p3_has_five = len(peak3_seqs) == 5

    return peak1_seqs, peak2_seqs, peak3_seqs


def print_seq_ids(seq_record):
    for seq_record in seq_record:
        print(seq_record.id)


def print_peak_seqs_ids(peak1_records, peak2_records, peak3_records):
    print("Sequence ids for 1st sequence:")
    print_seq_ids(peak1_records)
    print("Sequence ids for 2nd sequence:")
    print_seq_ids(peak2_records)
    print("Sequence ids for 3rd sequence:")
    print_seq_ids(peak3_records)


def blastn(sequence):

    # At this point it's better to use local blast and db; it takes ages...
    bacteria_taxid= "bacteria[ORGN]"
    result = NCBIWWW.qblast("blastn", "nt", sequence, alignments=1,
                            hitlist_size=1, entrez_query=bacteria_taxid)
    records = NCBIXML.parse(result)
    print("found")

    for record in records:
        for alignment in record.alignments:
            return alignment.hit_def


def find_and_add_matches(table, records):

    for sequence_record in records:
        seq = sequence_record.seq
        match = blastn(seq)
        table.append([sequence_record.id, match])


def blast_and_save_to_table(peak1_records, peak2_records, peak3_records):
    table = [["ID", "Found match"]]

    find_and_add_matches(table, peak1_records)
    find_and_add_matches(table, peak2_records)
    find_and_add_matches(table, peak3_records)

    with open('table.txt', 'w') as file:
        file.write(tabulate(table, headers="firstrow", tablefmt="github"))


def main():
    filepath = "sequences/sequence.fastq"

    print_encodings(filepath)

    seq_records = SeqIO.parse(filepath, "fastq")

    x_axis, y_axis = get_gc_axis(seq_records)
    print_gc_plot(x_axis, y_axis)

    # reopen the fastq file, read it again.
    seq_records = SeqIO.parse(filepath, "fastq")
    peak1_records, peak2_records, peak3_records = get_peak_sequences(seq_records, x_axis, y_axis)
    print_peak_seqs_ids(peak1_records, peak2_records, peak3_records)

    blast_and_save_to_table(peak1_records, peak2_records, peak3_records)


if __name__ == '__main__':
    main()
