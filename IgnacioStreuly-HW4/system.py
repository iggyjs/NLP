def main():
    count_table = {}
    likelihood_table = {}
    total_words = 0
    total_pos_tags = 0

    with open("training_corpus.pos") as f:

        for line in f:
            array = line.split("\t")
            if len(array) < 2:
                continue

            value = array[0]
            pos = array[1]
            pos = pos.replace("\n", "")
            value = value.lower()

            if not pos in count_table:
                count_table[pos]= 1
                total_pos_tags += 1

            if pos in count_table:
                count_table[pos] += 1

            total_words += 1

        for key, value in count_table.iteritems():
            likelihood_table[key] = float(count_table[key])/total_words

    #TODO prior_probability_table

main()
